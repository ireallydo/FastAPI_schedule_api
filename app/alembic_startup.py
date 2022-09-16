import os
import subprocess
from dotenv import load_dotenv

# TODO
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import create_engine

from sqlalchemy.engine import Connection

from alembic.runtime import migration
from alembic import command, context, config, script, op

load_dotenv()

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = 'localhost'
DB_NAME = os.environ.get("DB_NAME")

# alembic script always needs to work from the same directory with the alembic ini file
# os.chdir('../..')

cfg = config.Config("alembic.ini")

# TODO make asyncengine and rewrite functions with async-await bc we use the same connection for autogenerate

engine = create_engine(
    f"postgresql://"
    f"{DB_USER}:{DB_PASSWORD}@"
    f"{DB_HOST}/{DB_NAME}",
    isolation_level="READ COMMITTED",
    echo="debug",
)


class MigrationOutOfSync(Exception):
    """ Raised when the current statement of the database is out of sync with models and there is no appropriate migration script to apply."""

    def __init__(self, stderr, message=" The database is out of sync with models and there is no appropriate migration script to apply. Please submit a valid migration script to alembic versions directory before deployment. \nEXIT"):
        self.error_msg = stderr
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        catch_err = self.error_msg.find('[alembic.autogenerate.compare]')
        begin_err = self.error_msg.find('ERROR')
        end_err = self.error_msg.find('You may need to')
        error_catch = self.error_msg[catch_err:begin_err-2]
        error_msg = self.error_msg[begin_err:end_err-4]
        return f'\n\nDatabase check results:\n{error_catch} \n{error_msg} \n\n-> {self.message}\n'


def current_head():
    """
    A function returns the number of the latest added revision in the versions directory.
    The latest added revision (head) is not necessary the one applied.
    """
    # alembic versions directory load
    script_ = script.ScriptDirectory.from_config(cfg)
    # get current head
    cur_head = script_.get_current_head()
    return cur_head

def latest_migration_is_applied(connection):
    """
    A function checks if the current applied migration/revision (cur_revision) is the same as the latest added revision (head).
    Returns a tuple (Boolean, current_head_number).
    """
    # check the latest applied revision
    context = migration.MigrationContext.configure(connection)
    cur_revision = context.get_current_revision()
    # get the latest added revision
    cur_head = current_head()
    return (cur_revision == cur_head, cur_head)


def main():
    with engine.begin() as conn:
        # pass made connection to config attributes to be used in env.py
        cfg.attributes['connection'] = conn
        # check if there are migrations which were generated (presumably - manually) but not applied
        (migrations_check, cur_head) = latest_migration_is_applied(conn)
        if not migrations_check:
            # if so, upgrade db to latest migration
            command.upgrade(cfg, revision = cur_head)
            # we assume that the latest migration was made manually and includes everything, so there's no need to autogenerate one more migration, the script may finish
        else:
            # if the head is on the latest migration added, check if db schema has any changes compared to current db, and if it has - exit with 1
            migrations_needed_check = subprocess.run('alembic-autogen-check', capture_output=True)
            stderr = str(migrations_needed_check.stderr)
            return_code = migrations_needed_check.returncode
            if return_code != 0:
                raise MigrationOutOfSync(stderr)


if __name__ == '__main__':
    main()

print ('\nMigrations are finished!\n');
