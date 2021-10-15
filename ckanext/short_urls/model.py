import enum
from enum import auto
from sqlalchemy import Column, types, UniqueConstraint, Enum
from sqlalchemy.ext.declarative import declarative_base
from ckan.model.meta import metadata

Base = declarative_base(metadata=metadata)


class ObjectType(enum.Enum):
    DATASET = auto()
    RESOURCE = auto()


class ShortUrl(Base):
    """
    Stores a short_url pointing to a specific dataset or resource
    """
    __tablename__ = 'short_url'

    id = Column(types.Integer, primary_key=True, nullable=False)
    code = Column(types.UnicodeText, nullable=False)
    object_type = Column(ObjectType, nullable=False)
    object_id = Column(types.Integer, nullable=False)

    UniqueConstraint('code')
    UniqueConstraint('object_type', 'object_id')

    def to_dict(self):
        output = self.__dict__.copy()
        output.pop('_sa_instance_state')
        return output


def init_tables():
    ShortUrl.__table__.create()


def tables_exists():
    return ShortUrl.__table__.exists()
