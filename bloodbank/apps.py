from django.apps import AppConfig


class BloodbankConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bloodbank'

    def ready(self):
        import bloodbank.signals

# class BloodbankConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'bloodbank'

#     def ready(self):
#         import bloodbank.signals  # This will import signals.py file
