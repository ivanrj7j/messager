from flask import Flask
from dotenv import load_dotenv
import os
from flask_cors import CORS

from src import socket
from src import main
from src.blueprints import userBlueprint, communityBlueprint
# importing all the modules 

load_dotenv()

SECRET_KEY = os.environ["SECRET_KEY"]
# importing environment variables

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
cors = CORS(app)

socket.init_app(app)
app.register_blueprint(main)
app.register_blueprint(userBlueprint)
app.register_blueprint(communityBlueprint)
# setting up the apps 




if __name__ == '__main__':
    socket.run(app, debug=True)