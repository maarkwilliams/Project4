from django.apps import AppConfig


class WishlistConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wishlist'


class WishlistConfig(AppConfig):
    name = 'wishlist'

    def ready(self):
        import wishlist.signals
