from sqlalchemy import ARRAY, String, Text, DateTime, Boolean, Integer, SmallInteger, Float, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from datetime import datetime, timezone

from config import settings

engine = create_async_engine(settings.DB_URL, echo=False, pool_size=settings.DB_POOL_SIZE)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 't_user'

    user_guid: Mapped[str] = mapped_column(String(64), primary_key=True)
    username: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, comment="email_address")
    authority_level: Mapped[int] = mapped_column(SmallInteger, default=4)
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=True)
    base_info: Mapped["UserBaseInfo"] = relationship(back_populates="user", cascade="all, delete")
    estate_info: Mapped["UserEstateInfo"] = relationship(back_populates="user", cascade="all, delete")
    insert_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True,
                                                      insert_default=datetime.now(timezone.utc))
    update_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True,
                                                      onupdate=datetime.now(timezone.utc))


class UserBaseInfo(Base):
    __tablename__ = 't_user_base_info'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nickname: Mapped[str] = mapped_column(String(64), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(64), nullable=True)
    org_name: Mapped[str] = mapped_column(String(64), nullable=True)
    post_number: Mapped[str] = mapped_column(String(64), nullable=True)
    city_id: Mapped[int] = mapped_column(Integer, nullable=True)
    district_id: Mapped[int] = mapped_column(Integer, nullable=True)
    address: Mapped[str] = mapped_column(String(128), nullable=True)
    user_guid: Mapped[str] = mapped_column(ForeignKey("t_user.user_guid", ondelete="CASCADE"), nullable=True)
    user: Mapped["User"] = relationship(back_populates="base_info", passive_deletes=True)
    insert_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True,
                                                      insert_default=datetime.now(timezone.utc))
    update_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True,
                                                      onupdate=datetime.now(timezone.utc))


class UserEstateInfo(Base):
    __tablename__ = 't_user_estate_info'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    faved_estates: Mapped[list[int]] = mapped_column(ARRAY(Integer), insert_default=[])
    viewed_estates: Mapped[list[int]] = mapped_column(ARRAY(Integer), insert_default=[])
    query_records: Mapped[list[int]] = mapped_column(ARRAY(Integer), insert_default=[])
    last_search_criteria: Mapped[dict] = mapped_column(JSONB, nullable=True)
    user_guid: Mapped[str] = mapped_column(ForeignKey("t_user.user_guid", ondelete="CASCADE"), nullable=True)
    user: Mapped["User"] = relationship(back_populates="base_info", passive_deletes=True)
    insert_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True,
                                                      insert_default=datetime.now(timezone.utc))
    update_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True,
                                                      onupdate=datetime.now(timezone.utc))


class QueryRecord(Base):
    __tablename__ = 't_query_record'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    query_type: Mapped[str] = mapped_column(String(64), nullable=False)
    first_name_kana: Mapped[str] = mapped_column(String(64), nullable=False)
    last_name_kana: Mapped[str] = mapped_column(String(64), nullable=False)
    first_name_kanji: Mapped[str] = mapped_column(String(64), nullable=False)
    last_name_kanji: Mapped[str] = mapped_column(String(64), nullable=False)
    email: Mapped[str] = mapped_column(String(64), nullable=False)
    phone: Mapped[str] = mapped_column(String(64), nullable=False)
    contact_type: Mapped[str] = mapped_column(String(64), nullable=False)
    query_content: Mapped[str] = mapped_column(Text, nullable=False)

    QUERY_TYPE = {
        'sell': '無料査定依頼',
        'rent': '貸主様相談',
        'any': 'お住いの相談',
        'empty': '最新の空室状況を知りたい',
        'look': '実際に見学したい'
    }

    CONTACT_TYPE = {
        'email': 'メール連絡希望',
        'phone': '電話連絡希望',
        'any': '両方OK'
    }


class City(Base):
    __tablename__ = 't_city'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column(String(64))


class District(Base):
    __tablename__ = 't_district'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column(String(64))


class TrainRoute(Base):
    __tablename__ = 't_train_route'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column(String(64))


class Station(Base):
    __tablename__ = 't_station'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column(String(64))


class Layout(Base):
    __tablename__ = 't_layout'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column(String(64))


