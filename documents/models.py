
from django.db import models
from cases.models import Case


class Document(models.Model):
    case = models.ForeignKey(Case, related_name="document_files",
                             on_delete=models.CASCADE)  # Updated related_name
    document_type = models.CharField(max_length=100)
    file = models.FileField(upload_to='documents/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.document_type} for Case {self.case.case_number}"