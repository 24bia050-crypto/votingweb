import re
from django.conf import settings
from django.db import transaction
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Voter, Position, Candidate, Vote
from .serializers import (
    VoterSerializer,
    PositionSerializer,
    CandidateSerializer,
)


class LoginView(APIView):
    def post(self, request):
        name = request.data.get('name')
        phone = request.data.get('phone')

        if not name or not phone:
            return Response({'detail': 'name and phone required'}, status=status.HTTP_400_BAD_REQUEST)

        phone = phone.strip()
        if not re.fullmatch(r'\+255\d{9}', phone):
            return Response({'detail': 'phone must start with +255 and include 9 digits'}, status=status.HTTP_400_BAD_REQUEST)

        voter = Voter.objects.filter(phone=phone).first()
        if voter:
            # Block re-login if already voted
            if voter.has_voted:
                return Response({'detail': 'you have already voted and cannot log in again'}, status=status.HTTP_403_FORBIDDEN)
            
            voter.name = name
            if not voter.token:
                voter.generate_token()
            voter.save(update_fields=['name', 'token'])
        else:
            voter = Voter.objects.create(
                name=name,
                phone=phone,
            )
            voter.generate_token()

        serializer = VoterSerializer(voter)
        return Response(serializer.data)


class PositionsView(APIView):
    def get(self, request):
        qs = Position.objects.all()
        serializer = PositionSerializer(qs, many=True)
        return Response(serializer.data)


class CandidatesByPositionView(APIView):
    def get(self, request, position_id):
        qs = Candidate.objects.filter(position_id=position_id).annotate(votes_count=Count('votes'))
        serializer = CandidateSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)


