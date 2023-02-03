from django.urls import path
# from . import views - This is used when you use functions base views
from . views import TaskList , TaskDetail , TaskCreate , TaskUpdate , TaskDelete, CustomLoginView, RegisterPage
from django.contrib.auth.views import LogoutView
# The above used when you use CBV then import the class you created
# but the urls expected FBV in that case your need to mention as.view() after your class

urlpatterns = [
    path('logout/',LogoutView.as_view(next_page = 'login'), name = 'logout'),
    path('register/',RegisterPage.as_view(), name = 'register'),
    path('',CustomLoginView.as_view(), name = 'login'),
    path("tasks",TaskList.as_view(), name = 'tasks'),
    path("task/<int:pk>/",TaskDetail.as_view(), name = 'task'),
    path("task-create/",TaskCreate.as_view(), name = 'task-create'),
    path("task-update/<int:pk>/",TaskUpdate.as_view(), name = 'task-update'),
    path("task-delete/<int:pk>/",TaskDelete.as_view(), name = 'task-delete'),

]
