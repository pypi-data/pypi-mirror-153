from django.apps import AppConfig


class WagtailAdminPreviewAppConfig(AppConfig):

	name='wagtail_admin_preview'

	def ready(self):
		from wagtail.models import Page
		from wagtail_admin_preview import wagtail_hooks

		wagtail_hooks.add_preview_panel(Page)
		Page.get_edit_handler = wagtail_hooks.get_edit_handler
