import frappe
from frappe.utils import flt


def apply_scm_amount(doc, method=None):
	"""Let "SCM" reduce Amount directly. Rate and Discount % are left
	completely untouched - Discount % already reduces Amount correctly on
	its own via core's native handling, since we never touch Rate or
	Price List Rate. Runs in "validate", after core's own
	calculate_taxes_and_totals() has already computed Amount/Net Amount
	(reflecting Discount % on its own) fresh from qty x rate - Amount is
	recomputed by core from scratch on *every* validate, so the full SCM
	value is subtracted from that fresh baseline every time, not just the
	change since the last save (there's nothing to double-count against).

	Note: because Rate/Price List Rate are never touched, core calculates
	GST/tax rows *before* this SCM deduction is applied, so tax ends up
	computed on the pre-SCM amount rather than the discounted one. That's
	a known trade-off of keeping Rate/Price List Rate untouched.
	"""
	conversion_rate = flt(doc.conversion_rate) or 1
	total_scm = 0.0
	total_base_scm = 0.0

	for row in doc.items:
		scm = flt(row.custom_scm_amount)
		if not scm:
			continue

		base_scm = scm * conversion_rate

		row.amount = flt(row.amount) - scm
		row.net_amount = flt(row.net_amount) - scm
		row.base_amount = flt(row.base_amount) - base_scm
		row.base_net_amount = flt(row.base_net_amount) - base_scm

		total_scm += scm
		total_base_scm += base_scm

	if total_scm:
		doc.total = flt(doc.total) - total_scm
		doc.net_total = flt(doc.net_total) - total_scm
		doc.grand_total = flt(doc.grand_total) - total_scm
		if doc.rounded_total:
			doc.rounded_total = flt(doc.rounded_total) - total_scm

		doc.base_total = flt(doc.base_total) - total_base_scm
		doc.base_net_total = flt(doc.base_net_total) - total_base_scm
		doc.base_grand_total = flt(doc.base_grand_total) - total_base_scm
		if doc.base_rounded_total:
			doc.base_rounded_total = flt(doc.base_rounded_total) - total_base_scm


def set_total_scm_amount(doc, method=None):
	"""Sum SCM across all item rows into the read-only header total."""
	doc.custom_total_scm_amount = sum(flt(row.custom_scm_amount) for row in doc.items)
