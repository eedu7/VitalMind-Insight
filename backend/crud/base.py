from typing import Any, Dict, Generic, Sequence, Type, TypeVar
from uuid import UUID

from sqlalchemy import and_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseCRUD(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model

    async def get_by_id(self, _id: int, session: AsyncSession) -> ModelType | None:
        return await self.get_by(field="id", value=_id, session=session)

    async def get_by_uuid(self, uuid: UUID, session: AsyncSession) -> ModelType | None:
        return await self.get_by(field="uuid", value=uuid, session=session)

    async def get_by(self, field: str, value: Any, session: AsyncSession) -> ModelType | None:
        column = getattr(self.model, field, None)

        if not column:
            raise ValueError(f"{field} is not a valid column of {self.model.__name__}")

        stmt = select(self.model).where(column == value)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_by_filters(
        self,
        session: AsyncSession,
        filters: Dict[str, Any],
        order_by: str | None = None,
        descending: bool = False,
    ) -> Sequence[ModelType]:
        conditions = [getattr(self.model, field) == value for field, value in filters.items()]
        stmt = select(self.model).where(and_(*conditions))  # type: ignore

        if order_by:
            column = getattr(self.model, order_by, None)
            if not column:
                raise ValueError(f"{order_by} is not a valid column of {self.model.__name__}")
            stmt = stmt.order_by(column.desc() if descending else column.asc())

        result = await session.execute(stmt)
        return result.scalars().all()

    async def get_one_by_filters(self, session: AsyncSession, filters: Dict[str, Any]) -> ModelType | None:
        conditions = [getattr(self.model, field) == value for field, value in filters.items()]
        stmt = select(self.model).where(and_(*conditions))  # type: ignore
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, obj: ModelType, session: AsyncSession) -> ModelType:
        session.add(obj)
        await session.commit()
        return obj

    async def update(self, _id: int, values: Dict[str, Any], session: AsyncSession) -> None:
        stmt = update(self.model).where(self.model.id == _id).values(**values)  # type: ignore
        await session.execute(stmt)
        await session.commit()

    async def delete(self, obj: ModelType, session: AsyncSession) -> None:
        await session.delete(obj)
        await session.commit()

    async def update_by_uuid(self, uuid: UUID, values: Dict[str, Any], session: AsyncSession) -> bool:
        stmt = (
            update(self.model)
            .where(self.model.uuid == uuid)  # type: ignore
            .values(**values)
            .execution_options(synchronize_session="fetch")
        )

        result = await session.execute(stmt)
        await session.commit()
        return bool(result.rowcount)  # return True if updated, else False
