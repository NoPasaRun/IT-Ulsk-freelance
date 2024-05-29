from django.db import models
from django.contrib.auth.models import User

from admin_panel.sqlalchemy_models import Company


class CompanyUser(User):
    company = models.ForeignKey(Company, related_name='users', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'company_user'
        verbose_name = "Учетка компании"
        verbose_name_plural = "Учетки компании"

    def __str__(self):
        return f"{self.company.name} №_{self.id}"
