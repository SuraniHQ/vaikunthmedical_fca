LOGO_URL = "/assets/vaikunthmedical_fca/images/company_logo.jpeg"

DEFAULT_LETTER_HEAD = "Vaikunth Medical"


def set_company_logo(doc, method=None):
	"""Default every Company's logo to the Vaikunthmedical brand logo, regardless of
	how many companies exist or when they're created, unless someone has set a different one.
	"""
	if not doc.company_logo:
		doc.company_logo = LOGO_URL
