"""DataLad demo extension"""

__docformat__ = 'restructuredtext'

import logging
lgr = logging.getLogger('datalad.lgpdextension')

# Defines a datalad command suite.
# This variable must be bound as a setuptools entrypoint
# to be found by datalad
command_suite = (
    # description of the command suite, displayed in cmdline help
    "Demo DataLad command suite",
    [
        # specification of a command, any number of commands can be defined
        (
            # importable module that contains the command implementation
            'datalad_lgpdextension.lgpd_extension',
            # name of the command class implementation in above module
            'LgpdExtension',
            # optional name of the command in the cmdline API
            'lgpd-extension',
            # optional name of the command in the Python API
            'lgpd_extension'
        ),
    ]
)

from datalad import setup_package
from datalad import teardown_package

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
