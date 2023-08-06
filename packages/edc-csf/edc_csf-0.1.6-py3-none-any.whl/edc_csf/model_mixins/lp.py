from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.html import format_html
from edc_constants.choices import YES_NO
from edc_model.validators import datetime_not_future

from ..choices import LP_REASON


class LpModelMixin(models.Model):

    lp_datetime = models.DateTimeField(
        verbose_name="LP Date and Time", validators=[datetime_not_future]
    )

    reason_for_lp = models.CharField(
        verbose_name="Reason for LP", max_length=50, choices=LP_REASON
    )

    opening_pressure_measured = models.CharField(
        verbose_name="Was the opening pressure measured", max_length=25, choices=YES_NO
    )

    opening_pressure = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(99)],
        blank=True,
        null=True,
        help_text=format_html("Units cm of H<sub>2</sub>O"),
    )

    closing_pressure = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(99)],
        help_text=format_html("Units cm of H<sub>2</sub>O"),
    )

    csf_amount_removed = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="CSF amount removed ",
        validators=[MinValueValidator(1)],
        help_text="Units ml",
    )

    class Meta:
        abstract = True
