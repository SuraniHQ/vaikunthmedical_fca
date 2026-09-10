import frappe

from vaikunthmedical_fca.branding import DEFAULT_LETTER_HEAD, LOGO_URL


def execute():
	"""Apply the Vaikunthmedical logo everywhere it can appear in the desk/website,
	and to every Company that exists, regardless of which company it is.
	"""
	website_settings = frappe.get_single("Website Settings")
	website_settings.app_logo = LOGO_URL
	website_settings.banner_image = LOGO_URL
	website_settings.favicon = LOGO_URL
	website_settings.footer_logo = LOGO_URL
	website_settings.save(ignore_permissions=True)

	navbar_settings = frappe.get_single("Navbar Settings")
	navbar_settings.app_logo = LOGO_URL
	navbar_settings.save(ignore_permissions=True)

	if frappe.db.exists("Letter Head", DEFAULT_LETTER_HEAD):
		letter_head = frappe.get_doc("Letter Head", DEFAULT_LETTER_HEAD)
	else:
		letter_head = frappe.new_doc("Letter Head")
		letter_head.letter_head_name = DEFAULT_LETTER_HEAD

	letter_head.source = "Image"
	letter_head.image = LOGO_URL
	letter_head.is_default = 1
	letter_head.save(ignore_permissions=True)

	for company in frappe.get_all("Company", pluck="name"):
		frappe.db.set_value("Company", company, "company_logo", LOGO_URL)
