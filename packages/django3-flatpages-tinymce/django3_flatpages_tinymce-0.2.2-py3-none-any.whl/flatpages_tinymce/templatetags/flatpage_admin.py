import os
import json

# Settings
from django.conf import settings
import tinymce.settings
from flatpages_tinymce import settings as local_settings

from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

register = template.Library()


def is_admin(context):
    return 'user' in context and context['user'].has_perm('flatpages.change_flatpage') \
        and local_settings.USE_FRONTED_TINYMCE


@register.simple_tag(takes_context=True)
def flatpage_media(context):
    if not is_admin(context):
        return ""

    if context.render_context.get("flatpage_media_loaded", None):
        return ""

    media_url = settings.MEDIA_URL

    mce_config = tinymce.settings.DEFAULT_CONFIG.copy()
    mce_config['mode'] = 'exact'
    mce_config['elements'] = f"{local_settings.DIV_PREFIX}_body"
    mce_config['strict_loading_mode'] = 1

    postfix = ""
    if local_settings.USE_MINIFIED:
        postfix = "-min"

    media = {
        'js': [
            os.path.join(media_url, tinymce.settings.JS_URL),
            os.path.join(local_settings.MEDIA_URL, f"edit{postfix}.js")
        ],
        'css': [
                os.path.join(local_settings.MEDIA_URL, f'edit{postfix}.css')
            ],
        }
    if tinymce.settings.USE_FILEBROWSER:
        mce_config['file_browser_callback'] = "djangoFileBrowser"
        media['js'].append(reverse('tinymce-filebrowser'))

    output_chunks = []
    for script in media['js']:
        output_chunks.append(f'<script type="text/javascript" src="{script}" ></script>')

    for stylesheet in media['css']:
        output_chunks.append(
            f'<link rel="stylesheet" href="{stylesheet}" type="text/css" media="screen" />'
        )
    params = {
        'tinymce_config': mce_config,
        'prefix': local_settings.DIV_PREFIX,
        'url': reverse('admin:flatpages_ajax_save'),
        'error_message': _('Error while saving. Please try again.'),
        'csrf_token': str(context['csrf_token']),
    }
    output_chunks.append(
        f'<script type="text/javascript">$_STATICPAGES_INIT({json.dumps(params)})</script>'
    )

    context.render_context["flatpage_media_loaded"] = 1
    return mark_safe("\n".join(output_chunks))


@register.inclusion_tag("flatpages_tinymce/_contentedit.htm", takes_context=True)
def flatpage_admin(context, flatpage):
    media = flatpage_media(context)
    output_content = mark_safe(flatpage.content)
    return {
        'media': media,
        'page_id': flatpage.id,
        'admin': is_admin(context),
        'prefix': local_settings.DIV_PREFIX,
        'content': output_content,
    }
