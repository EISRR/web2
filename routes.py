from flask_marshmallow import Marshmallow
from flask_jwt_extended import jwt_required
from models import *
from flask_restful import Resource
from flask import request

class VideoResource(Resource):
    def get(self, video_id):
        video = Video.query.get_or_404(video_id)
        
        return video_schema.dump(video)

    def patch(self, video_id):
        video = Video.query.get_or_404(video_id)
        if 'viName' in request.json: 
            video.viName = request.json['viName'],
        if 'weight' in request.json:
            video.weight = request.json['weight'],
        if 'datePublish' in request.json: 
            video.datePublish = request.json['datePublish'],
        if 'channel_id' in request.json:  
            video.channel_id = request.json['channel_id']

        db.session.commit()

        return video_schema.dump(video)

    def delete(self, video_id):
        video = Video.query.get_or_404(video_id)

        db.session.delete(video)
        db.session.commit()

        return '', 204

class VideoListResource(Resource):
    def get(self):
        videos = Video.query.all()

        return [a.to_dict() for a in videos]

    def post(self):
        new_video = Video(
            viName=request.json['viName'],
            weight=request.json['weight'],
            datePublish=request.json['datePublish'],
            channel_id=request.json['channel_id']
        )

        db.session.add(new_video)
        db.session.commit()

        return video_schema.dump(new_video)

class ChannelListResource(Resource):
    def get(self):
        channels = Channel.query.all()
        return [a.to_dict() for a in channels]

    def post(self):
        new_channel = Channel(
            nameAuthor=request.json['nameAuthor'],
            subs=request.json['subs'],
            date=request.json['dateCreation'],
        )

        db.session.add(new_channel)
        db.session.commit()

        return channel_schema.dump(new_channel)