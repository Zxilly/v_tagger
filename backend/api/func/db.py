from peewee import *

db_proxy = DatabaseProxy()


class BaseModel(Model):
    class Meta:
        database = db_proxy


class USER(BaseModel):
    ID: UUIDField(unique=True)
    studentID: BigIntegerField(primary_key=True)
    tagCount: IntegerField()
    role: SmallIntegerField()
    authCode: CharField(max_length=35)
    info: TextField()


class VIDEO(BaseModel):
    hash: FixedCharField(max_length=35)
    tagger: TextField()  # json格式，存 UUID list
    info: TextField()
