"""Declares :class:`CommandLine` and the main script entrypoint."""
import importlib
import os
from os.path import abspath
from os.path import dirname
from os.path import join

import ioc.loader
from alembic import config

from unimatrix.ext import rdbms


class CommandLine(config.CommandLine):

    def get_script_location(self, script_location):
        """Return the script location."""
        return script_location\
            or os.getenv('ALEMBIC_SCRIPT_LOCATION')\
            or abspath(dirname(__file__))

    def get_version_locations(self, cfg):
        """Get the ``version_locations`` configuration setting by
        discovering it from the metadata module.
        """
        module = importlib.import_module(
            str.rsplit(cfg.get_main_option('metadata'), '.', 1)[0]
        )
        return abspath(join(dirname(module.__file__), 'migrations'))

    def parse_metadata(self, qualname: str):
        """Normalize the qualified name to the :class:`MetaData`
        objects.
        """
        if qualname.find(':') == -1:
            qualname = f"{qualname}:metadata"
        return str.replace(qualname, ':', '.')

    def main(self, argv=None):
        self.parser.add_argument('--metadata',
            help="The MetaData object(s) to create.",
            required=True,
            type=self.parse_metadata
        )
        self.parser.add_argument('--script-location',
            default=None,
            help="Override the script_location setting."
        )
        connection = rdbms.get('self')
        options = self.parser.parse_args(argv)
        if not hasattr(options, "cmd"):
            self.parser.error("too few arguments")
        else:
            cfg = config.Config()
            cfg.set_main_option(
                'script_location',
                self.get_script_location(options.script_location))
            cfg.set_main_option("sqlalchemy.url", connection.dsn)
            cfg.set_main_option("metadata", options.metadata)
            cfg.set_main_option(
                "version_locations",
                self.get_version_locations(cfg)
            )
            self.run_cmd(cfg, options)


def main(argv=None, prog=None, **kwargs):
    """The console runner function for Alembic."""
    CommandLine(prog=prog).main(argv=argv)


if __name__ == "__main__":
    main()
