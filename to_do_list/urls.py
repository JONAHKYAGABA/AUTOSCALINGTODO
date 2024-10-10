from django.urls import path, include


from . views import CustomLoginView , TaskList,TaskDetail,TaskCreate,TaskUpdate,DeleteView,RegisterPage
from django.contrib.auth.views import LogoutView
from . import views
from django.urls import reverse
from django.conf.urls.static import static


app_name = 'to_do_list'



urlpatterns = [
    path('', views.index, name='index'),
    path('signin/', CustomLoginView.as_view(),name='signin'),
    path('tasks/',TaskList.as_view(),name='tasks'),
    path('logout/', LogoutView.as_view (next_page='to_do_list:signin'),name='logout'),
    path('profile/', views.profile, name='profile'),
    path('signup/',RegisterPage.as_view(), name='signup'),
    path('task/<int:pk>/',TaskDetail.as_view(),name='task'),
    path('create-task/',TaskCreate.as_view(),name='task-create'),
    path('task-update/<int:pk>/',TaskUpdate.as_view(),name='task-update'),
    path('task-delete/<int:pk>/',DeleteView.as_view(),name='task-delete'),   
] #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