class VoteView(APIView):
    def post(self, request):
        token = request.data.get('token')
        candidate_id = request.data.get('candidate_id')
        if not token or not candidate_id:
            return Response({'detail': 'token and candidate_id required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            voter = Voter.objects.get(token=token)
        except Voter.DoesNotExist:
            return Response({'detail': 'invalid token'}, status=status.HTTP_403_FORBIDDEN)
        if voter.has_voted:
            return Response({'detail': 'already voted'}, status=status.HTTP_403_FORBIDDEN)
        try:
            candidate = Candidate.objects.select_related('position').get(pk=candidate_id)
        except Candidate.DoesNotExist:
            return Response({'detail': 'candidate not found'}, status=status.HTTP_404_NOT_FOUND)

        # Enforce one vote per position using transaction and unique_together
        with transaction.atomic():
            # create vote; unique_together prevents duplicates
            Vote.objects.create(voter=voter, candidate=candidate, position=candidate.position)
            voter.has_voted = True
            voter.save(update_fields=['has_voted'])

        return Response({'detail': 'vote recorded'}, status=status.HTTP_201_CREATED)


class ResultsView(APIView):
    def get(self, request):
        qs = Candidate.objects.annotate(vote_count=Count('votes')).order_by('-vote_count')
        data = [
            {
                'id': c.id,
                'name': c.name,
                'position': c.position.name,
                'image_url': c.image.url if c.image else c.image_url,
                'votes': c.vote_count,
            }
            for c in qs
        ]
        return Response(data)


class AdminBaseView(APIView):
    def _is_admin(self, request):
        key = request.headers.get('X-Admin-Key') or request.query_params.get('admin_key')
        return key == getattr(settings, 'ADMIN_API_KEY', 'adminsecret')

    def dispatch(self, request, *args, **kwargs):
        if not self._is_admin(request):
            return Response({'detail': 'forbidden'}, status=status.HTTP_403_FORBIDDEN)
        return super().dispatch(request, *args, **kwargs)


class AdminCandidateView(AdminBaseView):
    def get(self, request):
        qs = Candidate.objects.select_related('position').annotate(vote_count=Count('votes'))
        serializer = CandidateSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        name = request.data.get('name')
        position_id = request.data.get('position_id')
        image_url = request.data.get('image_url')
        if not name or not position_id:
            return Response({'detail': 'name and position_id required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            pos = Position.objects.get(pk=position_id)
        except Position.DoesNotExist:
            return Response({'detail': 'position not found'}, status=status.HTTP_404_NOT_FOUND)
        cand = Candidate.objects.create(name=name, position=pos, image_url=image_url)
        return Response({'id': cand.id, 'name': cand.name}, status=status.HTTP_201_CREATED)


class MeView(APIView):
    def get(self, request):
        auth = request.headers.get('Authorization', '')
        token = auth.replace('Token ', '') if auth.startswith('Token ') else None
        if not token:
            return Response({'detail': 'authorization missing'}, status=status.HTTP_403_FORBIDDEN)
        try:
            voter = Voter.objects.get(token=token)
        except Voter.DoesNotExist:
            return Response({'detail': 'invalid token'}, status=status.HTTP_403_FORBIDDEN)
        serializer = VoterSerializer(voter)
        return Response(serializer.data)


class AdminPositionView(AdminBaseView):
    def get(self, request):
        qs = Position.objects.all()
        serializer = PositionSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        name = request.data.get('name')
        description = request.data.get('description', '')
        if not name:
            return Response({'detail': 'name required'}, status=status.HTTP_400_BAD_REQUEST)
        position = Position.objects.create(name=name, description=description)
        return Response({'id': position.id, 'name': position.name}, status=status.HTTP_201_CREATED)


class AdminCandidateDetailView(AdminBaseView):
    def patch(self, request, candidate_id):
        try:
            candidate = Candidate.objects.get(pk=candidate_id)
        except Candidate.DoesNotExist:
            return Response({'detail': 'candidate not found'}, status=status.HTTP_404_NOT_FOUND)
        name = request.data.get('name')
        position_id = request.data.get('position_id')
        image_url = request.data.get('image_url')
        if name:
            candidate.name = name
        if position_id:
            try:
                candidate.position = Position.objects.get(pk=position_id)
            except Position.DoesNotExist:
                return Response({'detail': 'position not found'}, status=status.HTTP_404_NOT_FOUND)
        if image_url is not None:
            candidate.image_url = image_url
        candidate.save()
        return Response({'id': candidate.id, 'name': candidate.name})

    def delete(self, request, candidate_id):
        try:
            candidate = Candidate.objects.get(pk=candidate_id)
        except Candidate.DoesNotExist:
            return Response({'detail': 'candidate not found'}, status=status.HTTP_404_NOT_FOUND)
        candidate.delete()
        return Response({'detail': 'candidate deleted'})


class AdminUserView(AdminBaseView):
    def get(self, request):
        qs = Voter.objects.all().order_by('-created_at')
        serializer = VoterSerializer(qs, many=True)
        return Response(serializer.data)


class AdminVoteView(AdminBaseView):
    def get(self, request):
        qs = Vote.objects.select_related('voter', 'candidate', 'position').all()
        data = [
            {
                'id': vote.id,
                'voter': vote.voter.name,
                'phone': vote.voter.phone,
                'candidate': vote.candidate.name,
                'position': vote.position.name,
                'created_at': vote.created_at,
            }
            for vote in qs
        ]
        return Response(data)


class WinnersView(AdminBaseView):
    def get(self, request):
        qs = Candidate.objects.annotate(vote_count=Count('votes')).order_by('-vote_count')
        data = [
            {
                'id': candidate.id,
                'name': candidate.name,
                'position': candidate.position.name,
                'votes': candidate.vote_count,
                'image_url': candidate.image.url if candidate.image else candidate.image_url,
            }
            for candidate in qs
        ]
        return Response(data)


class AdminUploadImageView(AdminBaseView):
    def post(self, request):
        candidate_id = request.data.get('candidate_id')
        image_url = request.data.get('image_url')
        if not candidate_id or not image_url:
            return Response({'detail': 'candidate_id and image_url required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            candidate = Candidate.objects.get(pk=candidate_id)
        except Candidate.DoesNotExist:
            return Response({'detail': 'candidate not found'}, status=status.HTTP_404_NOT_FOUND)
        candidate.image_url = image_url
        candidate.save(update_fields=['image_url'])
        return Response({'id': candidate.id, 'image_url': candidate.image_url})


class ResetElectionView(AdminBaseView):
    def post(self, request):
        Vote.objects.all().delete()
        Voter.objects.update(has_voted=False)
        return Response({'detail': 'election reset completed'})
