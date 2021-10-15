import string
import enum
import random
from enum import auto
from sqlalchemy import Column, types, UniqueConstraint, Enum
from sqlalchemy.ext.declarative import declarative_base
from ckan.model.meta import metadata

Base = declarative_base(metadata=metadata)


class ObjectType(enum.Enum):
    DATASET = auto()
    RESOURCE = auto()


def _generate_random_string(length=8):
    # taken from https://bit.ly/3nxGSMo
    alphanumeric_chars = string.ascii_lowercase + string.digits
    return ''.join(
        random.SystemRandom().choice(alphanumeric_chars)
        for _ in range(length)
    )


class ShortUrls(Base):
    """
    Stores a short_url pointing to a specific dataset or resource
    """
    __tablename__ = 'short_url'

    id = Column(types.Integer, primary_key=True, nullable=False)
    code = Column(
        types.UnicodeText, nullable=False,
        default=_generate_random_string()
    )
    object_type = Column(ObjectType, nullable=False)
    object_id = Column(types.Integer, nullable=False)

    UniqueConstraint('code')
    UniqueConstraint('object_type', 'object_id')

    def to_dict(self):
        output = self.__dict__.copy()
        output.pop('_sa_instance_state')
        return output


def init_tables():
    ShortUrls.__table__.create()


def tables_exists():
    return ShortUrls.__table__.exists()