class HouseSellNewOne(Base):
    __tablename__ = "t_house_sell_new_one"

    # common attribute
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    recommend_level: Mapped[int] = mapped_column(Integer, insert_default=1)  # 1-5
    sold: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    deleted: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    name: Mapped[str] = mapped_column(String(255))
    city_id: Mapped[int] = mapped_column(Integer)
    district_id: Mapped[int] = mapped_column(Integer)
    address: Mapped[str] = mapped_column(String(255))
    train_route1_id: Mapped[int] = mapped_column(Integer)
    station1_id: Mapped[int] = mapped_column(Integer)
    station_time1: Mapped[int] = mapped_column(Integer)
    train_route2_id: Mapped[int] = mapped_column(Integer, nullable=True)
    station2_id: Mapped[int] = mapped_column(Integer, nullable=True)
    station_time2: Mapped[int] = mapped_column(Integer, nullable=True)
    construction_company: Mapped[str] = mapped_column(String(255))
    completion_date: Mapped[str] = mapped_column(String(255))  # 完工时间
    move_in_date: Mapped[str] = mapped_column(String(255))  # 入居時期
    visit_schedule: Mapped[str] = mapped_column(String(255), nullable=True)
    information_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True,
                                                       insert_default=datetime.now(timezone.utc))
    layout_id: Mapped[int] = mapped_column(Integer)
    layout_detail: Mapped[str] = mapped_column(String(255), nullable=True)
    house_facing: Mapped[str] = mapped_column(String(255), nullable=True)  # 朝向
    land_usage_type: Mapped[str] = mapped_column(String(255), nullable=True)  # 用地类型
    land_category: Mapped[str] = mapped_column(String(255), nullable=True)  # 地目
    land_ownership: Mapped[str] = mapped_column(String(255), nullable=True)
    management_type: Mapped[str] = mapped_column(String(255), nullable=True)
    house_struction: Mapped[str] = mapped_column(String(255), nullable=True)
    main_pic_url: Mapped[str] = mapped_column(String(255), nullable=True)
    layout_pic_url: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_1: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_2: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_3: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_4: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_5: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_6: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_7: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_8: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_9: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_10: Mapped[str] = mapped_column(String(255), nullable=True)
    google_map_url: Mapped[str] = mapped_column(String(255), nullable=True)
    brief_title: Mapped[str] = mapped_column(Text, nullable=True)
    brief_desc: Mapped[str] = mapped_column(Text, nullable=True)
    bullet_point_1: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_2: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_3: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_4: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_5: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_6: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_7: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_8: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_9: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_10: Mapped[str] = mapped_column(String(255), nullable=True)

    # no-common info
    land_area: Mapped[float] = mapped_column(Float, nullable=True)
    building_area: Mapped[float] = mapped_column(Float, nullable=True)
    total_building_area: Mapped[float] = mapped_column(Float, nullable=True)
    building_coverage_ratio: Mapped[str] = mapped_column(String(255), nullable=True)
    private_road: Mapped[str] = mapped_column(String(255), nullable=True)

    parking_lot: Mapped[str] = mapped_column(String(255), insert_default='不明')
    bicycle_parking_lot: Mapped[str] = mapped_column(String(255), insert_default='不明')
    motorcycle_parking_lot: Mapped[str] = mapped_column(String(255), insert_default='不明')
    mini_motorcycle_parking_lot: Mapped[str] = mapped_column(String(255), insert_default='不明')

    management_fee: Mapped[int] = mapped_column(Integer, nullable=True)
    repair_reserve_gold: Mapped[int] = mapped_column(Integer, nullable=True)
    repair_reserve_fund: Mapped[int] = mapped_column(Integer, nullable=True)
    other_fee: Mapped[str] = mapped_column(String(255), nullable=True)
    selling_price: Mapped[int] = mapped_column(Integer, nullable=True)
    renting_price: Mapped[int] = mapped_column(Integer, nullable=True)
    key_money: Mapped[int] = mapped_column(Integer, nullable=True)
    deposit: Mapped[int] = mapped_column(Integer, nullable=True)
    security_deposit: Mapped[int] = mapped_column(Integer, nullable=True)
    quotation_fee: Mapped[int] = mapped_column(Integer, nullable=True)
    amortization_fee: Mapped[int] = mapped_column(Integer, nullable=True)

    has_indoor_laundry_space: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    is_independent_washroom: Mapped[bool] = mapped_column(Boolean, insert_default=True)
    has_flooring: Mapped[bool] = mapped_column(Boolean, insert_default=True)
    is_furniture_included: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    has_aircon: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    has_underfloor_heating: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    is_separate_bath_and_toilet: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    has_bidet: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    has_bathroom_dryer: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    has_reheating_bath: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    has_dishwasher: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    has_two_more_burners: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    has_system_kitchen: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    has_counter_kitchen: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    has_elevator: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    has_delivery_box: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    has_on_site_trash_space: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    has_private_garden: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    has_city_gas: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    has_propane_gas: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    has_autolock: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    has_intercom_with_monitor: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    has_security_camera: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    is_internet_applicable: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    has_shoes_box: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    has_walk_in_closet: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    has_ih_burners: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    has_roof_balcony: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    has_balcony: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    is_bs_applicable: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    is_cs_applicable: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    has_outside_top: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    has_locker: Mapped[bool] = mapped_column(Boolean, insert_default=False)


