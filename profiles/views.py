from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response 
from django.http import Http404
from .models import Profile
from .serializers import ProfileSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']  
        extra_kwargs = {'password': {'write_only': True}}

class ProfileList(APIView):
    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()  # Save the new user

            profile_data = {'user': user.id} 
            profile_serializer = ProfileSerializer(data=profile_data)
            if profile_serializer.is_valid():
                profile_serializer.save() 

                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_201_CREATED)
            else:
                user.delete()
                return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileDetail(APIView):
    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, pk):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)