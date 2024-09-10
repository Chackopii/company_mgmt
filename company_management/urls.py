from django.contrib import admin
from django.urls import path
from company import views
from django.contrib.auth.views import LoginView,LogoutView


#-------------FOR ADMIN RELATED URLS
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name=''),


    # path('aboutus', views.aboutus_view),
    # path('contactus', views.contactus_view),


    path('adminclick', views.adminclick_view),
    path('managerclick', views.managerclick_view),
    path('employeeclick', views.employeeclick_view),

    path('adminsignup', views.admin_signup_view),
    path('managersignup', views.manager_signup_view,name='managersignup'),
    path('employeesignup', views.employee_signup_view ,name='employeesignup'),
    
    path('adminlogin', LoginView.as_view(template_name='company/adminlogin.html')),
    path('managerlogin/', LoginView.as_view(template_name='company/managerlogin.html'),name='managerlogin'),
    path('employeelogin/', LoginView.as_view(template_name='company/employeelogin.html'),name='employeelogin'),


    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='company/index.html'),name='logout'),


    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),


    path('admin-manager', views.admin_manager_view, name='admin-manager'),
    path('admin-view-manager/', views.admin_view_manager_view, name='admin-view-manager'),
    path('delete-manager-from-company/<int:pk>', views.delete_manager_from_company_view, name='delete-manager-from-company'),
    path('update-manager/<int:pk>', views.update_manager_view, name='update-manager'),
    path('admin-add-manager/', views.admin_add_manager_view, name='admin-add-manager'),
    path('admin-approve-manager/', views.admin_approve_manager_view, name='admin-approve-manager'),
    path('approve-manager/<int:pk>', views.approve_manager_view, name='approve-manager'),
    path('reject-manager/<int:pk>', views.reject_manager_view, name='reject-manager'),
    path('admin-view-manager-department/',views.admin_view_manager_department_view,name='admin-view-manager-department'),


    path('admin-employee', views.admin_employee_view,name='admin-employee'),
    path('admin-view-employee/', views.admin_view_employee_view,name='admin-view-employee'),
    path('delete-employee-from-company/<int:pk>', views.delete_employee_from_company_view,name='delete-employee-from-company'),
    path('update-employee/<int:pk>', views.update_employee_view,name='update-employee'),
    path('admin-add-employee/', views.admin_add_employee_view,name='admin-add-employee'),
    path('admin-approve-employee/', views.admin_approve_employee_view,name='admin-approve-employee'),
    path('approve-employee/<int:pk>', views.approve_employee_view,name='approve-employee'),
    path('reject-employee/<int:pk>', views.reject_employee_view,name='reject-employee'),

    path('admin-task', views.admin_task_view,name='admin-task'),
    path('admin-view-tasks', views.admin_view_task, name='admin-view-tasks'),
    path('admin-assign-task/<int:task_id>', views.admin_assign_task, name='admin-assign-task'),
    # path('admin-approve-task', views.approve_task_list_view, name='admin-approve-task'),


]

#---------FOR manager RELATED URLS-------------------------------------
urlpatterns +=[
    path('manager-dashboard', views.manager_dashboard_view,name='manager-dashboard'),

    path('manager-employee', views.manager_employee_view,name='manager-employee'),
    path('manager-view-employee', views.manager_view_employee_view,name='manager-view-employee'),
    # path('manager-view-discharge-employee',views.manager_view_discharge_employee_view,name='manager-view-discharge-employee'),

#     path('manager-task', views.manager_appointment_view,name='manager-appointment'),
#     path('manager-view-appointment', views.manager_view_appointment_view,name='manager-view-appointment'),
#     path('manager-delete-appointment',views.manager_delete_appointment_view,name='manager-delete-appointment'),
#     path('delete-appointment/<int:pk>', views.delete_appointment_view,name='delete-appointment'),
 ]