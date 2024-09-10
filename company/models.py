from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

departments = [
    ('HR', 'Human Resources'),
    ('IT', 'Information Technology'),
    ('Finance', 'Finance'),
    ('Marketing', 'Marketing'),
    ('Operations', 'Operations'),
    ('Sales', 'Sales')
]

class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/ManagerProfilePic/', null=True, blank=True)
    address = models.CharField(max_length=100)
    mobile = models.CharField(max_length=20, null=True)
    department = models.CharField(max_length=50, choices=departments, default='HR')
    status = models.BooleanField(default=False)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return "{} ({})".format(self.user.first_name, self.department)


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/EmployeeProfilePic/', null=True, blank=True)
    address = models.CharField(max_length=100)
    mobile = models.CharField(max_length=20, null=False)
    role = models.CharField(max_length=100, null=False)
    department = models.CharField(max_length=50, choices=departments)  # Employee department field
    assignedManager = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True, related_name='employees')
    hireDate = models.DateField(auto_now=True)
    status = models.BooleanField(default=False)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return self.user.first_name + " (" + self.role + ")"

    def save(self, *args, **kwargs):
        # Ensure employee's department matches assigned manager's department
        if self.assignedManager:
            if self.assignedManager.department != self.department:
                raise ValueError("Employee's department must match Manager's department.")
        super().save(*args, **kwargs)


# Task Model
class Task(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    priority = models.CharField(
        max_length=10,
        choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')],
        default='Medium'
    )
    status = models.CharField(
        max_length=20,
        choices=[('Open', 'Open'), ('In Progress', 'In Progress'), ('Completed', 'Completed')],
        default='Open'
    )
    deadline = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.employee.user.username}"


# class PerformanceReview(models.Model):
#     employeeId = models.PositiveIntegerField(null=True)
#     managerId = models.PositiveIntegerField(null=True)
#     employeeName = models.CharField(max_length=40, null=True)
#     managerName = models.CharField(max_length=40, null=True)
#     reviewDate = models.DateField(auto_now=True)
#     feedback = models.TextField(max_length=500)
#     status = models.BooleanField(default=False)


class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Leave', 'On Leave')])
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Attendance for {self.employee.get_name} on {self.date}"
