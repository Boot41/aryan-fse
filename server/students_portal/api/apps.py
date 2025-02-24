from django.apps import AppConfig
from django.db.models.signals import post_migrate

def populate_sample_data(sender, **kwargs):
    # Import here to avoid circular import
    from django.core.management import call_command
    call_command('populate_sample_data')

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        post_migrate.connect(populate_sample_data, sender=self)