class HouseSellOldOne(Base):
    __tablename__ = "t_house_sell_old_one"

    # common attribute
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    recommend_level: Mapped[int] = mapped_column(Integer, insert_default=1)  # 1-5
    sold: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    deleted: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    name: Mapped[str] = mapped_column(String(255))
    city_id: Mapped[int] = mapped_column(Integer)
    district_id: Mapped[int] = mapped_column(Integer)
    address: Mapped[str] = mapped_column(String(255))
    train_route1_id: Mapped[int] = mapped_column(Integer)
    station1_id: Mapped[int] = mapped_column(Integer)
    station_time1: Mapped[int] = mapped_column(Integer)
    train_route2_id: Mapped[int] = mapped_column(Integer, nullable=True)
    station2_id: Mapped[int] = mapped_column(Integer, nullable=True)
    station_time2: Mapped[int] = mapped_column(Integer, nullable=True)
    construction_company: Mapped[str] = mapped_column(String(255))
    completion_date: Mapped[str] = mapped_column(String(255))  # 完工时间
    move_in_date: Mapped[str] = mapped_column(String(255))  # 入居時期
    visit_schedule: Mapped[str] = mapped_column(String(255), nullable=True)
    information_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True,
                                                       insert_default=datetime.now(timezone.utc))
    layout_id: Mapped[int] = mapped_column(Integer)
    layout_detail: Mapped[str] = mapped_column(String(255), nullable=True)
    house_facing: Mapped[str] = mapped_column(String(255), nullable=True)  # 朝向
    land_usage_type: Mapped[str] = mapped_column(String(255), nullable=True)  # 用地类型
    land_category: Mapped[str] = mapped_column(String(255), nullable=True)  # 地目
    land_ownership: Mapped[str] = mapped_column(String(255), nullable=True)
    management_type: Mapped[str] = mapped_column(String(255), nullable=True)
    house_struction: Mapped[str] = mapped_column(String(255), nullable=True)
    main_pic_url: Mapped[str] = mapped_column(String(255), nullable=True)
    layout_pic_url: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_1: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_2: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_3: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_4: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_5: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_6: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_7: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_8: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_9: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_10: Mapped[str] = mapped_column(String(255), nullable=True)
    google_map_url: Mapped[str] = mapped_column(String(255), nullable=True)
    brief_title: Mapped[str] = mapped_column(Text, nullable=True)
    brief_desc: Mapped[str] = mapped_column(Text, nullable=True)
    bullet_point_1: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_2: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_3: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_4: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_5: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_6: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_7: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_8: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_9: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_10: Mapped[str] = mapped_column(String(255), nullable=True)


class HouseSellNewMansion(Base):
    __tablename__ = "t_house_sell_new_mansion"

    # common attribute
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    recommend_level: Mapped[int] = mapped_column(Integer, insert_default=1)  # 1-5
    sold: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    deleted: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    name: Mapped[str] = mapped_column(String(255))
    city_id: Mapped[int] = mapped_column(Integer)
    district_id: Mapped[int] = mapped_column(Integer)
    address: Mapped[str] = mapped_column(String(255))
    train_route1_id: Mapped[int] = mapped_column(Integer)
    station1_id: Mapped[int] = mapped_column(Integer)
    station_time1: Mapped[int] = mapped_column(Integer)
    train_route2_id: Mapped[int] = mapped_column(Integer, nullable=True)
    station2_id: Mapped[int] = mapped_column(Integer, nullable=True)
    station_time2: Mapped[int] = mapped_column(Integer, nullable=True)
    construction_company: Mapped[str] = mapped_column(String(255))
    completion_date: Mapped[str] = mapped_column(String(255))  # 完工时间
    move_in_date: Mapped[str] = mapped_column(String(255))  # 入居時期
    visit_schedule: Mapped[str] = mapped_column(String(255), nullable=True)
    information_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True,
                                                       insert_default=datetime.now(timezone.utc))
    layout_id: Mapped[int] = mapped_column(Integer)
    layout_detail: Mapped[str] = mapped_column(String(255), nullable=True)
    house_facing: Mapped[str] = mapped_column(String(255), nullable=True)  # 朝向
    land_usage_type: Mapped[str] = mapped_column(String(255), nullable=True)  # 用地类型
    land_category: Mapped[str] = mapped_column(String(255), nullable=True)  # 地目
    land_ownership: Mapped[str] = mapped_column(String(255), nullable=True)
    management_type: Mapped[str] = mapped_column(String(255), nullable=True)
    house_struction: Mapped[str] = mapped_column(String(255), nullable=True)
    main_pic_url: Mapped[str] = mapped_column(String(255), nullable=True)
    layout_pic_url: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_1: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_2: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_3: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_4: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_5: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_6: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_7: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_8: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_9: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_10: Mapped[str] = mapped_column(String(255), nullable=True)
    google_map_url: Mapped[str] = mapped_column(String(255), nullable=True)
    brief_title: Mapped[str] = mapped_column(Text, nullable=True)
    brief_desc: Mapped[str] = mapped_column(Text, nullable=True)
    bullet_point_1: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_2: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_3: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_4: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_5: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_6: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_7: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_8: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_9: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_10: Mapped[str] = mapped_column(String(255), nullable=True)


