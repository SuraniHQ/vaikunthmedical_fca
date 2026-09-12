from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def _item_field():
	return {
		"fieldname": "custom_disc_percent",
		"label": "Disc % (post-tax)",
		"fieldtype": "Percent",
		"insert_after": "custom_scm_amount",
		"in_list_view": 1,
		"description": (
			"Discount % for this line only, applied after GST - matches how the supplier "
			"invoices this was built against compute their own totals: (Qty x Rate - SCM), "
			"GST added, then this % taken off. Different rows can use different percentages."
		),
	}


def _total_field():
	return {
		"fieldname": "custom_total_disc_amount",
		"label": "Total Disc Amount (post-tax)",
		"fieldtype": "Currency",
		"insert_after": "custom_total_scm_amount",
		"read_only": 1,
		"description": "Sum of the post-tax Disc % deduction across all item rows.",
	}


def execute():
	create_custom_fields(
		{
			"Purchase Receipt Item": [_item_field()],
			"Purchase Invoice Item": [_item_field()],
		}
	)
	create_custom_fields(
		{
			"Purchase Receipt": [_total_field()],
			"Purchase Invoice": [_total_field()],
		}
	)
