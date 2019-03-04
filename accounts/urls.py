from django.conf.urls import url, include
from .views import *

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('login', LoginViewSet, base_name='login')
# router.register('users', CustomUserView, base_name='users')

urlpatterns = [
    url(r'^test-api/$', TestApiView.as_view()),
    url(r'^users/$', CustomUserView.as_view()),
    url(r'^users/hod$', HODView.as_view()),
    url(r'^users/faculities/$', FaculityView.as_view()),
    url(r'^users/add-faculty/$', CreateFaculityView.as_view()),
    url(r'^users/add-student/$', CreateStudentView.as_view()),
    url(r'^add-student-mark/$', AddStudentMark.as_view()),
    url(r'^student-marks/(?P<user_id>[\w-]+)/$', StudentMarks.as_view()),
    url(r'^fetch-users/(?P<added_by>[\w-]+)/$', FetchUsersView.as_view()),
    url(r'^account-varification-request/(?P<user_id>[\w-]+)/$', VarifyAccountRequestView.as_view()),
    url(r'^varify-account/(?P<user_id>[\w-]+)/$', VarifyAccountView.as_view()),
    url(r'^users/students/$', StudentView.as_view()),
    url(r'^auth/$', CustomAuthToken.as_view()),
    url(r'', include(router.urls))
]
