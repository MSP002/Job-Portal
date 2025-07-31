from django.urls import path,include
from . import views
from django.contrib.auth import admin


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('post-job/', views.job_posting_view, name='post_job'),
    path('search-jobs/', views.job_search_view, name='search_jobs'),
    path('apply-job/<int:job_id>/', views.apply_job_view, name='apply_job'),
    path('admin/manage/', views.admin_manage_view, name='admin_manage'),
    path('admin-dashboard/manage-jobs/', views.admin_manage_jobs, name='admin_manage_jobs'),
    path('manage-jobs/', views.manage_jobs, name='manage_jobs'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    
]
