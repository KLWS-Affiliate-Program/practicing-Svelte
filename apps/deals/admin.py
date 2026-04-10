from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Pipeline, Stage, Deal


@admin.register(Pipeline)
class PipelineAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "created_at")
    list_filter = ("type",)
    search_fields = ("name",)


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ("name", "pipeline", "order", "is_terminal")
    list_filter = ("pipeline", "is_terminal")
    search_fields = ("name", "pipeline__name")
    ordering = ("pipeline__name", "order")


@admin.register(Deal)
class DealAdmin(SimpleHistoryAdmin):
    list_display = ("title", "company", "current_stage", "amount", "owner", "created_at")
    list_filter = ("pipeline", "current_stage", "owner", "is_won", "is_lost")
    search_fields = ("title", "company__name", "owner__email")
    readonly_fields = ("created_at", "updated_at", "created_by", "is_closed")
    fieldsets = (
        ("Deal Info", {"fields": ("title", "description", "pipeline", "current_stage")}),
        ("Company & Contact", {"fields": ("company", "contact")}),
        ("Financial", {"fields": ("amount", "currency", "probability", "won_amount")}),
        (
            "Timeline",
            {"fields": ("expected_close_date", "closed_date")},
        ),
        (
            "Ownership",
            {
                "fields": ("owner", "created_by"),
            },
        ),
        ("Status", {"fields": ("is_closed",), "classes": ("collapse",)}),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )
