import asyncio

from extract import extract_data


async def exctractor() -> None:
    while True:
        await extract_data()


if __name__ == '__main__':
    asyncio.run(exctractor())
