import frappe
from frappe.utils import flt, round_based_on_smallest_currency_fraction


def apply_scm_to_rate(doc, method=None):
	"""Let "SCM" (a flat per-line scheme discount) reduce Rate, applied
	pre-tax, so GST calculates on the post-SCM amount. Confirmed against a
	real supplier invoice: their own math per line is
	(Qty x Rate - SCM), GST added on that, and a % discount applied
	*afterward* - Discount % is handled separately by
	apply_row_wise_discount_after_tax (post-tax, can vary per row), not
	here.

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


def apply_row_wise_discount_after_tax(doc, method=None):
	"""Let "Disc % (post-tax)" reduce the grand total, per row, applied
	*after* GST - different rows can use different percentages, unlike
	ERPNext's native header-level "Additional Discount on Grand Total"
	(one percentage for the whole document). Confirmed against a real
	supplier invoice: per line, (Qty x Rate - SCM) + that row's own GST,
	then this % taken off - reproduces their printed per-item totals
	exactly.

	Runs in "validate", after core has already computed Amount and the
	per-row tax split from the SCM-adjusted Rate. Amount and tax are
	recomputed by core from scratch on every validate, so the full
	deduction is computed fresh from them each time - nothing to
	double-count against.

	Reads doc._item_wise_tax_details (a private, in-memory list core
	builds while calculating taxes) rather than the public
	item_wise_tax_details child table - that table is only materialized
	later, in on_update (a POST-save hook, via
	AccountsController.on_update() -> process_item_wise_tax_details()),
	so it's still empty at this point in validate.

	Only grand_total/rounded_total (and base_ equivalents) are adjusted -
	net_total is left alone, since this discount is computed on the
	post-tax amount, not the pre-tax one.
	"""
	conversion_rate = flt(doc.conversion_rate) or 1

	tax_by_row = {}
	for t in doc.get("_item_wise_tax_details") or []:
		tax_by_row[t.item.name] = tax_by_row.get(t.item.name, 0) + flt(t.amount)

	total_discount = 0.0
	for row in doc.items:
		disc_percent = flt(row.custom_disc_percent)
		if not disc_percent:
			continue

		row_total_before_discount = flt(row.amount) + tax_by_row.get(row.name, 0)
		total_discount += row_total_before_discount * disc_percent / 100.0

	doc.custom_total_disc_amount = total_discount

	if total_discount:
		base_discount = total_discount * conversion_rate

		doc.grand_total = flt(doc.grand_total) - total_discount
		doc.base_grand_total = flt(doc.base_grand_total) - base_discount

		# Recompute rounding from the new grand_total rather than subtracting
		# a delta from the old rounded_total - rounding_adjustment is not
		# guaranteed to track grand_total linearly (e.g. currency fraction
		# rounding), so a naive subtraction can drift.
		if doc.rounded_total and not doc.disable_rounded_total:
			doc.rounded_total = round_based_on_smallest_currency_fraction(
				doc.grand_total, doc.currency, doc.precision("rounded_total")
			)
			doc.rounding_adjustment = flt(
				doc.rounded_total - doc.grand_total, doc.precision("rounding_adjustment")
			)
			doc.base_rounded_total = round_based_on_smallest_currency_fraction(
				doc.base_grand_total,
				frappe.get_cached_value("Company", doc.company, "default_currency"),
				doc.precision("base_rounded_total"),
			)
			doc.base_rounding_adjustment = flt(
				doc.base_rounded_total - doc.base_grand_total, doc.precision("base_rounding_adjustment")
			)
