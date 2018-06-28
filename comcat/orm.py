"""Object relational mappings."""

from peewee import PrimaryKeyField

from peeweeplus import MySQLDatabase, JSONModel, UUID4Field, Argon2Field


DATABASE = MySQLDatabase.from_config(CONFIG['db'])


class _ComCatModel(JSONModel):
    """Basic comcat model."""
    
    class Meta:
        database = DATABASE
        schema = database.schema
    
    id = PrimaryKeyField()
    
    
class ComCatAccount(_ComCatModel):
    """A ComCat account."""
    
    uuid = UUID4Field()
    passwd = Argon2Field()
