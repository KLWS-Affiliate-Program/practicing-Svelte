"""
Service layer for contacts - all contact/company operations.
"""

from django.db import transaction
from django.core.cache import cache
from apps.contacts.models import Contact, Company
from apps.activities.models import AuditLog
from django.contrib.contenttypes.models import ContentType


class ContactService:
    """Service for contact operations."""

    @staticmethod
    @transaction.atomic
    def create_contact(email, first_name, last_name, **kwargs):
        """Create a new contact with duplicate detection."""
        # Check for existing email
        if Contact.objects.filter(email=email, is_deleted=False).exists():
            raise ValueError(f"Contact with email {email} already exists")

        contact = Contact.objects.create(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **kwargs,
        )

        # Audit log
        AuditLog.objects.create(
            user=kwargs.get("created_by"),
            action="create",
            entity_type=ContentType.objects.get_for_model(Contact),
            entity_id=contact.id,
            changes={"all": "created"},
        )

        return contact

    @staticmethod
    @transaction.atomic
    def soft_delete_contact(contact, user=None):
        """Soft delete a contact."""
        contact.is_deleted = True
        contact.is_active = False
        contact.save()

        # Audit log
        AuditLog.objects.create(
            user=user,
            action="delete",
            entity_type=ContentType.objects.get_for_model(Contact),
            entity_id=contact.id,
            changes={"is_deleted": True},
        )

        return contact


class CompanyService:
    """Service for company operations."""

    @staticmethod
    @transaction.atomic
    def create_company(name, **kwargs):
        """Create a new company."""
        if Company.objects.filter(name=name, is_deleted=False).exists():
            raise ValueError(f"Company {name} already exists")

        company = Company.objects.create(name=name, **kwargs)

        # Audit log
        AuditLog.objects.create(
            user=kwargs.get("created_by"),
            action="create",
            entity_type=ContentType.objects.get_for_model(Company),
            entity_id=company.id,
            changes={"all": "created"},
        )

        return company

    @staticmethod
    @transaction.atomic
    def soft_delete_company(company, user=None):
        """Soft delete a company with guards."""
        # Check if company has active deals
        if not company.can_delete():
            raise ValueError(
                f"Cannot delete company with active deals: {company.name}"
            )

        # Unlink contacts without cascading
        company.contacts.all().update(company=None)

        # Soft delete company
        company.is_deleted = True
        company.is_active = False
        company.save()

        # Audit log
        AuditLog.objects.create(
            user=user,
            action="delete",
            entity_type=ContentType.objects.get_for_model(Company),
            entity_id=company.id,
            changes={"is_deleted": True},
        )

        return company
