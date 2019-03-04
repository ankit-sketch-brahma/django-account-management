from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from .serializers import *

# Create your views here.

class TestApiView(APIView):
    def get(self, request):
        return Response({"message": "Test Message"})

class CustomUserView(APIView):
    def get(self, request):
        users_obj = CustomUser.objects.all()
        custom_user_serializer = CustomUserSerializer(users_obj, many=True)

        return Response({"users": custom_user_serializer.data})

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            user = CustomUser.get_user_by_id(serializer.data.get('user_id'))
            if request.data['user_type'] == "H":
                new_user = HOD(author=user)
            elif request.data['user_type'] == "F":
                new_user = Faculity(author=user)
            elif request.data['user_type'] == "S":
                new_user = Student(author=user)

            new_user.save()

            full_name = serializer.data.get('full_name')
            data = {}
            data['user_type'] = serializer.data.get('user_type')
            data['full_name'] = serializer.data.get('full_name')
            data['user_id'] = serializer.data.get('user_id')
            return Response(data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HODView(APIView):
    def get(self, request):
        hods_obj = HOD.objects.all()
        custom_user_serializer = HODSerializer(hods_obj, many=True)

        return Response({"hod's": custom_user_serializer.data, "Name": "Faculity"})

class FaculityView(APIView):
    def get(self, request):
        users_obj = Faculity.objects.all()
        custom_user_serializer = FaculitySerializer(users_obj, many=True)

        return Response({"faculities": custom_user_serializer.data})

class CreateFaculityView(APIView):
    def post(self, request):
        try:
            print(request.data)
            user_serializer = CustomUserSerializer(data=request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                user = CustomUser.get_user_by_id(user_serializer.data.get('user_id'))
                hod = HOD.get_hod_by_id(request.data['added_by'])
                new_user = Faculity(author=user, added_by=hod)
                new_user.save()

                faculty = {}
                faculty['user_id'] = new_user.id
                faculty['name'] = user_serializer.data.get('full_name')
                faculty['email'] = user_serializer.data.get('email')
                print(faculty)
                return Response({'user': faculty, 'user_type': 'F'})
            else:
                print(user_serializer.errors)
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print('Errorr', e)
            return Response({"error": "error"}, status=status.HTTP_400_BAD_REQUEST)

class CreateStudentView(APIView):
    def post(self, request):
        try:
            print(request.data)
            user_serializer = CustomUserSerializer(data=request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                user = CustomUser.get_user_by_id(user_serializer.data.get('user_id'))
                fac = Faculity.get_faculity_by_id(request.data['added_by'])
                new_user = Student(author=user, added_by=fac)
                new_user.is_varified = True
                new_user.save()

                student = {}
                student['id'] = new_user.id
                student['name'] = user_serializer.data.get('full_name')
                student['email'] = user_serializer.data.get('email')
                student['is_varified'] = new_user.is_varified
                student['added_by'] = fac.author.full_name
                student['is_request_sent'] = new_user.is_request_sent_for_varify
                print(student)
                return Response({'user': student, 'user_type': 'S'})
            else:
                print(user_serializer.errors)
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print('Errorr', e)
            return Response({"error": "error"}, status=status.HTTP_400_BAD_REQUEST)

class StudentView(APIView):
    def get(self, request):
        hods_obj = Student.objects.all()
        custom_user_serializer = StudentSerializer(hods_obj, many=True)

        return Response({"students": custom_user_serializer.data})

class FetchUsersView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            users = {}
            faculty_list = list()
            students_list = list()
            user_type = request.GET.get('user_type', '')
            print(user_type)

            if user_type == "H":
                hod = HOD.get_hod_by_id(kwargs['added_by'])
                faculty_obj = Faculity.objects.filter(added_by=hod)

                for faculty in faculty_obj:
                    faculity_dict = dict()
                    faculity_dict['user_id'] = faculty.id
                    faculity_dict['name'] = faculty.author.full_name
                    faculity_dict['email'] = faculty.author.email

                    students_obj = Student.objects.filter(added_by=faculty)
                    for student in students_obj:
                        student_dict = dict()
                        student_dict['user_id'] = student.id
                        student_dict['name'] = student.author.full_name
                        student_dict['email'] = student.author.email
                        student_dict['added_by'] = faculty.author.full_name
                        student_dict['is_varified'] = student.is_varified
                        student_dict['is_request_sent'] = student.is_request_sent_for_varify

                        students_list.append(student_dict)

                    faculty_list.append(faculity_dict)

                users['faculties'] = faculty_list
                users['students'] = students_list

                return Response({"users": users})

            elif user_type == "F":
                fac = Faculity.get_faculity_by_id(kwargs['added_by'])
                students_obj = Student.objects.filter(added_by=fac)

                for student in students_obj:
                    student_dict = dict()
                    student_dict['user_id'] = student.id
                    student_dict['name'] = student.author.full_name
                    student_dict['email'] = student.author.email
                    student_dict['is_varified'] = student.is_varified
                    student_dict['is_request_sent'] = student.is_request_sent_for_varify

                    students_list.append(student_dict)

                users['students'] = students_list
                return Response({"users": users})

        except Exception as e:
            print(e)
            return Response({"error": e})

class StudentMarks(APIView):
    def get(self, request, *args, **kwargs):
        try:
            stu_marks = StudentMark.objects.filter(author=kwargs['user_id'])
            stu_marks_list = list()

            for stu_mark in stu_marks:
                stu_mark_dict = dict()
                stu_mark_dict['subject'] = stu_mark.subject
                stu_mark_dict['mark'] = stu_mark.mark

                stu_marks_list.append(stu_mark_dict)

            return Response({"student_marks": stu_marks_list})

        except Exception as e:
            print('Errorr', e)
            return Response({"error": "error"}, status=status.HTTP_400_BAD_REQUEST)

class AddStudentMark(APIView):
    def post(self, request):
        try:
            print(request.data)
            addStuMark_serializer = AddStudentMarkSerializer(data=request.data)
            if addStuMark_serializer.is_valid():
                addStuMark_serializer.save()
                return Response({'message': 'Mark added successfully'})
            else:
                print(user_serializer.errors)
                return Response(addStuMark_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print('Errorr', e)
            return Response({"error": "error"}, status=status.HTTP_400_BAD_REQUEST)

class VarifyAccountRequestView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            student_id = kwargs['user_id']
            stu_obj = Student.get_student_by_id(student_id)
            stu_obj.is_request_sent_for_varify = True
            stu_obj.save()
            return Response({'message': 'Account Varification Request sent successfully'})

        except Exception as e:
            print('Errorr', e)
            return Response({"error": "error"}, status=status.HTTP_400_BAD_REQUEST)

class VarifyAccountView(APIView):
    def post(self, request, *args, **kwargs):
        print("insode")
        try:
            student_id = kwargs['user_id']
            stu_obj = Student.get_student_by_id(student_id)
            hod_id = request.data['added_by']

            if stu_obj.added_by.added_by.id == hod_id:
                stu_obj.is_varified = True
                stu_obj.is_request_sent_for_varify = False
                stu_obj.save()
                return Response({'message': 'Account Varified'})
            else:
                return Response({'message': 'Unauthorized Access'})

        except Exception as e:
            print('Errorr', e)
            return Response({"error": "error"}, status=status.HTTP_400_BAD_REQUEST)
class LoginViewSet(viewsets.ViewSet):
    serializer_class = AuthTokenSerializer

    def create(self, request):
        return ObtainAuthToken().post(request)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        hod = HOD.objects.filter(author=user)
        fac = Faculity.objects.filter(author=user)
        stu = Student.objects.filter(author=user)

        if hod:
            current_user = hod[0]
        if fac:
            current_user = fac[0]
        if stu:
            current_user = stu[0]

        if user.user_type == "S" :
            return Response({
                'token': token.key,
                'user_id': current_user.id,
                'name': user.full_name,
                'user_type': user.user_type,
                'is_varified': current_user.is_varified,
                'is_request_sent': current_user.is_request_sent_for_varify,
            })

        else:
            return Response({
                'token': token.key,
                'user_id': current_user.id,
                'name': user.full_name,
                'user_type': user.user_type
            })
