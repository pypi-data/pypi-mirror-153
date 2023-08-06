from django.db import models
from edc_constants.choices import YES_NO
from edc_constants.constants import NOT_APPLICABLE, YES

from .choices import PHQ_CHOICES


class Phq9ModelMixin(models.Model):

    ph9_performed = models.CharField(
        verbose_name="Is the PH9 assessment being performed?",
        max_length=15,
        choices=YES_NO,
        default=YES,
    )

    ph9_not_performed_reason = models.TextField(
        verbose_name="If NO, please provide a reason",
        max_length=200,
        null=True,
        blank=True,
    )

    ph9interst = models.CharField(
        verbose_name="Little interest or pleasure in doing things",
        max_length=15,
        choices=PHQ_CHOICES,
        default=NOT_APPLICABLE,
    )

    ph9feel = models.CharField(
        verbose_name="Feeling down, depressed or hopeless",
        max_length=15,
        choices=PHQ_CHOICES,
        default=NOT_APPLICABLE,
    )

    ph9troubl = models.CharField(
        verbose_name="Trouble falling/staying asleep, sleeping too much",
        max_length=15,
        choices=PHQ_CHOICES,
        default=NOT_APPLICABLE,
    )

    ph9tired = models.CharField(
        verbose_name="Feeling tired or having little energy",
        max_length=15,
        choices=PHQ_CHOICES,
        default=NOT_APPLICABLE,
    )
    ph9appetit = models.CharField(
        verbose_name="Poor appetite or over eating",
        max_length=15,
        choices=PHQ_CHOICES,
        default=NOT_APPLICABLE,
    )

    ph9badabt = models.CharField(
        verbose_name=(
            "Feeling bad about yourself or that you are a "
            "failure or have let yourself or your family down"
        ),
        max_length=15,
        choices=PHQ_CHOICES,
        default=NOT_APPLICABLE,
    )

    ph9concen = models.CharField(
        verbose_name=(
            "Trouble concentrating on things such as reading the "
            "newspapers or watching television"
        ),
        max_length=15,
        choices=PHQ_CHOICES,
        default=NOT_APPLICABLE,
    )

    ph9moving = models.CharField(
        verbose_name=(
            "Moving or speaking so slowly  that other people could have "
            "noticed or the opposite: being so fidgety or restless that "
            "you have been moving around a lot more than usual"
        ),
        max_length=15,
        choices=PHQ_CHOICES,
        default=NOT_APPLICABLE,
    )

    ph9though = models.CharField(
        verbose_name=(
            "Thoughts that you would be better off dead or of hurting yourself in some way"
        ),
        max_length=15,
        choices=PHQ_CHOICES,
        default=NOT_APPLICABLE,
    )

    ph9functio = models.CharField(
        verbose_name=(
            "If you checked off any problems on this questionnaire so far, "
            "how difficult have these problems made it for you to do your "
            "work, take care of things at home or get along with other people?"
        ),
        max_length=15,
        choices=PHQ_CHOICES,
        default=NOT_APPLICABLE,
    )

    class Meta:
        abstract = True
        verbose_name = "Patient Health Questionnaire-9 (PHQ-9)"
        verbose_name_plural = "Patient Health Questionnaires-9 (PHQ-9)"
