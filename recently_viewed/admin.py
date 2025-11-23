from django.contrib import admin
from .models import RecentlyViewed


class RecentlyViewedAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'timestamp')
    list_filter = ('user', 'timestamp')


admin.site.register(RecentlyViewed, RecentlyViewedAdmin)