class HouseSellOldMansion(Base):
    __tablename__ = "t_house_sell_old_mansion"

    # common attribute
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    recommend_level: Mapped[int] = mapped_column(Integer, insert_default=1)  # 1-5
    sold: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    deleted: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    name: Mapped[str] = mapped_column(String(255))
    city_id: Mapped[int] = mapped_column(Integer)
    district_id: Mapped[int] = mapped_column(Integer)
    address: Mapped[str] = mapped_column(String(255))
    train_route1_id: Mapped[int] = mapped_column(Integer)
    station1_id: Mapped[int] = mapped_column(Integer)
    station_time1: Mapped[int] = mapped_column(Integer)
    train_route2_id: Mapped[int] = mapped_column(Integer, nullable=True)
    station2_id: Mapped[int] = mapped_column(Integer, nullable=True)
    station_time2: Mapped[int] = mapped_column(Integer, nullable=True)
    construction_company: Mapped[str] = mapped_column(String(255))
    completion_date: Mapped[str] = mapped_column(String(255))  # 完工时间
    move_in_date: Mapped[str] = mapped_column(String(255))  # 入居時期
    visit_schedule: Mapped[str] = mapped_column(String(255), nullable=True)
    information_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True,
                                                       insert_default=datetime.now(timezone.utc))
    layout_id: Mapped[int] = mapped_column(Integer)
    layout_detail: Mapped[str] = mapped_column(String(255), nullable=True)
    house_facing: Mapped[str] = mapped_column(String(255), nullable=True)  # 朝向
    land_usage_type: Mapped[str] = mapped_column(String(255), nullable=True)  # 用地类型
    land_category: Mapped[str] = mapped_column(String(255), nullable=True)  # 地目
    land_ownership: Mapped[str] = mapped_column(String(255), nullable=True)
    management_type: Mapped[str] = mapped_column(String(255), nullable=True)
    house_struction: Mapped[str] = mapped_column(String(255), nullable=True)
    main_pic_url: Mapped[str] = mapped_column(String(255), nullable=True)
    layout_pic_url: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_1: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_2: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_3: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_4: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_5: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_6: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_7: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_8: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_9: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_10: Mapped[str] = mapped_column(String(255), nullable=True)
    google_map_url: Mapped[str] = mapped_column(String(255), nullable=True)
    brief_title: Mapped[str] = mapped_column(Text, nullable=True)
    brief_desc: Mapped[str] = mapped_column(Text, nullable=True)
    bullet_point_1: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_2: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_3: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_4: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_5: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_6: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_7: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_8: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_9: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_10: Mapped[str] = mapped_column(String(255), nullable=True)


