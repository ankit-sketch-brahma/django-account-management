from rest_framework import serializers
from .models import *


# create serializers

class CustomUserSerializer(serializers.ModelSerializer):
    # full_name = serializers.CharField(max_length=100)
    # email = serializers.EmailField(max_length=255, allow_blank=False)
    # user_type = serializers.CharField(max_length=5)

    class Meta:
        model = CustomUser
        fields = ('user_id', 'email', 'full_name', 'password', 'user_type')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            user_type=validated_data['user_type']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user

class HODSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer()
    class Meta:
        model = HOD
        fields = ('id', 'author')

class FaculitySerializer(serializers.ModelSerializer):
    author = CustomUserSerializer()

    class Meta:
        model = Faculity
        fields = ('id', 'author', 'added_by')

class StudentSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer()
    class Meta:
        model = Student
        fields = ('id', 'author')


class AddStudentMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentMark
        fields = ('author', 'subject', 'mark')

    def create(self, validated_data):
        obj = StudentMark(
            author=validated_data['author'],
            subject=validated_data['subject'],
            mark=validated_data['mark']
        )

        obj.save()
        return obj
