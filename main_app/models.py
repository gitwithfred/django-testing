from django.db import models


class MainModel(models.Model):
    file = models.FileField(
        # unique=True,
        # upload_to='uploads/%Y/%m/%d/',
    )

    def __str__(self):
        return self.file.name