class HouseRentOne(Base):
    __tablename__ = "t_house_rent_one"

    # common attribute
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    recommend_level: Mapped[int] = mapped_column(Integer, insert_default=1)  # 1-5
    sold: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    deleted: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    name: Mapped[str] = mapped_column(String(255))
    city_id: Mapped[int] = mapped_column(Integer)
    district_id: Mapped[int] = mapped_column(Integer)
    address: Mapped[str] = mapped_column(String(255))
    train_route1_id: Mapped[int] = mapped_column(Integer)
    station1_id: Mapped[int] = mapped_column(Integer)
    station_time1: Mapped[int] = mapped_column(Integer)
    train_route2_id: Mapped[int] = mapped_column(Integer, nullable=True)
    station2_id: Mapped[int] = mapped_column(Integer, nullable=True)
    station_time2: Mapped[int] = mapped_column(Integer, nullable=True)
    construction_company: Mapped[str] = mapped_column(String(255))
    completion_date: Mapped[str] = mapped_column(String(255))  # 完工时间
    move_in_date: Mapped[str] = mapped_column(String(255))  # 入居時期
    visit_schedule: Mapped[str] = mapped_column(String(255), nullable=True)
    information_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True,
                                                       insert_default=datetime.now(timezone.utc))
    layout_id: Mapped[int] = mapped_column(Integer)
    layout_detail: Mapped[str] = mapped_column(String(255), nullable=True)
    house_facing: Mapped[str] = mapped_column(String(255), nullable=True)  # 朝向
    land_usage_type: Mapped[str] = mapped_column(String(255), nullable=True)  # 用地类型
    land_category: Mapped[str] = mapped_column(String(255), nullable=True)  # 地目
    land_ownership: Mapped[str] = mapped_column(String(255), nullable=True)
    management_type: Mapped[str] = mapped_column(String(255), nullable=True)
    house_struction: Mapped[str] = mapped_column(String(255), nullable=True)
    main_pic_url: Mapped[str] = mapped_column(String(255), nullable=True)
    layout_pic_url: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_1: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_2: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_3: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_4: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_5: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_6: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_7: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_8: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_9: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_10: Mapped[str] = mapped_column(String(255), nullable=True)
    google_map_url: Mapped[str] = mapped_column(String(255), nullable=True)
    brief_title: Mapped[str] = mapped_column(Text, nullable=True)
    brief_desc: Mapped[str] = mapped_column(Text, nullable=True)
    bullet_point_1: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_2: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_3: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_4: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_5: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_6: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_7: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_8: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_9: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_10: Mapped[str] = mapped_column(String(255), nullable=True)


class HouseRentMansion(Base):
    __tablename__ = "t_house_rent_mansion"

    # common attribute
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    recommend_level: Mapped[int] = mapped_column(Integer, insert_default=1)  # 1-5
    sold: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    deleted: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    name: Mapped[str] = mapped_column(String(255))
    city_id: Mapped[int] = mapped_column(Integer)
    district_id: Mapped[int] = mapped_column(Integer)
    address: Mapped[str] = mapped_column(String(255))
    train_route1_id: Mapped[int] = mapped_column(Integer)
    station1_id: Mapped[int] = mapped_column(Integer)
    station_time1: Mapped[int] = mapped_column(Integer)
    train_route2_id: Mapped[int] = mapped_column(Integer, nullable=True)
    station2_id: Mapped[int] = mapped_column(Integer, nullable=True)
    station_time2: Mapped[int] = mapped_column(Integer, nullable=True)
    construction_company: Mapped[str] = mapped_column(String(255))
    completion_date: Mapped[str] = mapped_column(String(255))  # 完工时间
    move_in_date: Mapped[str] = mapped_column(String(255))  # 入居時期
    visit_schedule: Mapped[str] = mapped_column(String(255), nullable=True)
    information_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True,
                                                       insert_default=datetime.now(timezone.utc))
    layout_id: Mapped[int] = mapped_column(Integer)
    layout_detail: Mapped[str] = mapped_column(String(255), nullable=True)
    house_facing: Mapped[str] = mapped_column(String(255), nullable=True)  # 朝向
    land_usage_type: Mapped[str] = mapped_column(String(255), nullable=True)  # 用地类型
    land_category: Mapped[str] = mapped_column(String(255), nullable=True)  # 地目
    land_ownership: Mapped[str] = mapped_column(String(255), nullable=True)
    management_type: Mapped[str] = mapped_column(String(255), nullable=True)
    house_struction: Mapped[str] = mapped_column(String(255), nullable=True)
    main_pic_url: Mapped[str] = mapped_column(String(255), nullable=True)
    layout_pic_url: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_1: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_2: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_3: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_4: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_5: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_6: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_7: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_8: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_9: Mapped[str] = mapped_column(String(255), nullable=True)
    other_image_10: Mapped[str] = mapped_column(String(255), nullable=True)
    google_map_url: Mapped[str] = mapped_column(String(255), nullable=True)
    brief_title: Mapped[str] = mapped_column(Text, nullable=True)
    brief_desc: Mapped[str] = mapped_column(Text, nullable=True)
    bullet_point_1: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_2: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_3: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_4: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_5: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_6: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_7: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_8: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_9: Mapped[str] = mapped_column(String(255), nullable=True)
    bullet_point_10: Mapped[str] = mapped_column(String(255), nullable=True)


