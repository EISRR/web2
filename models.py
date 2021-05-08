from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
mshm = Marshmallow()

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    viName = db.Column(db.String(100), unique=True, nullable=False)
    weight = db.Column(db.Integer, unique=True, nullable=False)
    datePublish = db.Column(db.String(100), unique=True, nullable=False)
    channel = db.relationship('Channel', backref='videos', lazy=True)
    channel_id = db.Column(db.Integer, db.ForeignKey('channel.id'), nullable=False)

    def __str__(self):
        result = f'viName:{self.viName}'
        return result

    def to_dict(self):
        return {
            'id': self.id,
            'viName': self.viName,
            'weight': self.weight,
            'datePublish': self.datePublish,
            'channel_id': self.channel_id,
            'channel': self.channel,
        }

class VideoSchema(mshm.Schema):
    class Meta:
        fields = ("id","viName","weight", "datePublish","channel_id","channel")
        model = Video

class Channel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nameAuthor = db.Column(db.String(100), unique=True, nullable=False)
    subs = db.Column(db.String(100), unique=True, nullable=False)
    dateCreation = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return '<Channel %r>' % self.nameAuthor

    def to_dict(self):
        return {
            'id': self.id,
            'nameAuthor': self.nameAuthor,
            'subs': self.subs,
            'dateCreation': self.dateCreation,
        }

class ChannelSchema(mshm.Schema):
    class Meta:
        fields = ("id","nameAuthor","subs","dateCreation")
        model = Channel

channel_schema = ChannelSchema()
channels_schema = ChannelSchema(many=True)
video_schema = VideoSchema()
videos_schema = VideoSchema(many=True)