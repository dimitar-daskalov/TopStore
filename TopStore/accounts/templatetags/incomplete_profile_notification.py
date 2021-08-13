from django.template import Library

from TopStore.accounts.models import Profile

register = Library()


@register.inclusion_tag('template_tags/incomplete_profile_notification.html', takes_context=True)
def incomplete_profile_notification(context):
    profile = Profile.objects.get(pk=context.request.user.id)

    return {
        'is_profile_completed': profile.is_profile_completed,
    }