# class House(Base):
#     NEW = (
#         ('y', '新築'),
#         ('n', '中古'),
#     )
#     HOUSE_TYPE = (
#         ('mansion', 'マンション'),
#         ('one', '一戸建て'),
#         ('land', '土地'),
#         ('parking', '駐車場'),
#     )
#     MODE = (
#         ('rent', '借りる'),
#         ('sell', '買う'),
#     )
#     HOUSE_FACING = (
#         ('東', '東'),
#         ('西', '西'),
#         ('南', '南'),
#         ('北', '北'),
#         ('西北', '西北'),
#         ('東北', '東北'),
#         ('西南', '西南'),
#         ('東南', '東南'),
#     )
#
#     LAND_USAGE_TYPE = (
#         ('商業地域', '商業地域'),
#         ('工業地域', '工業地域'),
#         ('第一種低層住居専用地域', '第一種低層住居専用地域'),
#         ('第二種低層住居専用地域', '第二種低層住居専用地域'),
#         ('第一種中高層住居専用地域', '第一種中高層住居専用地域'),
#         ('第二種中高層住居専用地域', '第二種中高層住居専用地域'),
#         ('第一種住居地域', '第一種住居地域'),
#         ('第二種住居地域', '第二種住居地域'),
#         ('準住居地域', '準住居地域'),
#         ('近隣商業地域', '近隣商業地域'),
#         ('準工業地域', '準工業地域'),
#         ('工業専用地域', '工業専用地域'),
#     )
#
#     LAND_CATEGORY = (
#         ('田', '田'),
#         ('畑', '畑'),
#         ('宅地', '宅地'),
#         ('山林', '山林'),
#         ('牧場', '牧場'),
#     )
#
#     LAND_OWNERSHIP = (
#         ('所有権', '所有権'),
#         ('定期借地権', '定期借地権'),
#     )
#
#     HOUSE_STRUCTION = (
#         ('鉄筋コンクリート', '鉄筋コンクリート'),
#         ('鉄骨', '鉄骨'),
#         ('木造', '木造'),
#     )
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
#     recommend_level: Mapped[int] = mapped_column(Integer, insert_default=1)  # 1-5
#     rented: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     sold: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     deleted: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     name: Mapped[str] = mapped_column(String(255))
#     house_type: Mapped[str] = mapped_column(String(255), nullable=True)  # HOUSE_TYPE
#     new: Mapped[str] = mapped_column(String(255), nullable=True)  # NEW
#     mode: Mapped[str] = mapped_column(String(255), nullable=True)  # MODE
#     main_pic_url: Mapped[str] = mapped_column(String(255), nullable=True)
#     layout_pic_url: Mapped[str] = mapped_column(String(255), nullable=True)
#     other_image_1: Mapped[str] = mapped_column(String(255), nullable=True)
#     other_image_2: Mapped[str] = mapped_column(String(255), nullable=True)
#     other_image_3: Mapped[str] = mapped_column(String(255), nullable=True)
#     other_image_4: Mapped[str] = mapped_column(String(255), nullable=True)
#     other_image_5: Mapped[str] = mapped_column(String(255), nullable=True)
#     other_image_6: Mapped[str] = mapped_column(String(255), nullable=True)
#     other_image_7: Mapped[str] = mapped_column(String(255), nullable=True)
#     other_image_8: Mapped[str] = mapped_column(String(255), nullable=True)
#     other_image_9: Mapped[str] = mapped_column(String(255), nullable=True)
#     other_image_10: Mapped[str] = mapped_column(String(255), nullable=True)
#     google_map_url: Mapped[str] = mapped_column(String(255), nullable=True)
#     city_id: Mapped[int] = mapped_column(Integer)
#     district_id: Mapped[int] = mapped_column(Integer)
#     address: Mapped[str] = mapped_column(String(255))
#     train_route1_id: Mapped[int] = mapped_column(Integer)
#     station1_id: Mapped[int] = mapped_column(Integer)
#     station_time1: Mapped[int] = mapped_column(Integer)
#     station_time1_bycar: Mapped[int] = mapped_column(Integer, nullable=True)
#     train_route2_id: Mapped[int] = mapped_column(Integer, nullable=True)
#     station2_id: Mapped[int] = mapped_column(Integer, nullable=True)
#     station_time2: Mapped[int] = mapped_column(Integer, nullable=True)
#     station_time2_bycar: Mapped[int] = mapped_column(Integer, nullable=True)
#     train_route3_id: Mapped[int] = mapped_column(Integer, nullable=True)
#     station3_id: Mapped[int] = mapped_column(Integer, nullable=True)
#     station_time3: Mapped[int] = mapped_column(Integer, nullable=True)
#     station_time3_bycar: Mapped[int] = mapped_column(Integer, nullable=True)
#     agent_company: Mapped[str] = mapped_column(String(255))
#     completion_date: Mapped[str] = mapped_column(String(255))  # 完工时间
#     move_in_date: Mapped[str] = mapped_column(String(255))  # 入居時期
#     move_in_date_str: Mapped[str] = mapped_column(String(255), nullable=True)  # 入住时间 字符串说明
#     layout_id: Mapped[int] = mapped_column(Integer)
#     layout_detail: Mapped[str] = mapped_column(String(255), nullable=True)
#     house_facing: Mapped[str] = mapped_column(String(255))  # 朝向
#     land_usage_type: Mapped[str] = mapped_column(String(255))  # 用地类型
#     land_category: Mapped[str] = mapped_column(String(255))  # 地目
#     land_ownership: Mapped[str] = mapped_column(String(255))
#     house_struction: Mapped[str] = mapped_column(String(255))
#     number_of_floors: Mapped[int] = mapped_column(Integer, nullable=True)
#     building_scale: Mapped[int] = mapped_column(Integer, nullable=True)  # 一共多少户
#     total_number_of_floors: Mapped[int] = mapped_column(Integer, nullable=True)
#     parking_lot: Mapped[str] = mapped_column(String(255), insert_default='不明')
#     bicycle_parking_lot: Mapped[str] = mapped_column(String(255), insert_default='不明')
#     motorcycle_parking_lot: Mapped[str] = mapped_column(String(255), insert_default='不明')
#     mini_motorcycle_parking_lot: Mapped[str] = mapped_column(String(255), insert_default='不明')
#     management_type: Mapped[str] = mapped_column(String(255), nullable=True)
#     other_brief: Mapped[str] = mapped_column(String(255), nullable=True)
#     management_fee: Mapped[int] = mapped_column(Integer, nullable=True)
#     management_preparation_fee: Mapped[int] = mapped_column(Integer, nullable=True)
#     repair_reserve_gold: Mapped[int] = mapped_column(Integer, nullable=True)
#     repair_reserve_fund: Mapped[int] = mapped_column(Integer, nullable=True)
#     other_fee: Mapped[str] = mapped_column(String(255), nullable=True)
#     restriction: Mapped[str] = mapped_column(String(255), nullable=True)
#     brief_title: Mapped[str] = mapped_column(Text, nullable=True)
#     brief_desc: Mapped[str] = mapped_column(Text, nullable=True)
#     bullet_point_1: Mapped[str] = mapped_column(String(255), nullable=True)
#     bullet_point_2: Mapped[str] = mapped_column(String(255), nullable=True)
#     bullet_point_3: Mapped[str] = mapped_column(String(255), nullable=True)
#     bullet_point_4: Mapped[str] = mapped_column(String(255), nullable=True)
#     bullet_point_5: Mapped[str] = mapped_column(String(255), nullable=True)
#     bullet_point_6: Mapped[str] = mapped_column(String(255), nullable=True)
#     bullet_point_7: Mapped[str] = mapped_column(String(255), nullable=True)
#     bullet_point_8: Mapped[str] = mapped_column(String(255), nullable=True)
#     bullet_point_9: Mapped[str] = mapped_column(String(255), nullable=True)
#     bullet_point_10: Mapped[str] = mapped_column(String(255), nullable=True)
#     visit_schedule: Mapped[str] = mapped_column(String(255), nullable=True)
#
#     construction_company: Mapped[str] = mapped_column(String(255))
#     information_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True,
#                                                        insert_default=datetime.now(timezone.utc))
#     selling_price: Mapped[int] = mapped_column(Integer, nullable=True)
#     renting_price: Mapped[int] = mapped_column(Integer, nullable=True)
#     exclusive_area: Mapped[float] = mapped_column(Float, nullable=True)
#     balcony_area: Mapped[float] = mapped_column(Float, nullable=True)
#     other_area: Mapped[str] = mapped_column(String(255), nullable=True)
#     land_area: Mapped[float] = mapped_column(Float, nullable=True)
#     building_area: Mapped[float] = mapped_column(Float, nullable=True)
#     total_building_area: Mapped[float] = mapped_column(Float, nullable=True)
#     building_coverage_ratio: Mapped[str] = mapped_column(String(255), nullable=True)
#     floor_area_ratio: Mapped[str] = mapped_column(String(255), nullable=True)
#     private_road: Mapped[str] = mapped_column(String(255), nullable=True)
#     insurance: Mapped[int] = mapped_column(Integer, nullable=True)
#     contract_period: Mapped[str] = mapped_column(String(255), nullable=True)
#     key_money: Mapped[int] = mapped_column(Integer, nullable=True)
#     deposit: Mapped[int] = mapped_column(Integer, nullable=True)
#     security_deposit: Mapped[int] = mapped_column(Integer, nullable=True)
#     quotation_fee: Mapped[int] = mapped_column(Integer, nullable=True)
#     amortization_fee: Mapped[int] = mapped_column(Integer, nullable=True)
#
#     is_reformed: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     is_corner_room: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     is_top_floor: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     has_indoor_laundry_space: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     is_independent_washroom: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     has_flooring: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     is_loft: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     is_furniture_included: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     has_aircon: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     has_underfloor_heating: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     is_separate_bath_and_toilet: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     has_bidet: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     has_bathroom_dryer: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     has_reheating_bath: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     has_dishwasher: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     has_two_more_burners: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     has_system_kitchen: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     has_counter_kitchen: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     has_elevator: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     has_delivery_box: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     has_on_site_trash_space: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     has_private_garden: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     has_city_gas: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     has_propane_gas: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     has_autolock: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     has_intercom_with_monitor: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     has_security_camera: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     is_internet_applicable: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     is_available_for_immediate_move_in: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     is_only_women: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     is_pets_negotiable: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     is_available_for_roomshare: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     has_shoes_box: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     has_walk_in_closet: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     is_no_guarantor_required: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     has_every_floor_trash_space: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     has_ih_burners: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     has_roof_balcony: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     has_balcony: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     is_bs_applicable: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     is_cs_applicable: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     has_outside_top: Mapped[bool] = mapped_column(Boolean, insert_default=False)
#     has_locker: Mapped[bool] = mapped_column(Boolean, insert_default=False)


