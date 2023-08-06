import os
import signal
import sys

from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal
from cement.utils import fs
from tinydb import TinyDB

from .controllers.epic import Epic
from .controllers.project import Project
from .core.exc import GitManipulatorError
from .controllers.base import Base


def extend_tinydb(app):
    db_file = app.config.get('gitmanipulator', 'db_file')

    # ensure that we expand the full path
    db_file = fs.abspath(db_file)

    # ensure our parent directory exists
    db_dir = os.path.dirname(db_file)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    app.extend('db', TinyDB(db_file))


# configuration defaults
CONFIG = init_defaults('gitmanipulator')
CONFIG['gitmanipulator']['db_file'] = '~/.gitmanipulator/db.json'


class GitManipulator(App):
    """gitManipulator primary application."""

    class Meta:
        label = 'gitmanipulator'

        # configuration defaults
        config_defaults = CONFIG

        # call sys.exit() on close
        exit_on_close = True

        # load additional framework extensions
        extensions = [
            'yaml',
            'colorlog',
            'jinja2',
        ]

        # configuration handler
        config_handler = 'yaml'

        # configuration file suffix
        config_file_suffix = '.yml'

        # set the log handler
        log_handler = 'colorlog'

        # set the output handler
        output_handler = 'jinja2'

        # register handlers
        handlers = [
            Base,
            Project,
            Epic,
        ]
        hooks = [
            ('post_setup', extend_tinydb),
        ]


class GitManipulatorTest(TestApp, GitManipulator):
    """A sub-class of GitManipulator that is better suited for testing."""

    class Meta:
        label = 'gitmanipulator'


def main():
    def sigint_handler(signal, frame):
        print('KeyboardInterrupt is caught')
        sys.exit(0)

    signal.signal(signal.SIGINT, sigint_handler)

    with GitManipulator() as app:
        try:
            app.run()

        except AssertionError as e:
            print('AssertionError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except GitManipulatorError as e:
            print('GitManipulatorError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print('\n%s' % e)
            app.exit_code = 0


if __name__ == '__main__':
    main()
