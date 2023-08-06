from django.utils.translation import gettext_lazy

try:
    from pretix.base.plugins import PluginConfig
except ImportError:
    raise RuntimeError("Please use pretix 2.7 or above to run this plugin!")

__version__ = "1.0.0"


class PluginApp(PluginConfig):
    name = "pretix_ldap_mails"
    verbose_name = "LDAP mails"

    class PretixPluginMeta:
        name = gettext_lazy("LDAP mails")
        author = "strifel"
        description = gettext_lazy("Verify user supplied mails against LDAP")
        visible = True
        version = __version__
        category = "CUSTOMIZATION"
        compatibility = "pretix>=2.7.0"

    def ready(self):
        from . import signals  # NOQA


default_app_config = "pretix_ldap_mails.PluginApp"
