from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from yaml import serialize

from .serializers import (RegisterUserSerializer,
                          RegisterStudentSerializer,
                          RegisterEmployeeSerializer,
                          RegisterTeacherSerializer)
from drf_yasg.utils import swagger_auto_schema

# Create your views here.

class RegisterUserView(APIView):
    @swagger_auto_schema(request_body=RegisterUserSerializer)
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Foydalanuvchi yaratildi'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterStudentView(APIView):
    @swagger_auto_schema(request_body=RegisterStudentSerializer)
    def post(self, request):
        serializer = RegisterStudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': "Talaba ro'yxatdan o'tdi."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterEmployeeView(APIView):
    @swagger_auto_schema(request_body=RegisterEmployeeSerializer)
    def post(self, request):
        serializer = RegisterEmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': "Ro'yxatdan o'tdingiz"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterTeacherView(APIView):
    @swagger_auto_schema(request_body=RegisterTeacherSerializer)
    def post(self, request):
        serializer = RegisterTeacherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': "Ro'yxatdan o'tdingiz"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


