from django.db import models
from users.models import Lawyer, Judge, Citizen


class Case(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACTIVE', 'Active'),
        ('DISMISSED', 'Dismissed'),
        ('CLOSED', 'Closed'),
    ]
    case_number = models.CharField(max_length=50, unique=True)
    plaintiff = models.ForeignKey(
        Citizen, related_name="plaintiff_cases", on_delete=models.CASCADE)
    defendant = models.ForeignKey(
        Citizen, related_name="defendant_cases", on_delete=models.CASCADE)
    assigned_lawyer = models.ForeignKey(
        Lawyer, related_name="cases", on_delete=models.SET_NULL, null=True, blank=True)
    assigned_judge = models.ForeignKey(
        Judge, related_name="cases", on_delete=models.SET_NULL, null=True, blank=True)
    case_title = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='PENDING')
    case_filed_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Case {self.case_number} - {self.case_title}"


class Hearing(models.Model):
    case = models.ForeignKey(
        Case, related_name="hearings", on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=100)
    outcome = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Hearing for {self.case.case_number} on {self.date} at {self.time}"


class Document(models.Model):
    case = models.ForeignKey(Case, related_name="case_documents",
                             on_delete=models.CASCADE)  # Updated related_name
    document_type = models.CharField(max_length=100)
    file = models.FileField(upload_to='documents/%Y/%m/%d/')
    uploaded_by = models.ForeignKey(
        Citizen, related_name="uploaded_documents", on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document {self.document_type} for {self.case.case_number}"