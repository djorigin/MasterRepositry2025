from django.contrib import admin
from .models import SystemCoreColourCode

@admin.register(SystemCoreColourCode)
class SystemCoreColourCodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'hex_code', 'rgb_value',)
    list_display_links = ('name',)
    search_fields = ('name', 'hex_code', 'rgb_value')
    list_filter = ('hex_code',)
    ordering = ('name',)
    readonly_fields = ()
    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
        ('Color Information', {
            'fields': ('hex_code', 'rgb_value'),
            'description': 'Hex and RGB values must be unique and valid.'
        }),
    )
    # Optionally, add actions or custom admin methods here

    # Example: Custom validation or save logic in admin
    def save_model(self, request, obj, form, change):
        obj.full_clean()  # Ensures model validation in admin
        super().save_model(request, obj, form, change)
