from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User, Student, Employee, Teacher

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'is_student', 'is_employee']

class RegisterUserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'is_student', 'is_employee', 'is_teacher', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError('Parol mos emas!')
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')

        validated_data['is_active'] = True

        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = ['user','faculty', 'group', 'level', 'telegram_id']

class RegisterStudentSerializer(serializers.ModelSerializer):
    user = RegisterUserSerializer()

    class Meta:
        model = Student
        fields = ['user','birth_date', 'faculty', 'group', 'level', 'phone_number']

    def validate(self, data):
        user_data = data.get('user',{})
        password = user_data.get('password')
        confirm_password = user_data.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError({'password': 'Parol mos emas!'})
        return data

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data.pop('confirm_password')
        password = user_data.pop('password')
        user_data['is_student'] = True

        user = User(**user_data)
        user.set_password(password)
        user.save()

        student = Student.objects.create(user=user, **validated_data)
        return student

class RegisterEmployeeSerializer(serializers.ModelSerializer):
    user = RegisterUserSerializer()

    class Meta:
        model = Employee
        fields = ['user', 'position']

    def validate(self, data):
        user_data = data.get('user', {})
        password = user_data.get('password')
        confirm_password = user_data.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError({'password': 'Parollar mos emas'})
        return data

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data.pop('confirm_password')
        password = user_data.pop('password')
        user_data['is_employee'] = True

        user = User(**user_data)
        user.set_password(password)
        user.save()

        employee = Employee.objects.create(user=user, **validated_data)
        return employee

class RegisterTeacherSerializer(serializers.ModelSerializer):
    user = RegisterUserSerializer()

    class Meta:
        model = Teacher
        fields = ['user', 'subject', 'degree', 'work_experience', 'salary']

    def validate(self, data):
        user_data = data.get('users', {})
        password = user_data.get('password')
        confirm_password = user_data.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError({'msg': 'Parollar mos emas'})
        return data

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data.pop('confirm_password')
        password = user_data.pop('password')
        user_data['is_teacher'] = True

        user = User(**user_data)
        user.set_password(password)
        user.save()

        teacher = Teacher.objects.create(user=user, **validated_data)
        return teacher