class HouseUploadRecord(Base):
    __tablename__ = 't_house_upload_record'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_guid: Mapped[str] = mapped_column(String(64))
    upload_file_url: Mapped[str] = mapped_column(String(255))
    insert_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True,
                                                      insert_default=datetime.now(timezone.utc))


class AtbbSellOne(Base):
    __tablename__ = 't_atbb_sell_one'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    faved: Mapped[bool] = mapped_column(Boolean)
    url: Mapped[str] = mapped_column(String(255))
    img: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    price: Mapped[int] = mapped_column(Integer)
    address: Mapped[str] = mapped_column(String(255))
    station: Mapped[str] = mapped_column(String(255))
    area: Mapped[str] = mapped_column(String(64))
    layout: Mapped[str] = mapped_column(String(64))
    city: Mapped[str] = mapped_column(String(64))
    district: Mapped[str] = mapped_column(String(64))
    train_route1: Mapped[str] = mapped_column(String(64))
    station1: Mapped[str] = mapped_column(String(64))
    insert_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True,
                                                      insert_default=datetime.now(timezone.utc))


class AtbbSellMansion(Base):
    __tablename__ = 't_atbb_sell_mansion'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    faved: Mapped[bool] = mapped_column(Boolean)
    url: Mapped[str] = mapped_column(String(255))
    img: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    price: Mapped[int] = mapped_column(Integer)
    address: Mapped[str] = mapped_column(String(255))
    station: Mapped[str] = mapped_column(String(255))
    area: Mapped[str] = mapped_column(String(64))
    layout: Mapped[str] = mapped_column(String(64))
    city: Mapped[str] = mapped_column(String(64))
    district: Mapped[str] = mapped_column(String(64))
    train_route1: Mapped[str] = mapped_column(String(64))
    station1: Mapped[str] = mapped_column(String(64))
    insert_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True,
                                                      insert_default=datetime.now(timezone.utc))


