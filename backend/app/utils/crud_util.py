from typing import Any, Literal
from sqlalchemy import select, desc, asc, or_, String
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import func
from sqlalchemy.sql.base import Executable
from datetime import timedelta, datetime
from uuid import UUID, uuid4

from config import settings
from exceptions import NotFoundError
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
    async def get_user_by_user_guid(self, user_guid: str) -> User | None:
        return await self._get_user({"user_guid": user_guid})

    async def get_user_by_user_name(self, username: str) -> User | None:
        return await self._get_user({"username": username})

    async def get_users(self) -> list[User]:
        return await self._get_user(_mode="all")

    async def _get_user(self, _filtering=None, _ordering=None, _mode: str = "one",
                        stmt=None) -> User | list[User] | None:
        return await self._get_stmt_result(_db=User, _filtering=_filtering, _ordering=_ordering, _mode=_mode, stmt=stmt)

    async def add_user(self, data) -> User:
        data_dict = data.model_dump()
        data_dict.update({"user_guid": str(uuid4())})
        new_user = User(**data_dict)
        await self.add_record(new_user)
        return new_user

    async def get_user_base_info(self, user_guid: int):
        stmt = (select(User, UserBaseInfo).
                join(User.base_info).
                where(User.user_guid == user_guid))
        res = await self.session.execute(stmt)

        return res.fetchone()


    # async def get_own_company(self, user: User) -> Company | None:
    #     return await self._get_company({"company_code": int(user.company_code)})
    #
    # async def get_company_by_company_code(self, company_code: str | int) -> Company | None:
    #     return await self._get_company({"company_code": int(company_code)})
    #
    # async def get_companys(self) -> list[Company]:
    #     return await self._get_company(_mode="all")
    #
    # async def _get_company(self, _filtering: dict | None = None, _ordering=None, _mode: str = "one",
    #                        stmt=None) -> Company | list[Company] | None:
    #     return await self._get_stmt_result(_db=Company, _filtering=_filtering, _ordering=_ordering, _mode=_mode,
    #                                        stmt=stmt)
    #
    # async def add_company(self) -> Company:
    #     new_company_code = await self.get_max_company_code()
    #     new_company = Company(
    #         company_code=new_company_code,
    #     )
    #     await self.add_record(new_company)
    #     return new_company
    #
    # async def update_company(self, orm_obj, data):
    #     data_dict = data.model_dump()
    #     self.update_record(orm_obj, data_dict)
    #
    # async def get_robot_by_head_id(self, head_id: str) -> Robot:
    #     return await self._get_robot({"head_id": head_id})
    #
    # async def get_robot_by_body_id(self, body_id: str) -> Robot:
    #     return await self._get_robot({"body_id": body_id})
    #
    # async def get_robot_by_service_id(self, service_id: str) -> Robot:
    #     return await self._get_robot({"service_id": service_id})
    #
    # async def get_robots_by_body_id_head_id(self, _id: str, _mode: str = "all_or") -> Robot | list[Robot]:
    #     return await self._get_robot(_filtering={"body_id": _id, "head_id": _id}, _mode=_mode)
    #
    # async def get_robot_by_or_body_id_head_id(self, _id: str, _mode: str = "or") -> Robot | None:
    #     return await self._get_robot(_filtering={"body_id": _id, "head_id": _id}, _mode=_mode)
    #
    # async def get_own_robots(self, user: User) -> list[Robot]:
    #     return await self.get_robots_by_cognito_id(user.cognito_id)
    #
    # async def get_robots_by_cognito_id(self, cognito_id) -> list[Robot]:
    #     return await self._get_robot(_filtering={"cognito_id": str(cognito_id)}, _mode="all")
    #
    # async def get_own_robot_by_head_id_or_body_id(self, user: User, robot_id) -> Robot | None:
    #     stmt = select(Robot).where(Robot.cognito_id == str(user.cognito_id)).where(
    #         or_(
    #             Robot.head_id == robot_id,
    #             Robot.body_id == robot_id
    #         )
    #     )
    #     return await self._get_stmt_result(stmt=stmt)
    #
    # async def get_own_robots_by_kw_included(self, kw: str, user: User) -> list[tuple[Robot, Profile]]:
    #     keyword_pattern = f"%{kw.lower()}%"
    #     stmt = select(Robot, Profile).outerjoin(
    #         Profile, Robot.profile_id == Profile.id
    #     ).where(Robot.cognito_id == str(user.cognito_id)).where(
    #         or_(
    #             func.lower(func.cast(Robot.id, String)).like(keyword_pattern),
    #             func.lower(func.cast(Robot.uuid, String)).like(keyword_pattern),
    #             func.lower(Robot.head_id).like(keyword_pattern),
    #             func.lower(Robot.body_id).like(keyword_pattern),
    #             func.lower(Robot.cognito_email).like(keyword_pattern),
    #             func.lower(Profile.name).like(keyword_pattern),
    #             func.lower(func.cast(Profile.id, String)).like(keyword_pattern),
    #         )
    #     ).order_by(asc(Robot.id))
    #
    #     results = await self.execute(stmt)
    #     return results.fetchall()
    #
    # async def get_robots_by_kw_included(self, kw: str) -> list[tuple[Robot, Profile]]:
    #     keyword_pattern = f"%{kw.lower()}%"
    #     stmt = select(Robot, Profile).outerjoin(
    #         Profile, Robot.profile_id == Profile.id
    #     ).where(
    #         or_(
    #             func.lower(func.cast(Robot.id, String)).like(keyword_pattern),
    #             func.lower(func.cast(Robot.uuid, String)).like(keyword_pattern),
    #             func.lower(Robot.head_id).like(keyword_pattern),
    #             func.lower(Robot.body_id).like(keyword_pattern),
    #             func.lower(Robot.cognito_email).like(keyword_pattern),
    #             func.lower(Profile.name).like(keyword_pattern),
    #             func.lower(func.cast(Profile.id, String)).like(keyword_pattern),
    #         )
    #     ).order_by(asc(Robot.id))
    #
    #     results = await self.execute(stmt)
    #     return results.fetchall()
    #
    # async def get_robots_by_store_code(self, store_code: str | int) -> list[Robot]:
    #     return await self._get_robot({"store_code": int(store_code)}, _mode="all")
    #
    # async def get_robot_by_uuid(self, robot_uuid) -> Robot | None:
    #     return await self._get_robot({"uuid": robot_uuid})
    #
    # async def get_robots(self) -> list[Robot]:
    #     return await self._get_robot(_mode="all")
    #
    # async def _get_robot(self, _filtering: dict | None = None, _ordering=None, _mode: str = "one",
    #                      stmt=None) -> Robot | list[Robot] | None:
    #     return await self._get_stmt_result(_db=Robot, _filtering=_filtering, _ordering=_ordering, _mode=_mode,
    #                                        stmt=stmt)
    #
    # async def update_robot_cognito_id(self, orm_obj, cognito_info: dict) -> Robot:
    #     self.update_record(orm_obj, cognito_info)
    #     await self.commit()
    #     return orm_obj
    #
    # async def update_robot(self, orm_obj, data) -> None:
    #     data_dict = data.model_dump()
    #     self.update_record(orm_obj, data_dict)
    #     orm_obj.update_datetime = datetime.utcnow()
    #
    # async def get_stores_by_company_code(self, company_code) -> list[Store]:
    #     return await self._get_store({"company_code": int(company_code)}, _mode="all")
    #
    # async def get_own_stores(self, user: User) -> list[Store]:
    #     return await self._get_store({"company_code": int(user.company_code)}, _mode="all")
    #
    # async def get_store_by_store_code(self, store_code) -> Store | None:
    #     return await self._get_store({"store_code": int(store_code)})
    #
    # async def get_store_by_company_code_and_store_name(self, company_code, store_name) -> Store:
    #     return await self._get_store({"store_name": store_name, "company_code": int(company_code)}, _mode="and")
    #
    # async def get_stores(self) -> list[Store]:
    #     return await self._get_store(_mode="all")
    #
    # async def _get_store(self, _filtering: dict | None = None, _ordering=None, _mode: str = "one",
    #                      stmt=None) -> Store | list[Store] | None:
    #     return await self._get_stmt_result(_db=Store, _filtering=_filtering, _ordering=_ordering, _mode=_mode,
    #                                        stmt=stmt)
    #
    # async def add_store(self, data) -> None:
    #     store_code = await self.get_max_store_code()
    #     new_store = Store(**data.model_dump(), store_code=store_code)
    #     await self.add_record(new_store)
    #
    # async def update_store(self, orm_obj, data):
    #     data_dict = data.model_dump()
    #     self.update_record(orm_obj, data_dict)
    #
    # async def get_issue_signature_by_error_id(self, error_id: str) -> SignatureTranslation:
    #     return await self._get_signature({"error_id": error_id})
    #
    # async def get_issue_signature_by_record_id(self, record_id: str | int) -> SignatureTranslation:
    #     return await self._get_signature({"record_id": int(record_id)})
    #
    # async def get_signatures(self) -> list[SignatureTranslation]:
    #     return await self._get_signature(_mode="all")
    #
    # async def _get_signature(self, _filtering: dict | None = None, _ordering=None, _mode: str = "one",
    #                          stmt=None) -> SignatureTranslation | list[SignatureTranslation] | None:
    #     return await self._get_stmt_result(_db=SignatureTranslation, _filtering=_filtering, _ordering=_ordering,
    #                                        _mode=_mode, stmt=stmt)
    #
    # async def get_swap_by_ticket_create_datetime(self, from_date: datetime, to_date: datetime) -> list[Swap]:
    #     stmt = select(Swap).where(
    #         (Swap.ticket_create_datetime >= from_date) &
    #         (Swap.ticket_create_datetime <= to_date)
    #     )
    #     return await self._get_swap(_mode="all", stmt=stmt)
    #
    # async def _get_swap(self, _filtering: dict | None = None, _ordering=None, _mode: str = "one", stmt=None):
    #     return await self._get_stmt_result(_db=Swap, _filtering=_filtering, _ordering=_ordering, _mode=_mode, stmt=stmt)
    #
    # async def get_swaps_by_service_id(self, service_ids, from_datetime: datetime) -> list[Swap]:
    #     stmt = select(Swap).where(
    #         (Swap.service_id.in_(service_ids)) &
    #         (Swap.reception_shipment_datetime + timedelta(days=1) >= from_datetime)
    #     ).order_by(Swap.rma_case_number.desc())
    #     return await self._get_stmt_result(None, _mode="all", stmt=stmt)
    #
    # async def get_kintone_swap_by_uuid(self, uuid_) -> KintoneSwap | None:
    #     return await self._get_kintone_swap(_filtering={"uuid": uuid_})
    #
    # async def _get_kintone_swap(self, _filtering: dict | None = None, _ordering=None, _mode: str = "one", stmt=None):
    #     return await self._get_stmt_result(_db=KintoneSwap, _filtering=_filtering, _ordering=_ordering, _mode=_mode,
    #                                        stmt=stmt)
    #
    # async def get_messages_by_date_answer(self, from_date: datetime, to_date: datetime, mode) -> list[Message]:
    #     stmt = select(Message).where(
    #         (Message.date_answer >= from_date) &
    #         (Message.date_answer <= to_date) &
    #         (Message.mode == mode)
    #     )
    #     return await self._get_stmt_result(_mode="all", stmt=stmt)
    #
    # async def get_messages_by_session_id(self, session_id: str, mode: str) -> list[Message]:
    #     stmt = select(Message).where(
    #         (Message.session_id.contains(session_id)) &
    #         (Message.mode == mode)
    #     )
    #     return await self._get_stmt_result(_mode="all", stmt=stmt)
    #
    # async def add_message(self, message):
    #     new_message = Message(
    #         record_uuid=message['record_uuid'],
    #         session_id=message['session_id'],
    #         date_answer=message['date_answer'],
    #         input_type=message['input_type'],
    #         input_msg=message['input_msg'],
    #         input_timezone=message['input_timezone'],
    #         input_mode=message['input_mode'],
    #         input_semantics=message['input_semantics'],
    #         answer_type=message['answer_type'],
    #         answer_msg=message['answer_msg'],
    #         answer_fullsession=message['answer_fullsession'],
    #         answer_mode=message['answer_mode'],
    #         answer_buttons=message['answer_buttons'],
    #         answer_nodding=message['answer_nodding'],
    #         answer_semantics=message['answer_semantics'],
    #         answer_previous_activated=message['answer_previous_activated'],
    #         update_datetime=message['update_datetime'],
    #         user_agent=message['user_agent'],
    #         next_id=message['next_id'],
    #         mode=message['mode']
    #     )
    #
    #     await self.add_record(new_message)
    #
    # async def get_robot_mac_address(self, robot_id: str) -> RobotMacAddress | None:
    #     return await self._get_robot_macaddress(_filtering={"body_id": robot_id, "head_id": robot_id}, _mode="or")
    #
    # async def _get_robot_macaddress(self, _filtering: dict | None = None, _ordering=None, _mode: str = "one",
    #                                 stmt=None) -> RobotMacAddress | list[RobotMacAddress] | None:
    #     return await self._get_stmt_result(_db=RobotMacAddress, _filtering=_filtering, _ordering=_ordering, _mode=_mode,
    #                                        stmt=stmt)
    #
    # async def get_robot_and_robot_mac_address(self, robot_id: str):
    #     stmt = select(Robot, RobotMacAddress).join(
    #         RobotMacAddress, Robot.head_id == RobotMacAddress.head_id, isouter=True
    #     ).where(
    #         (
    #                 (Robot.body_id == robot_id) |
    #                 (Robot.head_id == robot_id)
    #         )
    #     )
    #     result = await self.session.execute(stmt)
    #     return result.first()
    #
    # async def get_robot_by_service_id_included(self, service_ids) -> Robot | None:
    #     stmt = select(Robot).where(
    #         Robot.service_id.in_(service_ids)
    #     ).limit(1)
    #
    #     result = await self.session.execute(stmt)
    #     return result.scalar_one_or_none()
    #
    # async def get_convert_robot_by_uuid(self, uuid_: str | UUID) -> ConvertRobotId | None:
    #     return await self._get_convert_robot({"uuid": uuid_})
    #
    # async def get_convert_robot_history_by_uuid(self, uuid_: str | UUID) -> ConvertRobotIdHistory | None:
    #     return await self._get_convert_robot_history({"uuid": uuid_})
    #
    # async def _get_convert_robot(self, _filtering: dict | None = None, _ordering=None, _mode: str = "one",
    #                              stmt=None) -> ConvertRobotId | list[ConvertRobotId] | None:
    #     return await self._get_stmt_result(_db=ConvertRobotId, _filtering=_filtering, _ordering=_ordering, _mode=_mode,
    #                                        stmt=stmt)
    #
    # async def _get_convert_robot_history(self, _filtering: dict | None = None, _ordering=None, _mode: str = "one",
    #                                      stmt=None) -> ConvertRobotIdHistory | list[ConvertRobotIdHistory] | None:
    #     return await self._get_stmt_result(_db=ConvertRobotIdHistory, _filtering=_filtering, _ordering=_ordering,
    #                                        _mode=_mode, stmt=stmt)
    #
    # async def add_convert_robot_data(self, _obj: dict) -> None:
    #     await self.add_record(ConvertRobotId(uuid=_obj["uuid"], service_id=_obj["sno"]))
    #
    # async def update_convert_robot_data(self, orm_obj: ConvertRobotId, _obj: dict) -> None:
    #     orm_obj.uuid = _obj["uuid"]
    #     orm_obj.service_id = _obj["sno"]
    #     await self.flush()
    #
    # async def add_convert_robot_history_data(self, _obj: dict) -> None:
    #     new_history = ConvertRobotIdHistory(history_id=uuid4(), uuid=_obj["uuid"], service_id=_obj["sno"])
    #     await self.add_record(new_history)
    #
    # async def update_convert_robot_history_data(self, orm_obj: ConvertRobotIdHistory, _obj: dict) -> None:
    #     orm_obj.uuid = _obj["uuid"]
    #     orm_obj.service_id = _obj["sno"]
    #     await self.flush()
    #
    # async def get_max_company_code(self) -> int:
    #     stmt = select(func.max(Company.company_code))
    #     res = await self._get_stmt_result(stmt=stmt)
    #     return 1 if res is None else res + 1
    #
    # async def get_max_store_code(self) -> int:
    #     stmt = select(func.max(Store.store_code))
    #     res = await self._get_stmt_result(stmt=stmt)
    #     return 1 if res is None else res + 1
    #
    # async def get_job_by_id(self, job_id: int) -> Job | None:
    #     return await self._get_job({"id": job_id})
    #
    # async def get_job_by_include_id(self, job_ids: list[int]) -> list[Job]:
    #     if not job_ids:
    #         return []
    #     stmt = select(Job).where(Job.id.in_(job_ids))
    #     return await self._get_stmt_result(_mode="all", stmt=stmt)
    #
    # async def get_jobs_by_kw_included(self, kw: str) -> list[Job]:
    #     keyword_pattern = f"%{kw.lower()}%"
    #     stmt = select(Job).where(
    #         or_(
    #             func.lower(func.cast(Job.id, String)).like(keyword_pattern),
    #             func.lower(Job.name).like(keyword_pattern),
    #         )
    #     ).order_by(asc(Job.id))
    #
    #     results = await self.session.scalars(stmt)
    #     return results.fetchall()
    #
    # async def get_own_jobs_by_kw_included(self, kw: str, user: User) -> list[Job]:
    #     keyword_pattern = f"%{kw.lower()}%"
    #     stmt = select(Job).where(Job.cognito_id == str(user.cognito_id)).where(
    #         or_(
    #             func.lower(func.cast(Job.id, String)).like(keyword_pattern),
    #             func.lower(Job.name).like(keyword_pattern),
    #         )
    #     ).order_by(asc(Job.id))
    #
    #     results = await self.session.scalars(stmt)
    #     return results.fetchall()
    #
    # async def get_jobs(self) -> list[Job]:
    #     return await self._get_job(_mode="all")
    #
    # async def get_own_jobs(self, user: User) -> list[Job]:
    #     return await self._get_job(_filtering={"cognito_id": str(user.cognito_id)}, _mode="all")
    #
    # async def _get_job(self, _filtering: dict | None = None, _ordering=None, _mode: str = "one", stmt=None) -> Job | \
    #                                                                                                            list[
    #                                                                                                                Job] | None:
    #     return await self._get_stmt_result(_db=Job, _filtering=_filtering, _ordering=_ordering, _mode=_mode, stmt=stmt)
    #
    # async def add_job(self, job_data) -> Job:
    #     new_job = Job(
    #         cognito_id=job_data.cognito_id,
    #         cognito_email=job_data.cognito_email,
    #         name=job_data.name,
    #         user_guid=job_data.user_guid,
    #         instance_guid=job_data.instance_guid,
    #         instance_status=job_data.instance_guid
    #     )
    #     await self.add_record(new_job)
    #     return new_job
    #
    # async def update_job(self, orm_obj: Job, data: dict) -> Job:
    #     data.update({"version": orm_obj.version + 1})
    #     self.update_record(orm_obj, data)
    #     await self.session.flush()
    #
    #     return orm_obj
    #
    # async def get_job_transfer_records(self) -> list[JobTransferRecord]:
    #     return await self._get_job_transfer_record(_filtering={"resolved": False}, _mode="all")
    #
    # async def _get_job_transfer_record(self, _filtering: dict | None = None, _ordering=None, _mode: str = "one",
    #                                    stmt=None) -> JobTransferRecord | list[JobTransferRecord] | None:
    #     return await self._get_stmt_result(_db=JobTransferRecord, _filtering=_filtering, _ordering=_ordering,
    #                                        _mode=_mode, stmt=stmt)
    #
    # async def add_job_transfer_record(self, job_id: int, file_name: str, key: str):
    #     new_record = JobTransferRecord(job_id=job_id, file_name=file_name, key=key)
    #     await self.add_record(new_record)
    #
    # async def get_max_job_id(self) -> int:
    #     stmt = select(func.max(Job.id))
    #     res = await self._get_stmt_result(stmt=stmt)
    #     return 0 if res is None else res
    #
    # async def get_gen_conf_by_id(self, gen_conf_id: int) -> GenConf | None:
    #     return await self._get_gen_conf({"id": gen_conf_id})
    #
    # async def get_gen_confs(self) -> list[GenConf]:
    #     return await self._get_gen_conf(_ordering=("id", "asc"), _mode="all")
    #
    # async def _get_gen_conf(self, _filtering: dict | None = None, _ordering=None, _mode: str = "one",
    #                         stmt=None) -> GenConf | list[GenConf] | None:
    #     return await self._get_stmt_result(_db=GenConf, _filtering=_filtering, _ordering=_ordering, _mode=_mode,
    #                                        stmt=stmt)
    #
    # async def add_gen_conf(self, gen_conf_data) -> GenConf:
    #     new_gen_conf = GenConf(
    #         name=gen_conf_data.name,
    #     )
    #
    #     await self.add_record(new_gen_conf)
    #
    #     return new_gen_conf
    #
    # async def update_gen_conf(self, orm_obj: GenConf, data: dict) -> GenConf:
    #     data.update({"version": orm_obj.version + 1})
    #     self.update_record(orm_obj, data)
    #     await self.session.flush()
    #
    #     return orm_obj
    #
    # async def get_rps_conf_by_id(self, rps_conf_id: int) -> RPSConf | None:
    #     return await self._get_rps_conf({"id": rps_conf_id})
    #
    # async def get_rps_confs(self) -> list[RPSConf]:
    #     return await self._get_rps_conf(_ordering=("id", "asc"), _mode="all")
    #
    # async def _get_rps_conf(self, _filtering: dict | None = None, _ordering=None, _mode: str = "one",
    #                         stmt=None) -> RPSConf | list[RPSConf] | None:
    #     return await self._get_stmt_result(_db=RPSConf, _filtering=_filtering, _ordering=_ordering, _mode=_mode,
    #                                        stmt=stmt)
    #
    # async def add_rps_conf(self, rps_conf_data) -> RPSConf:
    #     new_rps_conf = RPSConf(
    #         name=rps_conf_data.name,
    #     )
    #
    #     await self.add_record(new_rps_conf)
    #
    #     return new_rps_conf
    #
    # async def update_rps_conf(self, orm_obj: RPSConf, data: dict) -> RPSConf:
    #     data.update({"version": orm_obj.version + 1})
    #     self.update_record(orm_obj, data)
    #     await self.session.flush()
    #
    #     return orm_obj
    #
    # async def get_profile_by_id(self, profile_id: int) -> Profile | None:
    #     return await self._get_profile({"id": profile_id})
    #
    # async def get_profiles(self) -> list[Profile]:
    #     return await self._get_profile(_ordering=("id", "asc"), _mode="all")
    #
    # async def _get_profile(self, _filtering: dict | None = None, _ordering=None, _mode: str = "one",
    #                        stmt=None) -> Profile | list[Profile] | None:
    #     return await self._get_stmt_result(_db=Profile, _filtering=_filtering, _ordering=_ordering, _mode=_mode,
    #                                        stmt=stmt)
    #
    # async def add_profile(self, profile_data) -> Profile:
    #     new_profile = Profile(
    #         name=profile_data.name,
    #         gen_id=profile_data.gen_id,
    #         rps_id=profile_data.rps_id,
    #     )
    #
    #     await self.add_record(new_profile)
    #
    #     return new_profile
    #
    # async def update_profile(self, orm_obj: Profile, data: dict) -> Profile:
    #     data.update({"version": orm_obj.version + 1})
    #     self.update_record(orm_obj, data)
    #     await self.session.flush()
    #
    #     return orm_obj
    #
    # async def get_newcompany_by_id(self, newcompany_id: int) -> NewCompany | None:
    #     return await self._get_newcompany({"id": newcompany_id})
    #
    # async def get_newcompany_by_email(self, newcompany_email: str) -> NewCompany | None:
    #     return await self._get_newcompany({"contact_email": newcompany_email})
    #
    # async def get_newcompanies(self) -> list[NewCompany]:
    #     return await self._get_newcompany(_mode="all")
    #
    # async def _get_newcompany(self, _filtering: dict | None = None, _ordering=None, _mode: str = "one",
    #                           stmt=None) -> NewCompany | list[NewCompany] | None:
    #     return await self._get_stmt_result(_db=NewCompany, _filtering=_filtering, _ordering=_ordering, _mode=_mode,
    #                                        stmt=stmt)
    #
    # async def add_newcompany(self, name, contact_email, billing_country) -> NewCompany | None:
    #     new_company = NewCompany(
    #         name=name,
    #         contact_email=contact_email,
    #         billing_country=billing_country
    #     )
    #
    #     await self.add_record(new_company)
    #     return new_company
    #
    # async def update_newcompany(self, orm_obj: NewCompany, data: dict) -> NewCompany:
    #     self.update_record(orm_obj, data)
    #     await self.session.flush()
    #     return orm_obj
    #
    # async def get_new_robot_by_id(self, robot_id) -> Robot | None:
    #     return await self._get_new_robot({"id": robot_id})
    #
    # async def get_new_robot_by_head_id(self, head_id) -> Robot | None:
    #     return await self._get_new_robot({"head_id": head_id})
    #
    # async def get_new_robot_by_cognito_id(self, cognito_id) -> Robot | None:
    #     return await self._get_new_robot({"cognito_id": cognito_id})
    #
    # async def _get_new_robot(self, _filtering: dict | None = None, _ordering=None, _mode: str = "one",
    #                          stmt=None) -> Robot | list[Robot] | None:
    #     return await self._get_stmt_result(_db=Robot, _filtering=_filtering, _ordering=_ordering, _mode=_mode,
    #                                        stmt=stmt)
    #
    # async def add_new_robot(self, new_robot_data) -> Robot:
    #     new_robot = Robot(
    #         head_id=new_robot_data.head_id,
    #         body_id=new_robot_data.body_id,
    #         uuid=new_robot_data.uuid,
    #         profile_id=new_robot_data.profile_id,
    #         job_ids=new_robot_data.job_ids,
    #         cognito_id=new_robot_data.cognito_id,
    #     )
    #
    #     await self.add_record(new_robot)
    #
    #     return new_robot
    #
    # async def update_new_robot(self, orm_obj: Robot, data: dict) -> Robot:
    #     self.update_record(orm_obj, data)
    #     await self.session.flush()
    #     return orm_obj
    #
    # async def get_json_by_id(self, json_id: int) -> ConfigJson | None:
    #     return await self._get_json(_filtering={"id": json_id})
    #
    # async def get_rps_conf_json_by_id(self, rps_conf_id: int) -> ConfigJson | None:
    #     rps_conf = await self.get_rps_conf_by_id(rps_conf_id)
    #     if rps_conf is None:
    #         raise NotFoundError(f"rps_conf {rps_conf_id} not found")
    #     return await self.get_json_by_id(rps_conf.json_data_id)
    #
    # async def get_gen_conf_json_by_id(self, gen_conf_id: int) -> ConfigJson | None:
    #     gen_conf = await self.get_gen_conf_by_id(gen_conf_id)
    #     if gen_conf is None:
    #         raise NotFoundError(f"gen_conf {gen_conf_id} not found")
    #     return await self.get_json_by_id(gen_conf.json_data_id)
    #
    # async def get_job_json_by_id(self, job_id: int) -> ConfigJson | None:
    #     job = await self.get_job_by_id(job_id)
    #     if job is None:
    #         raise NotFoundError(f"job {job_id} not found")
    #     return await self.get_json_by_id(job.json_data_id)
    #
    # async def _get_json(self, _filtering: dict | None = None, _ordering=None, _mode: str = "one",
    #                     stmt=None) -> ConfigJson | list[ConfigJson] | None:
    #     return await self._get_stmt_result(_db=ConfigJson, _filtering=_filtering, _ordering=_ordering, _mode=_mode,
    #                                        stmt=stmt)
    #
    # async def add_config_json(self, json_data) -> int:
    #     config_json = ConfigJson(json_data=json_data)
    #     await self.add_record(config_json)
    #     return config_json.id
    #
    # async def update_config_json(self, config_json_id, json_data) -> None:
    #     config_json = await self.get_json_by_id(config_json_id)
    #     config_json.json_data = json_data
    #
    # async def get_job_instance_descriptor_by_job_id(self, job_id: int) -> tuple[Job, ConfigJson, Company]:
    #     stmt = (select(Job, ConfigJson, Company).
    #             join(ConfigJson, ConfigJson.id == Job.json_data_id).
    #             join(User, func.cast(User.cognito_id, String) == Job.cognito_id).
    #             join(Company, Company.company_code == User.company_code).
    #             where(Job.id == job_id))
    #     result = await self.execute(stmt)
    #
    #     res = result.fetchone()
    #     if res is None:
    #         raise NotFoundError(f"job {job_id} not found")
    #
    #     return res
