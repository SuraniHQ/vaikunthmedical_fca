import frappe
from frappe.utils import flt


def apply_scm_to_rate(doc, method=None):
	"""Let "SCM" (a flat per-line scheme discount) reduce Rate, applied
	pre-tax, so GST calculates on the post-SCM amount. Confirmed against a
	real supplier invoice: their own math is (Qty x Rate - SCM), GST added
	on that, and the % discount applied *afterward* on the grand total -
	not per row. So Discount % is deliberately not handled here at all;
	use ERPNext's native "Apply Additional Discount On: Grand Total" +
	"Additional Discount Percentage" on the document header for that part
	instead - no custom code needed, and it reconciles exactly with how
	the source invoice computes its own total.

	Runs in before_validate, ahead of core's own tax calculation.

	Rate is a persisted field, so a naive per-save delta on SCM alone
	would double-subtract on resave. Instead, custom_scm_rate_anchor
	(hidden) holds Rate as it was before any SCM reduction, frozen once,
	and Rate is recomputed fresh from it every time: anchor - SCM / qty.
	That's stateless and idempotent - re-saving without changes, or
	changing SCM later, always recomputes correctly with no drift.
	"""
	for row in doc.items:
		scm = flt(row.custom_scm_amount)
		if not scm:
			continue

		qty = flt(row.qty) or 1

		if not flt(row.custom_scm_rate_anchor):
			row.custom_scm_rate_anchor = flt(row.price_list_rate) or flt(row.rate)

		row.rate = flt(row.custom_scm_rate_anchor) - (scm / qty)


def set_total_scm_amount(doc, method=None):
	"""Sum SCM across all item rows into the read-only header total."""
	doc.custom_total_scm_amount = sum(flt(row.custom_scm_amount) for row in doc.items)
