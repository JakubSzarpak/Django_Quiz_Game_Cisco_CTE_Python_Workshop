# DATABASE FIELDS DOWN BELOW AND PK,FK

from django.db import models # type: ignore
import uuid

class Participant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    score = models.IntegerField()
    taken_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}: {self.score}"