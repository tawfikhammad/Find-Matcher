from controller import ScrapeController
import asyncio

async def main():
    controller = ScrapeController()
    await controller.store_into_vdb()

if __name__ == "__main__":
    asyncio.run(main())