from django.db import models

class CommonMailingList(models.Model):
    email = models.EmailField(db_index=True)
    user = models.ForeignKey("user_management.CustomUser", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.email} of mailing list"
