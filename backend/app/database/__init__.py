from sqlalchemy import ARRAY, String, Text, DateTime, Boolean, Integer, SmallInteger, Float, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from datetime import datetime, timezone

from config import settings
from custom_types import Gender

engine = create_async_engine(settings.DB_URL, echo=False, pool_size=settings.DB_POOL_SIZE)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 't_user'

    id: Mapped[str] = mapped_column(String(60), primary_key=True)
    username: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, comment="email_address")
    # email_validated: Mapped[bool] = mapped_column(Boolean, default=False)
    authority_level: Mapped[int] = mapped_column(SmallInteger, default=settings.USER_DEFAULT_AUTHORITY_CODE)
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=True, insert_default=None)
    base_info: Mapped["UserBaseInfo"] = relationship(back_populates="user", cascade="all, delete")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True,
                                                 insert_default=datetime.now(settings.CONST.TIMEZONE))
    update_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True,
                                                      onupdate=datetime.now(settings.CONST.TIMEZONE))

    @property
    def is_active(self) -> bool:
        return self.authority_level == settings.USER_INACTIVE_AUTHORITY_CODE
    

class UserAuthProvider(Base):
    __tablename__ = 't_user_auth_provider'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("t_user.id", ondelete="CASCADE"), nullable=True)
    provider: Mapped[str] = mapped_column(String(64), nullable=False)
    provider_id: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True,
                                                 insert_default=datetime.now(settings.CONST.TIMEZONE))
    update_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True,
                                                      onupdate=datetime.now(settings.CONST.TIMEZONE))


class UserBaseInfo(Base):
    __tablename__ = 't_user_base_info'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nickname: Mapped[str] = mapped_column(String(64), nullable=True)
    gender: Mapped[Gender] = mapped_column(String(64), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(64), nullable=True)
    org_name: Mapped[str] = mapped_column(String(64), nullable=True)
    post_number: Mapped[str] = mapped_column(String(64), nullable=True)
    city_id: Mapped[int] = mapped_column(Integer, nullable=True)
    district_id: Mapped[int] = mapped_column(Integer, nullable=True)
    address: Mapped[str] = mapped_column(String(128), nullable=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("t_user.id", ondelete="CASCADE"), nullable=True)
    user: Mapped["User"] = relationship(back_populates="base_info", passive_deletes=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True,
                                                  insert_default=datetime.now(settings.CONST.TIMEZONE))
    update_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True,
                                                      onupdate=datetime.now(settings.CONST.TIMEZONE))


class Quota(Base):
    __tablename__ = "t_quota"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(60), nullable=False)
    total_quota: Mapped[int] = mapped_column(Integer)
    used_quota: Mapped[int] = mapped_column(Integer)
    last_reset: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True,
                                                  insert_default=datetime.now(settings.CONST.TIMEZONE))
    update_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True,
                                                      onupdate=datetime.now(settings.CONST.TIMEZONE))

    @property
    def left_quota(self) -> int:
        return self.total_quota - self.used_quota

    @property
    def quota_avaliable(self) -> bool:
        return self.left_quota > 0


class Conversation(Base):
    __tablename__ = "t_conversation"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(60), nullable=False)
    closed: Mapped[bool] = mapped_column(Boolean, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True,
                                                  insert_default=datetime.now(settings.CONST.TIMEZONE))
    update_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True,
                                                      onupdate=datetime.now(settings.CONST.TIMEZONE))


class Message(Base):
    __tablename__ = "t_message"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(Text, nullable=True)
    role: Mapped[str] = mapped_column(String(64), nullable=True)
    conversation_id: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True,
                                                  insert_default=datetime.now(settings.CONST.TIMEZONE))
    update_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True,
                                                      onupdate=datetime.now(settings.CONST.TIMEZONE))


class Mountain(Base):
    __tablename__ = "t_mountain"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), nullable=True)
    level: Mapped[int] = mapped_column(Integer, nullable=True)
    province: Mapped[str] = mapped_column(String(64), nullable=True)
    city: Mapped[str] = mapped_column(String(64), nullable=True)
    address: Mapped[str] = mapped_column(String(1000), nullable=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True,
                                                  insert_default=datetime.now(settings.CONST.TIMEZONE))
    update_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True,
                                                      onupdate=datetime.now(settings.CONST.TIMEZONE))


class TourCourse(Base):
    __tablename__ = "t_tour_course"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    mountain_id: Mapped[int] = mapped_column(Integer, nullable=True)
    course_name: Mapped[str] = mapped_column(String(64), nullable=True)
    course_distance: Mapped[int] = mapped_column(Integer, nullable=True)
    course_duration: Mapped[int] = mapped_column(Integer, nullable=True)
    course_difficulty: Mapped[int] = mapped_column(Integer, nullable=True)
    

class Tour(Base):
    __tablename__ = "t_tour"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), nullable=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("t_user.id", ondelete="CASCADE"), nullable=True)
    tour_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    mountain_id: Mapped[int] = mapped_column(Integer, nullable=True)
    tour_up_duration: Mapped[int] = mapped_column(Integer, nullable=True)
    tour_up_course_id: Mapped[int] = mapped_column(Integer, nullable=True)
    tour_down_duration: Mapped[int] = mapped_column(Integer, nullable=True)
    tour_down_course_id: Mapped[int] = mapped_column(Integer, nullable=True)
    tour_distance: Mapped[int] = mapped_column(Integer, nullable=True)
    tour_difficulty: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True,
                                                  insert_default=datetime.now(settings.CONST.TIMEZONE))
    update_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True,
                                                      onupdate=datetime.now(settings.CONST.TIMEZONE))

