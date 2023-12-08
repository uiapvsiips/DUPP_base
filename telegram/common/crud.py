from datetime import datetime, timedelta

from sqlalchemy import select, update, func, desc, ScalarResult, and_
from sqlalchemy.orm import selectinload

from db.engines.async_engine import db_helper
from db.models import User, Utb, Photo


async def get_user_by_tg_id(tg_user):
    async with db_helper.session_factory() as session:
        stmt = select(User).where(User.tgid == tg_user.id)
        user = await session.scalar(stmt)
        return user


async def get_user_by_uuid(uuid):
    async with db_helper.session_factory() as session:
        stmt = select(User).where(User.tg_confirm_guid == uuid)
        user = await session.scalar(stmt)
        return user


async def update_any_obj(obj):
    async with db_helper.session_factory() as session:
        stmt = update(obj.__class__).where(obj.__class__.id == obj.id).values(obj.dict())
        await session.execute(stmt)
        await session.commit()


async def get_data_by_column_and_value(column_name, value):
    async with db_helper.session_factory() as session:
        if column_name == 'car_going_date':
            next_day = value + timedelta(days=1)
            value: datetime
            # f'{value.strftime("%Y-%m-%d")}'
            # f'{next_day.strftime("%Y-%m-%d")}'
            stmt = select(Utb).where(
                (Utb.__table__.c[column_name] > value) &
                (Utb.__table__.c[column_name] < next_day)
            ).options(
                selectinload(Utb.add_by_user),
                selectinload(
                    Utb.kr_by_user)).order_by(
                desc('id')).order_by(desc(Utb.__table__.c[column_name]))
        else:
            stmt = select(Utb).where(func.upper(
                Utb.__table__.c[column_name]).like(f'%{value.upper()}%')).options(selectinload(Utb.add_by_user),
                                                                                  selectinload(
                                                                                      Utb.kr_by_user)).order_by(
                desc('id')).order_by(desc(Utb.__table__.c[column_name]))
        results = await session.scalars(stmt)
        results: ScalarResult
        return results.all()


async def get_photos_by_utb_id(utb_id):
    async with db_helper.session_factory() as session:
        stmt = select(Photo).where(Photo.utb_id == utb_id)
        photos = await session.scalars(stmt)
        return photos.all()


async def get_all_executors():
    async with db_helper.session_factory() as session:
        stmt = select(Utb.executor).group_by(Utb.executor)
        executors = await session.scalars(stmt)
        return executors.all()
