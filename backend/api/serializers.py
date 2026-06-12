from rest_framework import serializers
from .models import Voter, Position, Candidate, Vote


class VoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        fields = ['id', 'name', 'phone', 'has_voted', 'is_admin', 'token']


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'name', 'description']


class CandidateSerializer(serializers.ModelSerializer):
    votes_count = serializers.IntegerField(read_only=True)
    position_name = serializers.CharField(source='position.name', read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Candidate
        fields = ['id', 'name', 'image_url', 'position', 'position_name', 'votes_count']

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return obj.image_url or ''


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'voter', 'candidate', 'position', 'created_at']
