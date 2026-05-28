from django.core.exceptions import ValidationError
from django.db import models


class TravelProject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if self.project_places.filter(visited=True).exists():
            raise ValidationError("Can not delete a project with already visited places.")
        super().delete(*args, **kwargs)


class ProjectPlace(models.Model):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(
        TravelProject,
        on_delete=models.CASCADE,
        related_name="project_places"
    )
    external_id = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    visited = models.BooleanField(default=False)

    class Meta:
        unique_together = ("project", "external_id")

    def __str__(self):
        return f"{self.name} - {self.project.name}"
