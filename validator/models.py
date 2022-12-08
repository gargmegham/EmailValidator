from django.db import models

class emailFiles(models.Model):
    file = models.FileField()
    is_processed = models.BooleanField(default=False)
    name = models.CharField(unique=True, max_length=20)

    def __str__(self):
        return self.file.name