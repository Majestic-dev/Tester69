import asyncio
import datetime
import json
import os
import random
import uuid
from dataclasses import dataclass
from typing import Any

import asyncpg


@dataclass
class Inventory:
    id: int
    items: dict[str, Any] = None


@dataclass
class User:
    id: int
    inventory: dict[str, Any] = None
    cooldowns: dict[str, Any] = None
    balance: int = None
    bank: int = None


@dataclass
class Guild:
    id: int
    muted_role_id: int = None
    muted_user_roles: dict[str, Any] = None
    unverified_role_id: int = None
    verification_channel_id: int = None
    verification_logs_channel_id: int = None
    logs_channel_id: int = None
    appeal_link: str = None
    blacklisted_words: list[str] = None
    whitelist: list[int] = None
    welcome_message: str = None
    warned_users: dict[str, Any] = None


class DataManager:
    guilds: dict[str, Guild] = {}
    users: dict[str, User] = {}
    __data: dict[str, str] = {}
    initialised = False

    @classmethod
    def setup(cls, paths: list[tuple[str, str, str]]) -> None:
        for path in paths:
            path, default = path

            if not os.path.exists(path):
                if not os.path.exists(os.path.dirname(path)):
                    os.makedirs(os.path.dirname(path))

                with open(path, "w") as file:
                    file.write(json.dumps(default, indent=4))

    @classmethod
    async def initialise(cls) -> None:
        for root, _, files in os.walk(os.curdir):
            for file in files:
                if not file.endswith(".json"):
                    continue

                with open(os.path.join(root, file), "r") as f:
                    cls.__data[file[:-5]] = json.load(f)

        DataManager.initialised = True

        cls.db_connection = await asyncpg.create_pool(
            user=DataManager.get("config", "postgres_user"),
            host="127.0.0.1",
            password=DataManager.get("config", "postgres_password"),
            database=DataManager.get("config", "postgres_database"),
        )

        await cls.db_connection.execute(
            """CREATE TABLE IF NOT EXISTS guilds (
                id bigint PRIMARY KEY,
                unverified_role_id bigint,
                verification_channel_id bigint,
                verification_logs_channel_id bigint,
                logs_channel_id bigint,
                appeal_link TEXT,
                blacklisted_words TEXT ARRAY DEFAULT '{}'::text[],
                whitelist bigint ARRAY DEFAULT '{}'::bigint[],
                welcome_message TEXT,
                warned_users JSONB,
                giveaways JSONB
            );"""
        )

        await cls.db_connection.execute(
            """CREATE TABLE IF NOT EXISTS giveaways (
                id bigint PRIMARY KEY,
                guild_id bigint,
                channel_id bigint,
                end_date TEXT,
                winner_amount bigint,
                prize TEXT,
                extra_notes TEXT,
                host_id bigint,
                participants bigint ARRAY DEFAULT '{}'::bigint[],
                winners bigint ARRAY DEFAULT '{}'::bigint[],
                ended BOOLEAN DEFAULT FALSE
            );"""
        )

        await cls.db_connection.execute(
            """CREATE TABLE IF NOT EXISTS users (
                id bigint PRIMARY KEY,
                inventory JSONB,
                cooldowns JSONB,
                balance bigint DEFAULT 0,
                bank bigint DEFAULT 0
            );"""
        )

    @classmethod
    def get(cls, path: str, key: str) -> Any:
        return cls.__data.get(path, {}).get(key, None)

    @classmethod
    async def add_guild_data(cls, guild_id: int) -> None:
        async with cls.db_connection.acquire():
            await cls.db_connection.execute(
                "INSERT INTO guilds (id) VALUES ($1)", guild_id
            )

    @classmethod
    async def remove_guild_data(cls, guild_id: int) -> None:
        async with cls.db_connection.acquire():
            await cls.db_connection.execute(
                "DELETE FROM guilds WHERE id = $1", guild_id
            )

    @classmethod
    async def remove_guilds_column(cls, column: str) -> None:
        async with cls.db_connection.acquire():
            columnexists = await cls.db_connection.fetchval(
                f"SELECT EXISTS (SELECT FROM information_schema.columns WHERE table_name = 'guilds' AND column_name = '{column}')"
            )

            if columnexists:
                await cls.db_connection.execute(
                    f"ALTER TABLE guilds DROP COLUMN IF EXISTS {column}"
                )

            elif not columnexists:
                return

    @classmethod
    async def add_guilds_column(cls, column: str, value: Any) -> None:
        async with cls.db_connection.acquire():
            columnexists = await cls.db_connection.fetchval(
                f"SELECT EXISTS (SELECT FROM information_schema.columns WHERE table_name = 'guilds' AND column_name = '{column}')"
            )

            if not columnexists:
                await cls.db_connection.execute(
                    f"ALTER TABLE guilds ADD COLUMN IF NOT EXISTS {column} {value}"
                )

            elif columnexists:
                await cls.db_connection.execute(
                    f"ALTER TABLE guilds ALTER COLUMN {column} TYPE {value} USING {column}::{value}"
                )

    @classmethod
    async def get_all_guilds(cls) -> None:
        async with cls.db_connection.acquire():
            rows = await cls.db_connection.fetch("SELECT id FROM guilds")
            return [row["id"] for row in rows]

    @classmethod
    async def get_guild_data(cls, guild_id: int) -> None:
        async with cls.db_connection.acquire():
            if guild_id not in await cls.get_all_guilds():
                await cls.add_guild_data(guild_id)

            row = await cls.db_connection.fetchrow(
                "SELECT * FROM guilds WHERE id = $1", guild_id
            )
            return row

    @classmethod
    async def edit_guild_data(cls, guild_id: int, key: str, value: Any) -> None:
        async with cls.db_connection.acquire():
            if guild_id not in await cls.get_all_guilds():
                await cls.add_guild_data(guild_id)

            await cls.db_connection.execute(
                f"UPDATE guilds SET {key} = $1 WHERE id = $2", value, guild_id
            )

    @classmethod
    async def edit_blacklisted_words(cls, guild_id: int, words: list[str]) -> None:
        async with cls.db_connection.acquire():
            if guild_id not in await cls.get_all_guilds():
                await cls.add_guild_data(guild_id)

            await cls.db_connection.execute(
                "UPDATE guilds SET blacklisted_words = $1 WHERE id = $2",
                words,
                guild_id,
            )

    @classmethod
    async def edit_whitelist(cls, guild_id: int, whitelist: list[int]) -> None:
        async with cls.db_connection.acquire():
            if guild_id not in await cls.get_all_guilds():
                await cls.add_guild_data(guild_id)

            await cls.db_connection.execute(
                "UPDATE guilds SET whitelist = $1 WHERE id = $2", whitelist, guild_id
            )

    @classmethod
    async def register_warning(cls, guild_id: int, user_id: int, reason: str) -> None:
        async with cls.db_connection.acquire():
            if guild_id not in await cls.get_all_guilds():
                await cls.add_guild_data(guild_id)

            existing_warnings = await cls.db_connection.fetchval(
                "SELECT warned_users FROM guilds WHERE id = $1", guild_id
            )
            new_warning = {str(user_id): [{str(uuid.uuid4()): reason}]}

            if existing_warnings is None:
                await cls.db_connection.execute(
                    "UPDATE guilds SET warned_users = $1::jsonb WHERE id = $2",
                    json.dumps(new_warning),
                    guild_id,
                )

            else:
                warned_user_dict = json.loads(existing_warnings)
                if str(user_id) in warned_user_dict:
                    warned_user_dict[str(user_id)].append(new_warning)
                else:
                    warned_user_dict[str(user_id)] = [new_warning]

                await cls.db_connection.execute(
                    "UPDATE guilds SET warned_users = $1::jsonb WHERE id = $2",
                    json.dumps(warned_user_dict),
                    guild_id,
                )

    @classmethod
    async def delete_warning(cls, guild_id: int, warning_uuid: uuid.uuid4) -> None:
        async with cls.db_connection.acquire():
            if guild_id not in await cls.get_all_guilds():
                await cls.add_guild_data(guild_id)

            warned_users_json = await cls.db_connection.fetchval(
                "SELECT warned_users FROM guilds WHERE id  = $1 FOR UPDATE", guild_id
            )

            if warned_users_json:
                warned_users_dict = json.loads(warned_users_json)
                found = False
                for user_warnings in warned_users_dict.values():
                    for warning in user_warnings:
                        if warning.get(warning_uuid):
                            user_warnings.remove(warning)
                            found = True
                            break

                if found:
                    await cls.db_connection.execute(
                        "UPDATE guilds SET warned_users = $1::jsonb WHERE id = $2",
                        json.dumps(warned_users_dict),
                        guild_id,
                    )
                    return True
                else:
                    return False

    @classmethod
    async def get_user_warnings(cls, guild_id: int, user_id: int) -> None:
        async with cls.db_connection.acquire():
            if guild_id not in await cls.get_all_guilds():
                await cls.add_guild_data(guild_id)

            warned_users_json = await cls.db_connection.fetchval(
                "SELECT warned_users FROM guilds where id = $1", guild_id
            )

            if warned_users_json:
                warned_users_dict = json.loads(warned_users_json)
                return warned_users_dict.get(str(user_id), [])

    @classmethod
    async def register_giveaway(
        cls,
        giveaway_id: int,
        guild_id: int,
        channel_id: int,
        minutes: int,
        winners: int,
        prize: str,
        extra_notes: str,
        host_id: int,
    ) -> None:
        async with cls.db_connection.acquire():
            end_date = datetime.datetime.now() + datetime.timedelta(minutes=minutes)
            await cls.db_connection.execute(
                "INSERT INTO giveaways (id, guild_id, channel_id, end_date, winner_amount, prize, extra_notes, host_id) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)",
                giveaway_id,
                guild_id,
                channel_id,
                end_date.isoformat(),
                winners,
                prize,
                extra_notes,
                host_id,
            )

    @classmethod
    async def edit_giveaway(
        cls, giveaway_id: int, guild_id: int, column: str, value: Any
    ) -> None:
        async with cls.db_connection.acquire():
            await cls.db_connection.execute(
                f"UPDATE giveaways SET {column} = $1 WHERE id = $2 AND guild_id = $3",
                value,
                giveaway_id,
                guild_id,
            )

    @classmethod
    async def add_giveaway_participant(cls, giveaway_id: int, user_id: int) -> None:
        async with cls.db_connection.acquire():
            participants = await cls.db_connection.fetchval(
                "SELECT participants FROM giveaways WHERE id = $1", giveaway_id
            )

            if user_id not in participants:
                await cls.db_connection.execute(
                    "UPDATE giveaways SET participants = array_append(participants, $1) WHERE id = $2",
                    user_id,
                    giveaway_id,
                )
                return True

            elif user_id in participants:
                return False

    @classmethod
    async def remove_giveaway_participant(cls, giveaway_id: int, user_id: int) -> None:
        async with cls.db_connection.acquire():
            participants = await cls.db_connection.fetchval(
                "SELECT participants FROM giveaways WHERE id = $1", giveaway_id
            )

            if user_id in participants:
                await cls.db_connection.execute(
                    "UPDATE giveaways SET participants = array_remove(participants, $1) WHERE id = $2",
                    user_id,
                    giveaway_id,
                )
                return True

            elif user_id not in participants:
                return False

    @classmethod
    async def replace_giveaway_winner(
        cls, giveaway_id: int, guild_id: int, replaced_user_id: int
    ) -> None:
        async with cls.db_connection.acquire():
            giveaway_data = await cls.get_giveaway_data(giveaway_id, guild_id)
            new_random_winner = random.choice(giveaway_data["participants"])
            await cls.db_connection.execute(
                "UPDATE giveaways SET winners = array_replace(winners, $1, $2) WHERE id = $3 AND guild_id = $4",
                replaced_user_id,
                new_random_winner,
                giveaway_id,
                guild_id,
            )
            return new_random_winner

    @classmethod
    async def get_giveaway_data(cls, giveaway_id: int, guild_id: int) -> None:
        async with cls.db_connection.acquire():
            row = await cls.db_connection.fetchrow(
                "SELECT * FROM giveaways WHERE id = $1 AND guild_id = $2",
                giveaway_id,
                guild_id,
            )
            return row

    @classmethod
    async def get_next_giveaway(cls) -> None:
        async with cls.db_connection.acquire():
            row = await cls.db_connection.fetchrow(
                "SELECT * FROM giveaways WHERE end_date > $1 AND ended = FALSE ORDER BY end_date ASC",
                datetime.datetime.now().isoformat(),
            )
            return row

    @classmethod
    async def end_giveaway(cls, giveaway_id: int, guild_id: int) -> None:
        async with cls.db_connection.acquire():
            await cls.db_connection.execute(
                "UPDATE giveaways SET ended = TRUE WHERE id = $1 AND guild_id = $2",
                giveaway_id,
                guild_id,
            )

    @classmethod
    async def draw_giveaway_winners(cls, giveaway_id: int, guild_id: int) -> None:
        async with cls.db_connection.acquire():
            participants = await cls.db_connection.fetchval(
                "SELECT participants FROM giveaways WHERE id = $1 AND guild_id = $2",
                giveaway_id,
                guild_id,
            )
            winneramount = await cls.db_connection.fetchval(
                "SELECT winner_amount FROM giveaways WHERE id = $1 AND guild_id = $2",
                giveaway_id,
                guild_id,
            )

            winners = await cls.db_connection.fetchval(
                "SELECT winners FROM giveaways WHERE id = $1 AND guild_id = $2",
                giveaway_id,
                guild_id,
            )

            if participants == "[]":
                return False

            if winners != "[]":
                for winner in winners:
                    await cls.db_connection.execute(
                        "UPDATE giveaways SET winners = array_remove(winners, $1) WHERE id = $2 AND guild_id = $3",
                        winner,
                        giveaway_id,
                        guild_id,
                    )

            if len(participants) > winneramount:
                winners = random.sample(participants, winneramount)
                for winner in winners:
                    await cls.db_connection.execute(
                        "UPDATE giveaways SET winners = array_append(winners, $1) WHERE id = $2 AND guild_id = $3",
                        winner,
                        giveaway_id,
                        guild_id,
                    )
                return winners
            elif len(participants) <= winneramount:
                for participant in participants:
                    await cls.db_connection.execute(
                        "UPDATE giveaways SET winners = array_append(winners, $1) WHERE id = $2 AND guild_id = $3",
                        participant,
                        giveaway_id,
                        guild_id,
                    )
                return participants

    @classmethod
    async def get_all_users(cls) -> None:
        async with cls.db_connection.acquire():
            rows = await cls.db_connection.fetch("SELECT id FROM users")
            return [row["id"] for row in rows]

    @classmethod
    async def get_user_data(cls, user_id: int) -> None:
        async with cls.db_connection.acquire():
            if user_id not in await cls.get_all_users():
                await cls.add_user_data(user_id)

            row = await cls.db_connection.fetchrow(
                "SELECT * FROM users WHERE id = $1", user_id
            )
            return row

    @classmethod
    async def add_user_data(cls, user_id: int) -> None:
        async with cls.db_connection.acquire():
            await cls.db_connection.execute(
                "INSERT INTO users (id) VALUES ($1)", user_id
            )

    @classmethod
    async def edit_user_data(cls, user_id: int, key: str, value: Any) -> None:
        async with cls.db_connection.acquire():
            if user_id not in await cls.get_all_users():
                await cls.add_user_data(user_id)

            await cls.db_connection.execute(
                f"UPDATE users SET {key} = $1 WHERE id = $2", value, user_id
            )

    @classmethod
    async def edit_user_inventory(cls, user_id: int, item: str, amount: int) -> None:
        async with cls.db_connection.acquire():
            if user_id not in await cls.get_all_users():
                await cls.add_user_data(user_id)

            inventory = await cls.db_connection.fetchval(
                "SELECT inventory FROM users WHERE id = $1", user_id
            )

            if inventory is None:
                await cls.db_connection.execute(
                    "UPDATE users SET inventory = $1::jsonb WHERE id = $2",
                    json.dumps({item: amount}),
                    user_id,
                )
            else:
                inventory_dict = json.loads(inventory)
                if item not in inventory_dict:
                    inventory_dict[item] = amount
                    await cls.db_connection.execute(
                        "UPDATE users SET inventory = $1::jsonb WHERE id = $2",
                        json.dumps(inventory_dict),
                        user_id,
                    )
                else:
                    inventory_dict[item] += amount

                    await cls.db_connection.execute(
                        "UPDATE users SET inventory = $1::jsonb WHERE id = $2",
                        json.dumps(inventory_dict),
                        user_id,
                    )

    @classmethod
    async def add_cooldown(
        cls, user_id: int, command_name: str, cooldown_seconds: int
    ) -> None:
        async with cls.db_connection.acquire():
            if user_id not in await cls.get_all_users():
                await cls.add_user_data(user_id)

            cooldowns = await cls.db_connection.fetchval(
                "SELECT cooldowns FROM users WHERE id = $1", user_id
            )

            end_time = datetime.datetime.now() + datetime.timedelta(
                seconds=cooldown_seconds
            )
            new_cooldown = {command_name: end_time.isoformat()}

            if cooldowns is None:
                await cls.db_connection.execute(
                    "UPDATE users set cooldowns = $1::jsonb WHERE id = $2",
                    json.dumps(new_cooldown),
                    user_id,
                )
            else:
                cooldown_dict = json.loads(cooldowns)
                cooldown_dict.update(new_cooldown)

                await cls.db_connection.execute(
                    "UPDATE users SET cooldowns = $1::jsonb WHERE id = $2",
                    json.dumps(cooldown_dict),
                    user_id,
                )

    @classmethod
    async def get_cooldown_end(cls, user_id: int, command_name: str) -> None:
        async with cls.db_connection.acquire():
            if user_id not in await cls.get_all_users():
                await cls.add_user_data(user_id)

            cooldowns = await cls.db_connection.fetchval(
                "SELECT cooldowns FROM users WHERE id = $1", user_id
            )

            if cooldowns:
                cooldown_dict = json.loads(cooldowns)
                return cooldown_dict.get(command_name, None)

    @classmethod
    async def remove_cooldown(cls, user_id: int, command_name: str) -> None:
        async with cls.db_connection.acquire():
            if user_id not in await cls.get_all_users():
                await cls.add_user_data(user_id)

            cooldowns = await cls.db_connection.fetchval(
                "SELECT cooldowns FROM users WHERE id = $1", user_id
            )

            if cooldowns:
                cooldown_dict = json.loads(cooldowns)
                if command_name in cooldown_dict:
                    del cooldown_dict[command_name]

                    await cls.db_connection.execute(
                        "UPDATE users SET cooldowns = $1::jsonb WHERE id = $2",
                        json.dumps(cooldown_dict),
                        user_id,
                    )

    @classmethod
    async def remove_all_cooldowns(cls, user_id: int) -> None:
        async with cls.db_connection.acquire():
            if user_id not in await cls.get_all_users():
                await cls.add_user_data(user_id)

            await cls.db_connection.execute(
                "UPDATE users SET cooldowns = null WHERE id = $1", user_id
            )


async def main():
    await DataManager.initialise()


if __name__ == "__main__":
    asyncio.run(main())
