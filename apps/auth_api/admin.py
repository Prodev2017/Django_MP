from django.contrib import admin

from apps.auth_api.models import BlockChain, User


class BlockhainAdmin(admin.ModelAdmin):
    pass


admin.site.register(User)
admin.site.register(BlockChain, BlockhainAdmin)
