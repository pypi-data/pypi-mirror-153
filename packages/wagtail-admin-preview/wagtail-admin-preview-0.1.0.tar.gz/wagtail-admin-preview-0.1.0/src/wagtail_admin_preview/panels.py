from django.conf import settings
from django.template.loader import get_template
from wagtail.admin.panels import Panel


class AdminPreviewPanel(Panel):
	class BoundPanel(Panel.BoundPanel):
		template_name = 'wagtail_admin_preview/preview_panel.html'
		rendered = None

		def __init__(self, *args, **kwargs):
			super(AdminPreviewPanel.BoundPanel, self).__init__(*args, **kwargs)

		def render_html(self, parent_context=None):
			preview_instance = self.instance.serve_preview(self.request, 'admin_preview')
			template = get_template(preview_instance.template_name)
			self.rendered = template.render(preview_instance.context_data).replace('\n', '')
			panel = get_template(self.template_name)
			if parent_context is None:
				parent_context = {}

			try:
				sizes = settings.__getattr__('WAGTAIL_ADMIN_PREVIEW_BREAKPOINTS')
			except AttributeError:
				sizes = [375, 766, 1278]

			parent_context.update(
				{'self': self, 'sizes': sizes}
			)
			return panel.render(parent_context)
