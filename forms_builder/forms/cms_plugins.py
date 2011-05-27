from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext as _

from forms_builder.forms.forms import FormForForm

from .admin import FormAdmin
from .models import CMSForm, Field


class FieldAdmin(admin.StackedInline):
    model = Field

class CMSFormPlugin(CMSPluginBase):
    model = CMSForm
    name = _("Form")
    render_template = "forms/form_plugin.html"

    inlines = (FieldAdmin,)
    radio_fields = FormAdmin.radio_fields
    fieldsets = [(_("CMS Specific"), {"fields": (('csrf', 'action'),)},),] + FormAdmin.fieldsets

    def render(self, context, instance, placeholder):
        args = (instance, None, None)
        form_for_form = FormForForm(*args)
        context.update({
            "form": instance,
            "form_for_form": form_for_form,
        })
        return context

plugin_pool.register_plugin(CMSFormPlugin)