from django.shortcuts import render,redirect,get_object_or_404
from company import forms ,models
from django.urls import reverse
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.conf import settings

def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'company/index.html')


# for showing signup/login button for admin
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'company/adminclick.html')


# for showing signup/login button for manager (formerly manager)
def managerclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'company/managerclick.html')


# for showing signup/login button for employee (formerly employee)
def employeeclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'company/employeeclick.html')


def admin_signup_view(request):
    form = forms.AdminSignupForm()
    if request.method == 'POST':
        form = forms.AdminSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group, created = Group.objects.get_or_create(name='ADMIN')
            my_admin_group.user_set.add(user)
            return redirect('adminlogin')
    return render(request, 'company/adminsignup.html', {'form': form})


def manager_signup_view(request):
    userForm = forms.ManagerUserForm()
    managerForm = forms.ManagerForm()
    context = {'userForm': userForm, 'managerForm': managerForm}
    if request.method == 'POST':
        userForm = forms.ManagerUserForm(request.POST)
        managerForm = forms.ManagerForm(request.POST, request.FILES)
        if userForm.is_valid() and managerForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            manager = managerForm.save(commit=False)
            manager.user = user
            manager.save()
            my_manager_group, created = Group.objects.get_or_create(name='MANAGER')
            my_manager_group.user_set.add(user)
            return redirect('managerlogin')
    return render(request, 'company/managersignup.html', context)


def employee_signup_view(request):
    userForm = forms.EmployeeUserForm()
    employeeForm = forms.EmployeeForm()
    context = {'userForm': userForm, 'employeeForm': employeeForm}
    if request.method == 'POST':
        userForm = forms.EmployeeUserForm(request.POST)
        employeeForm = forms.EmployeeForm(request.POST, request.FILES)
        if userForm.is_valid() and employeeForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            employee = employeeForm.save(commit=False)
            employee.user = user
            # employee.department = request.POST.get('department')  # Assuming department is passed in the form
            employee.save()
            my_employee_group, created = Group.objects.get_or_create(name='EMPLOYEE')
            my_employee_group.user_set.add(user)
            return redirect('employeelogin')
    return render(request, 'company/employeesignup.html', context)


# Check user role
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()

def is_manager(user):
    return user.groups.filter(name='MANAGER').exists()

def is_employee(user):
    return user.groups.filter(name='EMPLOYEE').exists()


# Redirect users after login based on their role
def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_manager(request.user):
        accountapproval = models.Manager.objects.all().filter(user_id=request.user.id, status=True)
        if accountapproval:
            return redirect('manager-dashboard')
        else:
            return render(request, 'company/manager_wait_for_approval.html')
    elif is_employee(request.user):
        accountapproval = models.Employee.objects.all().filter(user_id=request.user.id, status=True)
        if accountapproval:
            return redirect('employee-dashboard')
        else:
            return render(request, 'company/employee_wait_for_approval.html')
    # else:
    #     return redirect('logout')  # Redirect to login or another appropriate page

# Admin-related views

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    # Data for dashboard
    managers = models.Manager.objects.all().order_by('-id')
    employees = models.Employee.objects.all().order_by('-id')

    # Counts for active and pending managers
    managercount = models.Manager.objects.filter(status=True).count()
    pendingmanagercount = models.Manager.objects.filter(status=False).count()

    # Counts for active and pending employees
    employeecount = models.Employee.objects.filter(status=True).count()
    pendingemployeecount = models.Employee.objects.filter(status=False).count()

    # counts for active and pending task
    taskcount=models.Task.objects.filter(status=True).count
    pendingtaskcount=models.Task.objects.filter(status=False).count
    
    # Attendance records
    attendancecount = models.Attendance.objects.count()

    context = {
        'managers': managers,
        'employees': employees,
        'managercount': managercount,
        'pendingmanagercount': pendingmanagercount,
        'employeecount': employeecount,
        'pendingemployeecount': pendingemployeecount,
        'taskcount': taskcount,
        'pendingtaskcount': pendingtaskcount,
        'attendancecount': attendancecount,
    }

    return render(request, 'company/admin_dashboard.html', context=context)

