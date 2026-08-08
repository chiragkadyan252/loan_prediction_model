from django.db import models
from django.contrib.auth.models import User


class Prediction(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    no_of_dependents = models.IntegerField()
    education = models.IntegerField()
    self_employed = models.IntegerField()
    income_annum = models.FloatField()
    loan_amount = models.FloatField()
    loan_term = models.FloatField()
    cibil_score = models.FloatField()
    residential_assets_value = models.FloatField()
    commercial_assets_value = models.FloatField()
    luxury_assets_value = models.FloatField()
    bank_asset_value = models.FloatField()

    result = models.CharField(max_length=30)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.result