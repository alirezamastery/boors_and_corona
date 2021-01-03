from django.contrib import admin

from .models import BlockedIp, SecurityConfig, ViewDetail


# Register your models here.

@admin.register(BlockedIp)
class BlockedIpAdmin(admin.ModelAdmin):
    list_display = ('id', 'ip', 'rps', 'view', 'ban_time', 'created_at')

    # Your code
    list_filter = ['view']
    search_fields = ['ip', 'view__path', 'view__name']

    list_display_links = ('id', 'ip')


@admin.register(SecurityConfig)
class SecurityConfigAdmin(admin.ModelAdmin):

    # Your code
    def has_add_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ViewDetail)
class ViewDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'path')

    search_fields = ('name', 'path')

    # Your code
    def has_add_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False
