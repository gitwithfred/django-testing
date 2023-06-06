from django.urls import path

from . import views

app_name = 'main_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('files/', views.MainModelListView.as_view(), name='index'),
    path('files/create', views.MainModelCreateView.as_view(), name='create'),
    path('files/<int:pk>/', views.MainModelDetailView.as_view(), name='detail'),
    path('files/<int:pk>/edit', views.MainModelUpdateView.as_view(), name='update'),
    path('files/<int:pk>/delete', views.MainModelDeleteView.as_view(), name='delete'),
    path('files/form_view/', views.form_view, name='form_view'),
    path('files/form_view/<int:pk>', views.form_view, name='form_view'),
    path('files/detail_view/<int:pk>', views.detail_view, name='detail_view'),
]
