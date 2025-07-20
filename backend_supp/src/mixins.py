from sqlalchemy.orm import declared_attr


class BaseTablenameMixin:
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class BaseModelMixin(BaseTablenameMixin):

    @property
    def pk_column(self) -> str:
        return f"{self.__tablename__}.id"
