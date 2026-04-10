"""
Service layer for deals - all business logic goes through here.
"""

from django.db import transaction
from django.core.cache import cache
from apps.deals.models import Deal, Pipeline, Stage
from apps.activities.models import AuditLog
from django.contrib.contenttypes.models import ContentType


class DealService:
    """Service for deal operations."""

    @staticmethod
    @transaction.atomic
    def create_deal(
        pipeline,
        company,
        contact,
        title,
        amount,
        currency="USD",
        probability=0,
        expected_close_date=None,
        owner=None,
        created_by=None,
    ):
        """Create a new deal with proper initialization."""
        # Get the first stage
        initial_stage = pipeline.stages.order_by("order").first()
        if not initial_stage:
            raise ValueError(f"Pipeline {pipeline.name} has no stages defined")

        # Create deal
        deal = Deal.objects.create(
            pipeline=pipeline,
            current_stage=initial_stage,
            company=company,
            contact=contact,
            title=title,
            amount=amount,
            currency=currency,
            probability=probability,
            expected_close_date=expected_close_date,
            owner=owner,
            created_by=created_by,
        )

        # Log audit trail
        AuditLog.objects.create(
            user=created_by,
            action="create",
            entity_type=ContentType.objects.get_for_model(Deal),
            entity_id=deal.id,
            changes={"all": "created"},
        )

        # Invalidate cache
        _invalidate_dashboard_cache()

        return deal

    @staticmethod
    @transaction.atomic
    def update_deal(deal, **kwargs):
        """Update deal fields with audit trail."""
        old_values = {
            field: getattr(deal, field)
            for field in kwargs.keys()
            if hasattr(deal, field)
        }

        for field, value in kwargs.items():
            if hasattr(deal, field):
                setattr(deal, field, value)

        deal.save()

        # Log changes
        AuditLog.objects.create(
            user=kwargs.get("updated_by"),
            action="update",
            entity_type=ContentType.objects.get_for_model(Deal),
            entity_id=deal.id,
            changes=old_values,
        )

        # Invalidate cache
        _invalidate_dashboard_cache()

        return deal


class TransitionService:
    """Service for deal stage transitions - CRITICAL for business logic."""

    @staticmethod
    @transaction.atomic
    def transition_stage(deal, new_stage, user=None):
        """Transition deal to a new stage with strict guards."""
        # Check if current stage is terminal
        if deal.current_stage and deal.current_stage.is_terminal:
            raise ValueError(
                f"Cannot transition from terminal stage: {deal.current_stage.name}"
            )

        # Validate new stage is in same pipeline
        if new_stage.pipeline_id != deal.pipeline_id:
            raise ValueError(
                f"Stage {new_stage.name} is not in pipeline {deal.pipeline.name}"
            )

        old_stage = deal.current_stage
        
        # Direct update bypass our guard by using raw update
        # We'll catch this in post_save
        Deal.objects.filter(pk=deal.id).update(current_stage=new_stage)
        deal.refresh_from_db()

        # Audit log the transition
        AuditLog.objects.create(
            user=user,
            action="transition",
            entity_type=ContentType.objects.get_for_model(Deal),
            entity_id=deal.id,
            changes={
                "old_stage": old_stage.name if old_stage else None,
                "new_stage": new_stage.name,
            },
        )

        # Invalidate cache
        _invalidate_dashboard_cache()

        return deal


def _invalidate_dashboard_cache():
    """Invalidate all dashboard caches when deals change."""
    cache_keys = [
        "dashboard_summary_viewer",
        "dashboard_summary_rep",
        "dashboard_summary_manager",
        "dashboard_summary_admin",
    ]
    cache.delete_many(cache_keys)
