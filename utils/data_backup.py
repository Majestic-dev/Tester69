import asyncio
import subprocess

from data_manager import DataManager


async def main():
    await DataManager.initialise()
    postgres_user = DataManager.get("config", "postgres_user")
    postgres_database = DataManager.get("config", "postgres_database")

    subprocess.run(
        [
            "pg_dump",
            "-h",
            "localhost",
            "-U",
            postgres_user,
            "-d",
            postgres_database,
            "--file",
            "data/backup.sql",
        ]
    )


if __name__ == "__main__":
    asyncio.run(main())
