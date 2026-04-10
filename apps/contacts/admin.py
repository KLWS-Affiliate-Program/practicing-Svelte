from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Company, Contact


@admin.register(Company)
class CompanyAdmin(SimpleHistoryAdmin):
    list_display = ("name", "industry", "city", "is_active", "is_deleted", "created_at")
    list_filter = ("is_active", "is_deleted", "industry", "country")
    search_fields = ("name", "website", "city")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Basic Info", {"fields": ("name", "industry", "website", "phone")}),
        ("Address", {"fields": ("address", "city", "state", "country", "postal_code")}),
        ("Status", {"fields": ("is_active", "is_deleted")}),
        ("Timestamps", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )


@admin.register(Contact)
class ContactAdmin(SimpleHistoryAdmin):
    list_display = ("full_name", "email", "company", "title", "source", "is_active", "created_at")
    list_filter = ("is_active", "is_deleted", "source", "department")
    search_fields = ("first_name", "last_name", "email", "company__name")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Personal Info", {"fields": ("first_name", "last_name", "email", "phone")}),
        ("Professional", {"fields": ("company", "title", "department")}),
        ("Contact Info", {"fields": ("source", "notes")}),
        ("Status", {"fields": ("is_active", "is_deleted")}),
        ("Timestamps", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def full_name(self, obj):
        return obj.full_name

    full_name.short_description = "Name"
