from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def _field():
	return {
		"fieldname": "custom_disc_percent_anchor",
		"label": "Discount % Anchor",
		"fieldtype": "Percent",
		"insert_after": "custom_scm_amount",
		"hidden": 1,
		"read_only": 1,
		"description": (
			"Internal use only - the Discount % you typed, frozen here before the native "
			"Discount % field is zeroed out to stop it from touching Rate."
		),
	}


def execute():
	create_custom_fields(
		{
			"Purchase Receipt Item": [_field()],
			"Purchase Invoice Item": [_field()],
		}
	)
