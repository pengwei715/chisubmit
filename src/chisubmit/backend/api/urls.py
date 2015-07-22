from chisubmit.backend.api import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url

URL_PREFIX = r"^api/v1/"

urlpatterns = [
    url(URL_PREFIX + r'courses/$', views.CourseList.as_view(), name="course-list"),
    url(URL_PREFIX + r'courses/(?P<course>[a-zA-Z0-9_-]+)/$', views.CourseDetail.as_view(), name="course-detail"),

    url(URL_PREFIX + r'courses/(?P<course>[a-zA-Z0-9_-]+)/instructors/$', views.InstructorList.as_view(), name="instructor-list"),
    url(URL_PREFIX + r'courses/(?P<course>[a-zA-Z0-9_-]+)/instructors/(?P<username>[a-zA-Z0-9_-]+)$', views.InstructorDetail.as_view(), name="instructor-detail"),

    url(URL_PREFIX + r'courses/(?P<course>[a-zA-Z0-9_-]+)/graders/$', views.GraderList.as_view(), name="grader-list"),
    url(URL_PREFIX + r'courses/(?P<course>[a-zA-Z0-9_-]+)/graders/(?P<username>[a-zA-Z0-9_-]+)$', views.GraderDetail.as_view(), name="grader-detail"),

    url(URL_PREFIX + r'courses/(?P<course>[a-zA-Z0-9_-]+)/students/$', views.StudentList.as_view(), name="student-list"),
    url(URL_PREFIX + r'courses/(?P<course>[a-zA-Z0-9_-]+)/students/(?P<username>[a-zA-Z0-9_-]+)$', views.StudentDetail.as_view(), name="student-detail"),

    url(URL_PREFIX + r'courses/(?P<course>[a-zA-Z0-9_-]+)/assignments/$', views.AssignmentList.as_view(), name="assignment-list"),
    url(URL_PREFIX + r'courses/(?P<course>[a-zA-Z0-9_-]+)/assignments/(?P<assignment>[a-zA-Z0-9_-]+)$', views.AssignmentDetail.as_view(), name="assignment-detail"),

    url(URL_PREFIX + r'courses/(?P<course>[a-zA-Z0-9_-]+)/assignments/(?P<assignment>[a-zA-Z0-9_-]+)/rubric$', views.RubricList.as_view(), name="rubric-list"),
    url(URL_PREFIX + r'courses/(?P<course>[a-zA-Z0-9_-]+)/assignments/(?P<assignment>[a-zA-Z0-9_-]+)/rubric/(?P<rubric_component>[0-9]+)$', views.RubricDetail.as_view(), name="rubric-detail"),

    url(URL_PREFIX + r'courses/(?P<course>[a-zA-Z0-9_-]+)/assignments/(?P<assignment>[a-zA-Z0-9_-]+)/register', views.Register.as_view(), name="register"),

    url(URL_PREFIX + r'courses/(?P<course>[a-zA-Z0-9_-]+)/teams/$', views.TeamList.as_view(), name="team-list"),
    url(URL_PREFIX + r'courses/(?P<course>[a-zA-Z0-9_-]+)/teams/(?P<team>[a-zA-Z0-9_-]+)$', views.TeamDetail.as_view(), name="team-detail"),

    url(URL_PREFIX + r'users/$', views.UserList.as_view(), name="user-list"),
    url(URL_PREFIX + r'users/(?P<username>[a-zA-Z0-9_-]+)/$', views.UserDetail.as_view(), name="user-detail"),
    url(URL_PREFIX + r'users/(?P<username>[a-zA-Z0-9_-]+)/token/$', views.UserToken.as_view(), name="user-token"),
    
    url(URL_PREFIX + r'user/$', views.AuthUserDetail.as_view(), name="auth-user-detail"),
    url(URL_PREFIX + r'user/token/$', views.AuthUserToken.as_view(), name="auth-user-token"),
]

urlpatterns = format_suffix_patterns(urlpatterns)