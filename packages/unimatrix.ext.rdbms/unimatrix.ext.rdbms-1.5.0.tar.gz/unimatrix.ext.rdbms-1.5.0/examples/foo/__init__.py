# pylint: skip-file
import sqlalchemy
from unimatrix.ext.rdbms import declarative_base


Base, metadata = declarative_base()


class Book(Base):
    __tablename__ = 'books'

    id = sqlalchemy.Column(
        sqlalchemy.BigInteger,
        primary_key=True,
        name='id'
    )

    title = sqlalchemy.Column(
        sqlalchemy.String,
        name='title'
    )
