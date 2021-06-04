from peewee import *

db = MySQLDatabase(None)


class BaseModel(Model):
    class Meta:
        database = db


class USER(BaseModel):
    ID = UUIDField(unique=True)
    studentID = BigIntegerField(primary_key=True)
    tagCount = IntegerField()
    role = SmallIntegerField()
    authCode = CharField(max_length=35)
    info = TextField()
    session = CharField(max_length=35,null=True)
    sessioncreated = TimestampField(null=True)


class VIDEO(BaseModel):
    hash = FixedCharField(max_length=35,primary_key=True)
    info = TextField()
    tagstatus = SmallIntegerField()
    markstatus = SmallIntegerField()
