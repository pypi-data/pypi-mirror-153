from django.utils.translation import gettext_lazy
from wagtail.admin.wagtail_hooks import hooks
from wagtail.admin.panels import set_default_page_edit_handlers, ObjectList, TabbedInterface
from wagtail.utils.decorators import cached_classmethod

from wagtail_admin_preview.panels import AdminPreviewPanel


@cached_classmethod
def get_edit_handler(cls):
	"""
	Get the panel to use in the Wagtail admin when editing this page type.
	:param cls:
	:return:
	"""

	if hasattr(cls, "edit_handler"):
		edit_handler = cls.edit_handler
	else:
		# construct a TabbedInterface made up of content_panels, promote_panels
		# and settings_panels, skipping any which are empty
		tabs = []
		if cls.content_panels:
			tabs.append(ObjectList(cls.content_panels, heading=gettext_lazy("Content")))
		if cls.preview_panels:
			tabs.append(
				ObjectList(
					cls.preview_panels,
					heading=gettext_lazy("Preview"),
					classname="preview",
				)
			)
			edit_handler = TabbedInterface(tabs, base_form_class=cls.base_form_class)
		if cls.promote_panels:
			tabs.append(ObjectList(cls.promote_panels, heading=gettext_lazy("Promote")))
		if cls.settings_panels:
			tabs.append(
				ObjectList(
					cls.settings_panels,heading=gettext_lazy("Settings"),classname="settings",
				)
			)
	return edit_handler.bind_to_model(cls)


def add_preview_panel(cls):
	"""
	Add the preview panel to the default set of panels in wagtail page editor
	:param cls:
	:return:
	"""
	set_default_page_edit_handlers(cls)
	cls.preview_panels = [
		AdminPreviewPanel('Live Preview', classname='full')
	]


@hooks.register("register_icons")
def register_icons(icons):
    return icons + [
		 'wagtailadmin/icons/mobile-screen.svg',
		 'wagtailadmin/icons/tablet-screen.svg',
		 'wagtailadmin/icons/desktop-screen.svg'
	 ]