import os
from flask import Flask, request, render_template
from models import db
from routes import *
from flask_restful import Api, Resource

app = Flask(__name__)

if __name__ == '__main__':
    api = Api(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///variant9.db'

    db.init_app(app)
    with app.app_context():
        db.create_all()

    api.add_resource(VideoResource, '/videos/<int:video_id>')
    api.add_resource(VideoListResource, '/videos')
    api.add_resource(ChannelListResource, '/channels')

    app.run(debug=True)

#app = Flask(__name__)
#api = Api(app)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///variant9.db'
#db = SQLAlchemy(app)

#api.add_resource(VideoResource, '/videos/<int:video_id>')
#api.add_resource(VideoListResource, '/videos')
#api.add_resource(ChannelListResource, '/channels')

#if __name__ == '__main__':
    #app.run(debug=True)