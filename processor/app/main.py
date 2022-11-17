import asyncio

from services.extract import extract_payments


async def exctractor() -> None:
    while True:
        await extract_payments()


if __name__ == '__main__':
    asyncio.run(exctractor())
