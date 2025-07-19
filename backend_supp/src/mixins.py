from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, declared_attr
from sqlalchemy import Integer, String


class BaseTablenameMixin:
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class BaseModelMixin(BaseTablenameMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    @property
    def pk_column(self) -> str:
        return f"{self.__tablename__}.id"
