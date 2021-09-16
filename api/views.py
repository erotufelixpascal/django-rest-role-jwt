
from django_rest_role_jwt.settings import AUTH_USER_MODEL
from rest_framework import status
from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserListSerializer
)

#Registration list
class UserRegistrationView(APIView):
        serializer_class = UserRegistrationSerializer
        permission_classes = (AllowAny, )

        def post(self, request):
            serializer = self.serializer_class(data=request.data)
            valid = serializer.is_valid(raise_exception=True)

            if valid:
                serializer.save()
                status_code = status.HTTP_201_CREATED

                response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User successfully registered!',
                'user': serializer.data
            }

            return Response(response, status=status_code)

#views list
class UserListView(APIView):
        serializer_class = UserListSerializer
        permission_classes = (IsAuthenticated, )

        def get (self, request):
            user = request.user
            if user.role !=1:
                response ={
                'success': False,
                'status_code': status.HTTP_403_FORBIDDEN,
                'message':'You are not authorized to perform this action'
            }
                return Response(response, status.HTTP_403_FORBIDDEN)
            else:
                users = AUTH_USER_MODEL.objects.all()
                serializer = self.serializer_class(users, many = True)
                response ={
                    'success':True,
                    'status_code':status.HTTP_200_OK,
                    'message': 'Successfuly fetched users',
                    'users': serializer.data
            }
            
            return Response(response, status = status.HTTP_200_OK)

#login view
class UserLoginView(APIView):
        serializer_class = UserLoginSerializer
        permission_classes = (AllowAny, )

        def post(self, request): 
            serializer = self.serializer_class(data = request.data)

            valid = Serializer.is_valid(raise_exception = True)

            if valid:
                response ={
                    'success': True,
                    'statusCode': status.HTTP_200_OK,
                    'message': 'User logged in successfully',
                    'access': serializers.Serializer.data['access'],
                    'refresh': serializers.Serializer.data['refresh'],
                    'authenticatedUser':{
                    'email':serializers.Serializer.data['email'],
                    'role': serializers.Serializer.data['role']
                                        }
                            }

            return Response(response, status= status.HTTP_200_OK)
            

