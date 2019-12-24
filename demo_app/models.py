from django.db import models

from sample_project.soft_deletion_helper import SoftDeletionModel


class VeryImportantSomething(SoftDeletionModel):
    name = models.CharField(max_length=112, null=True, blank=True)
    city = models.CharField(max_length=112, null=True, blank=True)

    def __str__(self):
        return f"{self.name}-{self.city}"
