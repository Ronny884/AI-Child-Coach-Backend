from __future__ import annotations
import uuid

from typing import TYPE_CHECKING
from logging import getLogger

from sqlalchemy.future import select

from src.data_access.models import Child
from src.data_access.db_connector import db_session

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


logger = getLogger(__name__)


async def get_or_create_child(
        child_id: uuid.UUID,
        thread: str = None,
        additional_instructions: str = None,
        session: AsyncSession = db_session
):
    async with session.begin():
        result = await session.execute(
            select(Child).filter_by(id=child_id)
        )
        existing_child = result.scalar_one_or_none()

        if existing_child:
            return existing_child

        new_child = Child(
            child_id=child_id,
            thread=thread,
            additional_instructions=additional_instructions
        )
        session.add(new_child)
        await session.commit()
        return new_child