from typing import Any, Literal
from sqlalchemy import select, desc, asc, or_, String
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import func
from sqlalchemy.sql.base import Executable
from datetime import timedelta, datetime
from uuid import UUID, uuid4

from config import settings
from exceptions import NotFoundError
from schemas.user import UserCreateSchema
from database import async_session
from database import (User,
                      UserBaseInfo)


async def get_session():
    async with Session() as session:
        yield session


class BaseSession:
    def __init__(self):
        self.session = async_session()

    async def __aenter__(self):
        await self.session.begin()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type:
            await self.session.rollback()
        else:
            await self.session.commit()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def flush(self):
        await self.session.flush()

    async def rollback(self):
        await self.session.rollback()

    async def execute(self, stmt):
        return await self.session.execute(stmt)

    async def add_record(self, orm_obj):
        self.session.add(orm_obj)
        await self.session.flush()

    @staticmethod
    def update_record(orm_obj, update_data: dict) -> None:
        for k, v in update_data.items():
            setattr(orm_obj, k, v)

    async def delete_record(self, instance):
        await self.session.delete(instance)

    async def _get_stmt_result(self,
                               _db=None,
                               _filtering: dict | None = None,
                               _ordering: tuple[str, Literal["desc", "asc"]] | None = None,
                               _mode: Literal["one", "or", "all", "all_or"] | str = "one",
                               stmt: Executable | None = None) -> Any:
        stmt = stmt if stmt is not None else self._build_stmt(_db, _filtering, _ordering, _mode)

        if _mode in ["all", "all_or"]:
            result = await self.session.scalars(stmt)
            return result.fetchall()
        else:
            return await self.session.scalar(stmt)

    @staticmethod
    def _build_stmt(_db,
                    _filtering: dict | None = None,
                    _ordering: tuple[str, Literal["desc", "asc"]] | None = None,
                    _mode: str = "one"):
        """
        Args:
            _db: orm class
            _filtering: dictionary to put the {key: value} data
            _ordering: tuple to order by. ("KEY to order by", "desc or asc")
            _mode: "one", "or", "all"
                - "one": get one result with AND condition to combine _filtering param
                - "or": get one result with OR condition to combine _filtering param
                - "all": get all results with AND condition to combine _filtering param
                - "all_or": get all results with OR condition to combine _filtering param
        Returns: stmt
        """

        assert _db is not None

        stmt = select(_db)
        if _filtering is None:
            stmt = stmt
        else:
            if _mode in ["or", "all_or"]:
                or_condition = None
                for k, v in _filtering.items():
                    if or_condition is None:
                        or_condition = (getattr(_db, k) == v)
                    else:
                        or_condition = or_condition | (getattr(_db, k) == v)
                else:
                    stmt = stmt.where(or_condition)
            else:
                stmt = stmt.filter_by(**_filtering)

        if _ordering is not None:
            key, order = _ordering
            _order_func = desc if order == "desc" else asc
            stmt = stmt.order_by(_order_func(getattr(_db, key)))

        return stmt


class Session(BaseSession):
    async def get_user_by_user_id(self, user_id: str) -> User | None:
        return await self._get_user({"id": user_id})

    async def get_user_by_username(self, username: str) -> User | None:
        return await self._get_user({"username": username})

    async def get_users(self) -> list[User]:
        return await self._get_user(_mode="all")

    async def _get_user(self, _filtering=None, _ordering=None, _mode: str = "one",
                        stmt=None) -> User | list[User] | None:
        return await self._get_stmt_result(_db=User, _filtering=_filtering, _ordering=_ordering, _mode=_mode, stmt=stmt)

    async def add_user(self, data: UserCreateSchema) -> User:
        data_dict = data.model_dump()
        data_dict.update({"id": str(uuid4())})
        new_user = User(**data_dict)
        await self.add_record(new_user)
        return new_user

    async def get_user_base_info(self, user_guid: int):
        stmt = (select(User, UserBaseInfo).
                join(User.base_info).
                where(User.user_guid == user_guid))
        res = await self.session.execute(stmt)

        return res.fetchone()
