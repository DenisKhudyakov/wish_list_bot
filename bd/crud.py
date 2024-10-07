from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bd.base import connection
from bd.model import Gift


@connection
async def get_all_gifts(db: AsyncSession):
    result = await db.execute(select(Gift))
    gifts = result.scalars().all()
    return gifts


@connection
async def add_gift(db: AsyncSession, name: str, link: str) -> None:
    gift = Gift(name=name, link=link)
    db.add(gift)
    await db.commit()


@connection
async def reserve_gift(db: AsyncSession, gift_id: int) -> None:
    gift = await db.scalar(select(Gift).filter_by(id=gift_id))
    if gift:
        gift.reserved = True
        await db.commit()


@connection
async def delete_gift(db: AsyncSession, gift_id: int) -> None:
    gift = await db.scalar(select(Gift).filter_by(id=gift_id))
    if gift:
        await db.delete(gift)
        await db.commit()


@connection
async def get_id_gift(db: AsyncSession, gift_id: int):
    gift = await db.scalar(select(Gift).filter_by(id=gift_id))
    return gift