class AtbbRentOne(Base):
    __tablename__ = 't_atbb_rent_one'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    faved: Mapped[bool] = mapped_column(Boolean)
    url: Mapped[str] = mapped_column(String(255))
    img: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    price: Mapped[int] = mapped_column(Integer)
    address: Mapped[str] = mapped_column(String(255))
    station: Mapped[str] = mapped_column(String(255))
    area: Mapped[str] = mapped_column(String(64))
    layout: Mapped[str] = mapped_column(String(64))
    city: Mapped[str] = mapped_column(String(64))
    district: Mapped[str] = mapped_column(String(64))
    train_route1: Mapped[str] = mapped_column(String(64))
    station1: Mapped[str] = mapped_column(String(64))
    insert_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True,
                                                      insert_default=datetime.now(timezone.utc))


class AtbbRentMansion(Base):
    __tablename__ = 't_atbb_rent_mansion'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    faved: Mapped[bool] = mapped_column(Boolean)
    url: Mapped[str] = mapped_column(String(255))
    img: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    price: Mapped[int] = mapped_column(Integer)
    address: Mapped[str] = mapped_column(String(255))
    station: Mapped[str] = mapped_column(String(255))
    area: Mapped[str] = mapped_column(String(64))
    layout: Mapped[str] = mapped_column(String(64))
    city: Mapped[str] = mapped_column(String(64))
    district: Mapped[str] = mapped_column(String(64))
    train_route1: Mapped[str] = mapped_column(String(64))
    station1: Mapped[str] = mapped_column(String(64))
    insert_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True,
                                                      insert_default=datetime.now(timezone.utc))
