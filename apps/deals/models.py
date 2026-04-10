from django.db import models

 from dirtyfields import DirtyFieldsMixin
from simple_history.models import HistoricalRecords
from apps.contacts.models import Company, Contact


class Pipeline(models.Model):
    """Sales pipeline definition."""

    name = models.CharField(max_length=255, unique=True)
    type = models.CharField(
        max_length=20,
        choices=[("hunting", "Hunting"), ("farming", "Farming")],
        default="hunting",
    )
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Pipeline"
        verbose_name_plural = "Pipelines"

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class Stage(models.Model):
    """Pipeline stage."""

    pipeline = models.ForeignKey(
        Pipeline, on_delete=models.CASCADE, related_name="stages"
    )
    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    is_terminal = models.BooleanField(
        default=False,
        help_text="Terminal stages (Won, Lost) don't allow further transitions",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["pipeline", "order"]
        unique_together = ("pipeline", "name")
        verbose_name = "Stage"
        verbose_name_plural = "Stages"

    def __str__(self):
        return f"{self.pipeline.name} > {self.name}"


class Deal(DirtyFieldsMixin, models.Model):
    """Sales deal."""

    pipeline = models.ForeignKey(
        Pipeline, on_delete=models.PROTECT, related_name="deals"
    )
    current_stage = models.ForeignKey(
        Stage,
        on_delete=models.PROTECT,
        related_name="deals",
        null=True,
        blank=True,
        help_text="Current stage in the pipeline",
    )
    company = models.ForeignKey(
        Company, on_delete=models.PROTECT, related_name="deals"
    )
    contact = models.ForeignKey(
        Contact, on_delete=models.SET_NULL, null=True, blank=True, related_name="deals"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default="USD")
    probability = models.IntegerField(default=0, help_text="Percentage 0-100")
    expected_close_date = models.DateField(null=True, blank=True)
    closed_date = models.DateField(null=True, blank=True)
    won_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    created_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_deals",
    )
    owner = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, related_name="owned_deals"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["-expected_close_date", "-created_at"]
        verbose_name = "Deal"
        verbose_name_plural = "Deals"
        indexes = [
            models.Index(fields=["current_stage"]),
            models.Index(fields=["company"]),
            models.Index(fields=["owner"]),
        ]

    def __str__(self):
        return f"{self.title} - {self.company.name}"

    def save(self, *args, **kwargs):
        """Model-level guard against direct stage manipulation."""
        # Check if current_stage was directly changed
        if self.is_dirty(check_relationship=True) and "current_stage" in self.get_dirty_fields():
            raise RuntimeError(
                "Stage transitions must only go through TransitionService. "
                "Use DealService.transition_deal() instead."
            )
        super().save(*args, **kwargs)

    @property
    def is_won(self):
        return self.current_stage and self.current_stage.name.lower() in [
            "won",
            "closed-won",
        ]

    @property
    def is_lost(self):
        return self.current_stage and self.current_stage.name.lower() in [
            "lost",
            "closed-lost",
        ]

    @property
    def is_closed(self):
        return self.is_won or self.is_lost
