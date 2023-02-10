import json
import os
from typing import Any, Optional


class DataManager:
    __data = {}

    def __init__(self, paths: list[tuple[str, str]]) -> None:
        for name, path, default in paths:
            if not os.path.exists(os.path.dirname(path)):
                os.mkdir(os.path.dirname(path))

            if not os.path.isfile(path):
                with open(path, "w") as f:
                    json.dump(default, f, indent=4)

            with open(path, "r") as f:
                self.__data[name] = json.load(f)

    @classmethod
    def get(cls, path: str, key: str) -> Any:
        return cls.__data[path].get(key, None)

    @classmethod
    def set(cls, path: str, key: str, value: Any) -> None:
        cls.__data[path][key] = value
        cls.save(path)

    @classmethod
    def add_user_data(cls, user_id: int) -> None:
        if str(user_id) not in cls.__data["users"]:
            cls.__data["users"][str(user_id)] = {"inventory": {}, "balance": 0}

        cls.save("users")

    @classmethod
    def get_user_data(cls, user_id: int) -> Optional[dict]:
        if str(user_id) not in cls.__data["users"]:
            cls.add_user_data(user_id)

        return cls.__data["users"].get(str(user_id), None)

    @classmethod
    def edit_user_data(cls, user_id: int, key: str, value: Any) -> None:
        if str(user_id) not in cls.__data["users"]:
            cls.add_user_data(user_id)

        cls.__data["users"][str(user_id)][key] = value
        cls.save("users")

    @classmethod
    def edit_user_inventory(cls, user_id: int, item: str, amount: int) -> None:
        if str(user_id) not in cls.__data["users"]:
            cls.add_user_data(user_id)

        if item not in cls.__data["users"][str(user_id)]["inventory"]:
            cls.__data["users"][str(user_id)]["inventory"][item] = 0

        cls.__data["users"][str(user_id)]["inventory"][item] += amount

        if cls.__data["users"][str(user_id)]["inventory"][item] <= 0:
            del cls.__data["users"][str(user_id)]["inventory"][item]

        cls.save("users")

    @classmethod
    def save(cls, path: str) -> None:
        with open(f"data/{path}.json", "w") as f:
            json.dump(cls.__data[path], f, indent=4)
