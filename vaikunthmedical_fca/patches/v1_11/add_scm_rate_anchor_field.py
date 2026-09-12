from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def _field():
	return {
		"fieldname": "custom_scm_rate_anchor",
		"label": "SCM Rate Anchor",
		"fieldtype": "Currency",
		"insert_after": "custom_scm_amount",
		"hidden": 1,
		"read_only": 1,
		"description": (
			"Internal use only - the post-Discount %, pre-SCM rate, frozen so GST calculates "
			"correctly on the post-SCM amount across repeated saves."
		),
	}


def execute():
	create_custom_fields(
		{
			"Purchase Receipt Item": [_field()],
			"Purchase Invoice Item": [_field()],
		}
	)
