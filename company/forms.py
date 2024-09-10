from django import forms
from django.contrib.auth.models import User
from . import models

#for admin signup (no changes)
class AdminSignupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

#for manager (doctor) related form
class ManagerUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class ManagerForm(forms.ModelForm):
    class Meta:
        model=models.Manager
        fields=['address','mobile','department','status','profile_pic']

#for employee (patient) related form
class EmployeeUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

class EmployeeForm(forms.ModelForm):
    assignedManager = forms.ModelChoiceField(
        queryset=models.Manager.objects.filter(status=True),
        empty_label="Name and Department",
        to_field_name="user_id"
    )
    
    class Meta:
        model = models.Employee
        fields = ['address', 'mobile', 'role', 'department', 'profile_pic', 'assignedManager']

class TaskForm(forms.ModelForm):
    employee = forms.ModelChoiceField(queryset=models.Employee.objects.all().filter(status=True), empty_label="Select Employee", to_field_name="user_id")

    class Meta:
        model = models.Task
        fields = ['title', 'description', 'priority', 'status', 'deadline']
        

# class ManagerPerformanceReviewForm(forms.ModelForm):
#     employeeId = forms.ModelChoiceField(
#         queryset=models.Employee.objects.all().filter(status=True),
#         empty_label="Select Employee",
#         to_field_name="id"  # Assuming 'id' is the primary key in the Employee model
#     )
    
#     class Meta:
#         model = models.PerformanceReview
#         fields = ['employeeId', 'feedback', 'status']  # Use actual fields from PerformanceReview model

# class EmployeePerformanceReviewForm(forms.ModelForm):
#     managerId = forms.ModelChoiceField(
#         queryset=models.Manager.objects.all().filter(status=True),
#         empty_label="Select Manager",
#         to_field_name="id"  # Assuming 'id' is the primary key in the Manager model
#     )

    # class Meta:
    #     model = models.PerformanceReview
    #     fields = ['managerId', 'feedback', 'status']  # Use actual fields from PerformanceReview model




class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))
