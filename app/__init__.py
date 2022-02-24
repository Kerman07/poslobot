from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

viber = Api(
    BotConfiguration(
        name="Poslobot",
        avatar="http://site.com/avatar.jpg",
        auth_token=os.environ.get("VIBER_AUTH"),
    )
)

from app import routes, models
