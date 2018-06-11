from peewee import *

from config import app_config
import datetime

# Connect to a MySQL database on network.
db = MySQLDatabase(app_config["DB_NAME"], user=app_config["DB_USER"], password=app_config["DB_PWD"],
                         host=app_config["DB_HOST"], port=app_config["DB_PORT"], charset='utf8mb4')
db.connect()


class GenderField(Field):
    field_type = 'enum("UNKNOWN", "MALE", "FEMALE", "OTHERS")'

    def db_value(self, value):
        return value + 1

    def python_value(self, value):
        if value == "UNKNOWN":
            return 0
        elif value == "MALE":
            return 1
        elif value == "FEMALE":
            return 2
        elif value == "OTHERS":
            return 3


class User(Model):
    name = CharField(default="")
    display_name = CharField(default="")
    gender = GenderField(null=False)
    signature = TextField(default="")
    tag = CharField(default="")
    avatar_file_name = CharField(default="")
    province = CharField(default="")
    city = CharField(default="")
    is_friend = BooleanField(default="")
    from_group = CharField(default="")
    from_id = CharField(default="")
    created_date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db  # This model uses the "user_info.db" database.


if __name__ == '__main__':
    db.create_tables([User])
    user = User(name="测试", gender=2, is_friend=True)
    user.save()
    db.close()
