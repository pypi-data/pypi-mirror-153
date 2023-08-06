"""Database table definitions."""

from piccolo.columns import Date, Integer
from piccolo.engine.sqlite import SQLiteEngine
from piccolo.table import Table

from casper7_plugin_meatball_day.settings import settings

DB = SQLiteEngine(str(settings.meatball_database))


class MeatballDay(Table, db=DB):
    """Stores meatball dates against a user & guild ID."""

    guild_id = Integer()
    user_id = Integer()
    month = Integer()
    day = Integer()


class MeatballChannel(Table, db=DB):
    """Stores the channel to post in for each guild."""

    guild_id = Integer()
    channel_id = Integer()


class MeatballRole(Table, db=DB):
    """Stores the role to assign on meatball day for each guild."""

    guild_id = Integer()
    role_id = Integer()


class MeatballRoleAssignment(Table, db=DB):
    """Stores people who currently have the role assigned."""

    guild_id = Integer()
    user_id = Integer()
    date = Date()
