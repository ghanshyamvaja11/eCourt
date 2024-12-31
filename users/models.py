from django.db import models
from django.contrib.auth.models import AbstractUser, Group,  Permission


class User(AbstractUser):
    CONTACT_TYPES = [
        ('PHONE', 'Phone'),
        ('EMAIL', 'Email'),
    ]

    user_type = models.CharField(
        max_length=20,
        choices=[('ADMIN', 'Admin'), ('LAWYER', 'Lawyer'),
                 ('JUDGE', 'Judge'), ('CITIZEN', 'Citizen')],
        default='CITIZEN'
    )
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    contact_type = models.CharField(
        max_length=10, choices=CONTACT_TYPES, default='EMAIL')
    address = models.TextField(blank=True, null=True)

    # Add related_name to avoid conflicts
    groups = models.ManyToManyField(
        Group, related_name='custom_user_set', blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission, related_name='custom_user_permissions_set', blank=True
    )

    def __str__(self):
        return self.username


class Admin(User):
    pass
    def __str__(self):
        return f"Admin - {self.username}"


class Lawyer(User):
    license_number = models.CharField(max_length=50, unique=True)
    law_firm = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Lawyer - {self.username}"


class Judge(User):
    court = models.CharField(max_length=100)
    cases_assigned = models.IntegerField(default=0)

    def __str__(self):
        return f"Judge - {self.username}"


class Citizen(User):
    national_id = models.CharField(max_length=20, unique=True)
    cases_filed = models.IntegerField(default=0)

    def __str__(self):
        return f"Citizen - {self.username}"