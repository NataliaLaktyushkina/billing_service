import uvicorn
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI, Depends
from fastapi.responses import ORJSONResponse

from api.v1 import payment, admin
from core.config import settings
from db import kafka
from services.jwt_check import JWTBearer

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

PROTECTED = [Depends(JWTBearer())]


@app.on_event('startup')
async def startup():
    kafka_settings = settings.kafka_settings
    kafka.bus_kafka = AIOKafkaProducer(
        bootstrap_servers=f'{kafka_settings.KAFKA_HOST}:{kafka_settings.KAFKA_PORT}',
        max_batch_size=1000)


@app.on_event('shutdown')
async def shutdown():
    await kafka.bus_kafka.stop()


app.include_router(payment.router, prefix='/api/v1/payments',
                   tags=['users'], dependencies=PROTECTED)
app.include_router(admin.router, prefix='/api/v1/admin',
                   tags=['admins'], dependencies=PROTECTED)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8101,
    )
