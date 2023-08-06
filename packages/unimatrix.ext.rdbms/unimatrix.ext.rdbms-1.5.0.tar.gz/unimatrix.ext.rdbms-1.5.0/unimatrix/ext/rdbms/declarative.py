# pylint: skip-file
import importlib

import sqlalchemy.ext.declarative
from sqlalchemy.sql.schema import MetaData
from unimatrix.conf import settings


def declarative_base(cls=None, class_factory=None, settings=None, apps=None): # pragma: no cover
    """Like :func:`sqlalchemy.ext.declarative.declarative_base()`, but
    returns a tuple containing the metadata objects for all applications
    that were specified in :attr:`unimatrix.conf.settings.INSTALLED_APPS`.

    Each application must have a submodule/subpackage named ``orm``, which
    exposed a ``metadata`` attribute.

    The list of installed apps may also be provided using the `apps`
    parameter.

    The resulting list of metadata objects is used to create Alembic
    migration scripts.

    Optionally, the `cls` argument may be provided to use a pre-existing
    declarative base class instead. This allows the :func:`declarative_base`
    function to be used with legacy models.

    By default, :func:`sqlalchemy.ext.declarative.declarative_base()` is
    used to create the base class, but another factory may be specified using
    the `class_factory` argument.
    """
    class_factory = class_factory or sqlalchemy.ext.declarative.declarative_base
    Base = cls or (class_factory)()
    target_metadata = []
    apps = apps or getattr(settings, 'INSTALLED_APPS', [])
    if apps:
        for app_qualname in apps:
            orm_qualname = "%s.orm" % app_qualname
            try:
                orm = importlib.import_module(orm_qualname)
            except ImportError as e:
                # Fail silently - assume that the installed application does
                # not declare an ORM. We do want to catch other ImportError
                # exceptions tho. This is quicky flaky but it works for now.
                if e.args[0] != ("No module named '%s'" %  orm_qualname):
                    raise
                continue
            if isinstance(orm.metadata, MetaData):
                target_metadata.append(orm.metadata)
            elif isinstance(orm.metadata, (list, tuple)):
                target_metadata.extend(orm.metadata)
            else:
                raise TypeError(
                    "%s.metadata is of invalid type." % orm_qualname)

    target_metadata.append(Base.metadata)
    return Base, target_metadata

