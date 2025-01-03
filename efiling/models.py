# from django.db import models
# from users.models import Citizen
# from cases.models import Case


# class eFiling(models.Model):
#     citizen = models.ForeignKey(
#         Citizen, related_name="efiling", on_delete=models.CASCADE)
#     case = models.ForeignKey(
#         Case, related_name="efilings", on_delete=models.CASCADE)
#     filing_date = models.DateTimeField(auto_now_add=True)
#     document = models.FileField(upload_to='efilings/%Y/%m/%d/')
#     status = models.CharField(max_length=20, choices=[('PENDING', 'Pending'), (
#         'APPROVED', 'Approved'), ('REJECTED', 'Rejected')], default='PENDING')

#     def __str__(self):
#         return f"eFiling for {self.case.case_number} by {self.citizen.username}"