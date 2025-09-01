from typing import Any, Dict, Generic, Sequence, Type, TypeVar, Union
from uuid import UUID

from sqlalchemy import and_, delete, select, update
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

    async def get_by(
        self, field: str, value: Any, session: AsyncSession
    ) -> ModelType | None:
        column = getattr(self.model, field, None)

        if not column:
            raise ValueError(f"{field} is not a valid column of {self.model.__name__}")

        query = select(self.model).where(column == value)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_filters(
        self, session: AsyncSession, unique: bool = False, **filters: Any
    ) -> Union[Sequence[ModelType], ModelType, None]:
        conditions = [
            getattr(self.model, field) == value for field, value in filters.items()
        ]

        stmt = select(self.model).where(and_(*conditions))  # type: ignore
        result = await session.execute(stmt)

        if unique:
            return result.scalar_one_or_none()
        else:
            return result.scalars().all()

    async def create(self, obj: ModelType, session: AsyncSession) -> ModelType:
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    async def update(
        self, _id: int, values: Dict[str, Any], session: AsyncSession
    ) -> None:
        query = update(self.model).where(self.model.id == _id).values(**values)  # type: ignore
        await session.execute(query)
        await session.commit()

    async def delete(self, _id: int, session: AsyncSession) -> None:
        query = delete(self.model).where(self.model.id == _id)  # type: ignore
        await session.execute(query)
        await session.commit()
