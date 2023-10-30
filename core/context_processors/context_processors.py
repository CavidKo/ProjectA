from core.models import Settings, Logo


def settings(request):
    context = {
        'footer_info': Settings.objects.first(),
        'logo': Logo.objects.first()
    }

    return context