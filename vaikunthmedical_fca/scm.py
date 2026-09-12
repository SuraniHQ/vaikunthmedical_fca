import frappe
from frappe.utils import flt


def neutralize_discount_percentage(doc, method=None):
	"""Freeze whatever Discount % was typed into a hidden anchor, then zero
	the native field before core ever processes it. Core's own Discount %
	handling works by reducing Rate (via Price List Rate), so zeroing it
	before core's validate() runs means core never touches Rate at all.
	Runs in before_validate, ahead of core's own reconciliation - the
	*first* pass where discount_percentage is still genuinely non-zero
	freezes the anchor; on later passes it already reads 0 (from us, not
	the user clearing it), so the existing anchor is left alone.
	"""
	for row in doc.items:
		discount_percentage = flt(row.discount_percentage)
		if discount_percentage:
			row.custom_disc_percent_anchor = discount_percentage
			row.discount_percentage = 0


def apply_scm_and_discount_to_amount(doc, method=None):
	"""Let Discount % (frozen in custom_disc_percent_anchor) and SCM both
	reduce Amount directly - Rate is never touched by either. Runs in
	"validate", after core has already computed Amount fresh from
	qty x rate (unaffected by Discount %, since neutralize_discount_
	percentage zeroed the native field before core's calculation ran).
	Amount is recomputed by core from scratch on *every* validate, so the
	full deduction is computed fresh every time here too - nothing to
	double-count against.

	Note: since Rate is never touched, core calculates GST/tax rows on
	the full, undiscounted amount - not the amount after Discount % or
	SCM. Deliberate trade-off: GST will not match a supplier invoice that
	charges GST on the discounted value.
	"""
	conversion_rate = flt(doc.conversion_rate) or 1
	total_deduction = 0.0
	total_base_deduction = 0.0

	for row in doc.items:
		base_amount = flt(row.amount)
		discount_value = base_amount * flt(row.custom_disc_percent_anchor) / 100.0
		scm = flt(row.custom_scm_amount)
		deduction = discount_value + scm

		if deduction:
			base_deduction = deduction * conversion_rate

			row.amount = base_amount - deduction
			row.net_amount = flt(row.net_amount) - deduction
			row.base_amount = flt(row.base_amount) - base_deduction
			row.base_net_amount = flt(row.base_net_amount) - base_deduction

			total_deduction += deduction
			total_base_deduction += base_deduction

	if total_deduction:
		doc.total = flt(doc.total) - total_deduction
		doc.net_total = flt(doc.net_total) - total_deduction
		doc.grand_total = flt(doc.grand_total) - total_deduction
		if doc.rounded_total:
			doc.rounded_total = flt(doc.rounded_total) - total_deduction

		doc.base_total = flt(doc.base_total) - total_base_deduction
		doc.base_net_total = flt(doc.base_net_total) - total_base_deduction
		doc.base_grand_total = flt(doc.base_grand_total) - total_base_deduction
		if doc.base_rounded_total:
			doc.base_rounded_total = flt(doc.base_rounded_total) - total_base_deduction


def set_total_scm_amount(doc, method=None):
	"""Sum SCM across all item rows into the read-only header total."""
	doc.custom_total_scm_amount = sum(flt(row.custom_scm_amount) for row in doc.items)
