"""Database table definitions."""

from piccolo.columns import Date, Integer
from piccolo.table import Table


class MeatballDay(Table):
    """Stores meatball dates against a user & guild ID."""

    guild_id = Integer()
    user_id = Integer()
    month = Integer()
    day = Integer()


class MeatballChannel(Table):
    """Stores the channel to post in for each guild."""

    guild_id = Integer()
    channel_id = Integer()


class MeatballRole(Table):
    """Stores the role to assign on meatball day for each guild."""

    guild_id = Integer()
    role_id = Integer()


class MeatballRoleAssignment(Table):
    """Stores people who currently have the role assigned."""

    guild_id = Integer()
    user_id = Integer()
    date = Date()