# --------------------------------------------admin-manager-views----------------------------------------#
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_manager_view(request):
    return render(request, 'company/admin_manager.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_manager_view(request):
    managers = models.Manager.objects.filter(status=True)
    return render(request, 'company/admin_view_manager.html', {'managers': managers})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_manager_from_company_view(request, pk):
    manager = models.Manager.objects.get(id=pk)
    user = models.User.objects.get(id=manager.user_id)
    user.delete()
    manager.delete()
    return redirect('admin-view-manager')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_manager_view(request, pk):
    manager = models.Manager.objects.get(id=pk)
    user = models.User.objects.get(id=manager.user_id)

    userForm = forms.ManagerUserForm(instance=user)
    managerForm = forms.ManagerForm(request.FILES, instance=manager)
    context = {'userForm': userForm, 'managerForm': managerForm}

    if request.method == 'POST':
        userForm = forms.ManagerUserForm(request.POST, instance=user)
        managerForm = forms.ManagerForm(request.POST, request.FILES, instance=manager)
        if userForm.is_valid() and managerForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            manager = managerForm.save(commit=False)
            manager.status = True
            manager.save()
            return redirect('admin-view-manager')
    return render(request, 'company/admin_update_manager.html', context=context)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_manager_view(request):
    userForm = forms.ManagerUserForm()
    managerForm = forms.ManagerForm()
    context = {'userForm': userForm, 'managerForm': managerForm}

    if request.method == 'POST':
        userForm = forms.ManagerUserForm(request.POST)
        managerForm = forms.ManagerForm(request.POST, request.FILES)
        if userForm.is_valid() and managerForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            manager = managerForm.save(commit=False)
            manager.user = user
            manager.status = True
            manager.save()

            my_manager_group, created = Group.objects.get_or_create(name='MANAGER')
            my_manager_group.user_set.add(user)

            return redirect('admin-view-manager')
    return render(request, 'company/admin_add_manager.html', context=context)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_manager_view(request):
    managers = models.Manager.objects.filter(status=False)
    return render(request, 'company/admin_approve_manager.html', {'managers': managers})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_manager_view(request, pk):
    manager = models.Manager.objects.get(id=pk)
    manager.status = True
    manager.save()
    return redirect(reverse('admin-approve-manager'))

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_manager_view(request, pk):
    manager = models.Manager.objects.get(id=pk)
    user = models.User.objects.get(id=manager.user_id)
    user.delete()
    manager.delete()
    return redirect('admin-approve-manager')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_manager_department_view(request):
    managers = models.Manager.objects.filter(status=True)
    return render(request, 'company/admin-view-manager-department.html', {'managers': managers})




# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def admin_employee_view(request):
#     return render(request, 'company/admin_employee.html')


# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def admin_view_employee_view(request):
#     employees = models.Employee.objects.filter(status=True)
#     return render(request, 'company/admin_view_employee.html', {'employees': employees})


# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def delete_employee_from_company_view(request, pk):
#     employee = models.Employee.objects.get(id=pk)
#     user = models.User.objects.get(id=employee.user_id)
#     user.delete()
#     employee.delete()
#     return redirect('admin-view-employee')


# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def update_employee_view(request, pk):
#     employee = models.Employee.objects.get(id=pk)
#     user = models.User.objects.get(id=employee.user_id)

#     userForm = forms.EmployeeUserForm(instance=user)
#     employeeForm = forms.EmployeeForm(request.FILES, instance=employee)
#     context = {'userForm': userForm, 'employeeForm': employeeForm}

#     if request.method == 'POST':
#         userForm = forms.EmployeeUserForm(request.POST, instance=user)
#         employeeForm = forms.EmployeeForm(request.POST, request.FILES, instance=employee)
#         if userForm.is_valid() and employeeForm.is_valid():
#             user = userForm.save()
#             user.set_password(user.password)
#             user.save()
#             employee = employeeForm.save(commit=False)
#             employee.status = True
#             employee.save()
#             return redirect('admin-view-employee')
#     return render(request, 'company/admin_update_employee.html', context=context)


# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def admin_add_employee_view(request):
#     userForm = forms.EmployeeUserForm()
#     employeeForm = forms.EmployeeForm()
#     context = {'userForm': userForm, 'employeeForm': employeeForm}

#     if request.method == 'POST':
#         userForm = forms.EmployeeUserForm(request.POST)
#         employeeForm = forms.EmployeeForm(request.POST, request.FILES)
#         if userForm.is_valid() and employeeForm.is_valid():
#             user = userForm.save()
#             user.set_password(user.password)
#             user.save()

#             employee = employeeForm.save(commit=False)
#             employee.user = user
#             employee.status = True
#             employee.save()

#             my_employee_group, created = Group.objects.get_or_create(name='EMPLOYEE')
#             my_employee_group.user_set.add(user)

#             return redirect('admin-view-employee')
#     return render(request, 'company/admin_add_employee.html', context=context)


# --------------------------------------------admin-employee-views----------------------------------------#

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_employee_view(request):
    return render(request, 'company/admin_employee.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_employee_view(request):
    employees = models.Employee.objects.filter(status=True)
    return render(request, 'company/admin_view_employee.html', {'employees': employees})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_employee_from_company_view(request, pk):
    employee = models.Employee.objects.get(id=pk)
    user = models.User.objects.get(id=employee.user_id)
    user.delete()
    employee.delete()
    return redirect('admin-view-employee')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_employee_view(request, pk):
    employee = models.Employee.objects.get(id=pk)
    user = models.User.objects.get(id=employee.user_id)

    userForm = forms.EmployeeUserForm(instance=user)
    employeeForm = forms.EmployeeForm(request.FILES, instance=employee)
    context = {'userForm': userForm, 'employeeForm': employeeForm}

    if request.method == 'POST':
        userForm = forms.EmployeeUserForm(request.POST, instance=user)
        employeeForm = forms.EmployeeForm(request.POST, request.FILES, instance=employee)
        if userForm.is_valid() and employeeForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            employee = employeeForm.save(commit=False)
            employee.status = True
            employee.save()
            return redirect('admin-view-employee')
    return render(request, 'company/admin_update_employee.html', context=context)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_employee_view(request):
    userForm = forms.EmployeeUserForm()
    employeeForm = forms.EmployeeForm()
    context = {'userForm': userForm, 'employeeForm': employeeForm}

    if request.method == 'POST':
        userForm = forms.EmployeeUserForm(request.POST)
        employeeForm = forms.EmployeeForm(request.POST, request.FILES)
        if userForm.is_valid() and employeeForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            employee = employeeForm.save(commit=False)
            employee.user = user
            employee.status = True
            employee.save()

            my_employee_group, created = Group.objects.get_or_create(name='EMPLOYEE')
            my_employee_group.user_set.add(user)

            return redirect('admin-view-employee')
    return render(request, 'company/admin_add_employee.html', context=context)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_employee_view(request):
    # Retrieve employees who need approval
    employees = models.Employee.objects.filter(status=False)
    return render(request, 'company/admin_approve_employee.html', {'employees': employees})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_employee_view(request, pk):
    employee = models.Employee.objects.get(id=pk)
    employee.status = True
    employee.save()
    return redirect(reverse('admin-approve-employee'))

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_employee_view(request, pk):
    employee = models.Employee.objects.get(id=pk)
    user = models.User.objects.get(id=employee.user_id)
    user.delete()
    employee.delete()
    return redirect('admin-approve-employee')

#-------------------------------------------------admin task view----------------------------------------------#

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_task_view(request):
    return render(request, 'company/admin_task.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_task(request):
    # Fetch filters from the request
    status = request.GET.get('status', '')
    manager_id = request.GET.get('manager', '')
    employee_id = request.GET.get('employee', '')
    priority = request.GET.get('priority', '')

    # Filter tasks based on query parameters
    tasks = models.Task.objects.all()
    
    if status:
        tasks = tasks.filter(status=status)
    if manager_id:
        tasks = tasks.filter(manager__id=manager_id)
    if employee_id:
        tasks = tasks.filter(assigned_to__id=employee_id)
    if priority:
        tasks = tasks.filter(priority=priority)

    managers = models.Manager.objects.all()
    employees = models.Employee.objects.all()

    context = {
        'tasks': tasks,
        'managers': managers,
        'employees': employees,
        'status': status,
        'manager_id': manager_id,
        'employee_id': employee_id,
        'priority': priority,
    }

    return render(request, 'company/admin_view_task.html', context=context)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_assign_task(request, task_id):
    # If task_id is provided, fetch the task object from the database
    if task_id:
        task = models.Task.objects.get(id=task_id)
    else:
        task = None

    if request.method == 'POST':
        # Process form submission to create or update the task
        form = forms.TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('admin-view-tasks')  # Redirect to task list
    else:
        # Load form with existing task data if task exists, or an empty form for a new task
        form = forms.TaskForm(instance=task)

    return render(request, 'company/admin_assign_task.html', {'form': form, 'task': task})













#--------------------------------manager-view------------------------------------------#


from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from . import models

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from . import models

@login_required(login_url='managerlogin')
@user_passes_test(is_manager)
def manager_dashboard_view(request):
    # Fetch the number of employees under the logged-in manager
    employeecount = models.Employee.objects.filter(status=True, assignedManager=request.user.manager).count()
    
    # Fetch the total number of attendance records for employees under the manager
    attendance_count = models.Attendance.objects.filter(employee__assignedManager=request.user.manager).count()
    
    # Fetch the total number of tasks assigned by the manager
    task_count = models.Task.objects.filter(manager=request.user.manager).count()

    # Count pending tasks (tasks with status 'Open' or 'In Progress')
    pending_task_count = models.Task.objects.filter(manager=request.user.manager).exclude(status='Completed').count()
    
    # Fetch recent tasks assigned to employees
    tasks = models.Task.objects.filter(manager=request.user.manager).select_related('employee').order_by('-created_at')[:10]

    # Context to be passed to the template
    context = {
        'employeecount': employeecount,
        'attendance_count': attendance_count,
        'task_count': task_count,
        'pending_task_count': pending_task_count,
        'manager': models.Manager.objects.get(user_id=request.user.id),  # Profile picture for the sidebar
        'tasks': tasks,
    }

    return render(request, 'company/manager_dashboard.html', context)


@login_required(login_url='managerlogin')
@user_passes_test(is_manager)
def manager_employee_view(request):
    mydict={
    'manager':models.Manager.objects.get(user_id=request.user.id), #for profile picture of manager in sidebar
    }
    return render(request,'company/manager_employee.html',context=mydict)


@login_required(login_url='managerlogin')
@user_passes_test(is_manager)
def manager_view_employee_view(request):
    # Get all active employees assigned to the manager
    employees = models.Employee.objects.filter(status=True, assignedManagerId=request.user.id)
    manager = models.Manager.objects.get(user_id=request.user.id)  # For profile picture of manager in sidebar

    return render(request, 'company/manager_view_employee.html', {'employees': employees, 'manager': manager})

