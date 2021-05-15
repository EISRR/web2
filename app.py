from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///variant9.db'
db = SQLAlchemy(app)

class Channel(db.Model):
    __tablename__ = "channels"
    id = db.Column(db.Integer, primary_key=True)
    channel_name = db.Column(db.String(150))
    date_creation = db.Column(db.String(150))
    subscribers = db.Column(db.Integer)
    videos = db.relationship('Video', backref = 'channel', lazy = True)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, channel_name, date_creation, subscribers):
        self.channel_name = channel_name
        self.date_creation = date_creation
        self.subscribers = subscribers

    def __repr__(self):
        return '' % self.id

class Video(db.Model):
    __tablename__ = "videos"
    id = db.Column(db.Integer, primary_key=True)
    video_name = db.Column(db.String(150))
    date_publication = db.Column(db.String(150))
    weight = db.Column(db.Integer)
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'), nullable = False)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, video_name, date_publication, weight, channel_id):
        self.video_name = video_name
        self.date_publication = date_publication
        self.weight = weight
        self.channel_id = channel_id

    def __repr__(self):
        return '' % self.id

db.create_all()

#__________________________SCHEMA______________________________

class VideoSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Video
        sqla_session = db.session
        include_fk = True

    id = fields.Number(dump_only = True)
    video_name = fields.String(required = True)
    date_publication = fields.String(required = True)
    weight = fields.Number(required = False)
    channel = fields.Nested(lambda: ChannelSchema(only = ("id", "channel_name", "date_creation", "subscribers")))

class ChannelSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Channel
        sqla_session = db.session
        include_relationships = True

    id = fields.Number(dump_only = True)
    channel_name = fields.String(required = True)
    date_creation = fields.String(required = True)
    subscribers = fields.Number(required = True)
    videos = fields.List(fields.Nested(VideoSchema(exclude = ("channel"))))

#____________________POST,GET,GET,PUT,DELETE___________________

@app.route('/channels', methods = ['POST'])
def create_channel():
    data = request.get_json()
    channel_schema = ChannelSchema()
    channel = channel_schema.load(data)
    result = channel_schema.dump(channel.create())
    return make_response(jsonify({"channel": result}),200)

@app.route('/channels', methods = ['GET'])
def get_channels():
    get_channels = Channel.query.all()
    channel_schema = ChannelSchema(many = True)
    channels = channel_schema.dump(get_channels)
    return make_response(jsonify({"channel": channels}))

@app.route('/channels/<id>', methods = ['GET'])
def get_channel_by_id(id):
    get_channel = Channel.query.get(id)
    channel_schema = ChannelSchema()
    channel = channel_schema.dump(get_channel)
    return make_response(jsonify({"channel": channel}))

@app.route('/channels/<id>', methods = ['PUT'])
def update_channel_by_id(id):
    data = request.get_json()
    get_channel = Channel.query.get(id)
    if data.get('channel_name'):
        get_channel.channel_name = data['channel_name']

    if data.get('date_creation'):
        get_channel.date_creation = data['date_creation']

    if data.get('subscribers'):
        get_channel.subscribers= data['subscribers']

    db.session.add(get_channel)
    db.session.commit()
    channel_schema = ChannelSchema(only=['id', 'channel_name', 'date_creation','subscribers'])
    channel = channel_schema.dump(get_channel)
    return make_response(jsonify({"channel": channel}))

@app.route('/channels/<id>', methods = ['DELETE'])
def delete_channel_by_id(id):
    get_channel = Channel.query.get(id)
    db.session.delete(get_channel)
    db.session.commit()
    return make_response("",204)

#____________________POST,GET,GET,PUT,DELETE___________________

@app.route('/videos', methods = ['POST'])
def create_video():
    data = request.get_json()
    video_schema = VideoSchema()
    video = video_schema.load(data)
    result = video_schema.dump(video.create())
    return make_response(jsonify({"video": result}),200)

@app.route('/videos', methods = ['GET'])
def get_videos():
    get_videos = Video.query.all()
    video_schema = VideoSchema(many = True)
    videos = video_schema.dump(get_videos)
    return make_response(jsonify({"video": videos}))

@app.route('/videos/<id>', methods = ['GET'])
def get_video_by_id(id):
    get_video = Video.query.get(id)
    video_schema = VideoSchema()
    video = video_schema.dump(get_video)
    return make_response(jsonify({"video": video}))

@app.route('/videos/<id>', methods = ['PUT'])
def update_video_by_id(id):
    data = request.get_json()
    get_video = Video.query.get(id)
    if data.get('video_name'):
        get_video.video_name = data['video_name']

    if data.get('date_publication'):
        get_video.date_publication = data['date_publication']

    if data.get('weight'):
        get_video.weight = data['weight'] 
		  
    db.session.add(get_video)
    db.session.commit()
    video_schema = VideoSchema(only=['id', 'video_name', 'date_publication', 'weight'])
    video = video_schema.dump(get_video)
    return make_response(jsonify({"video": video}))

@app.route('/videos/<id>', methods = ['DELETE'])
def delete_video_by_id(id):
    get_video = Video.query.get(id)
    db.session.delete(get_video)
    db.session.commit()
    return make_response("",204)

#______________________________________________________________

if __name__ == '__main__':
    app.run(debug=True)
