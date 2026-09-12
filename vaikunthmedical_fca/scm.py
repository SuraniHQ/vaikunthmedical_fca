import frappe
from frappe.utils import flt


def apply_scm_to_rate(doc, method=None):
	"""Let "SCM" (a flat per-line scheme discount, on top of Discount %) reduce
	Rate further, applied pre-tax - so GST calculates on the post-discount,
	post-SCM amount, matching how supplier invoices with a scheme line
	usually compute GST themselves (GST on Net Value, where Net Value is
	Goods Value minus both the % discount and the scheme value).

	Runs in before_validate, ahead of core's own discount_percentage/
	pricing-rule reconciliation and tax calculation. Handles a row as soon
	as either SCM or Discount % is used - core's own native handling of
	Discount % alone only works when Rate is left blank for core to
	derive; once Rate already holds a value (e.g. carried over from a
	previous save, or fetched from a Buying Price List alongside Price
	List Rate), core's reconciliation discards the discount the same way
	it would if we'd touched Rate ourselves. So this takes over for any
	row using either field, not just rows combining both.

	Expects the normal ERPNext input pattern: Price List Rate populated
	(typed directly, or fetched from a Buying Price List) with Discount %,
	Rate left for core to derive - not Rate typed directly. Price List Rate
	itself is never modified here, only read.

	Rate is a persisted field, so a naive per-save delta on SCM alone would
	either double-subtract on resave, or (since discount_percentage is a
	percentage, not a flat amount) compound incorrectly if combined the
	same way. Instead, custom_scm_rate_anchor (hidden) holds "Price List
	Rate x (1 - discount% / 100)", frozen once, and Rate is recomputed
	fresh from it every time: anchor - SCM / qty. That's stateless and
	idempotent - re-saving without changes, or changing SCM later, always
	recomputes correctly with no drift.

	Known trade-off: because our Rate no longer matches what core's own
	reconciliation would derive from Price List Rate/Discount % alone, core
	resets the *displayed* Discount % to 0 after save (folding the
	equivalent reduction into Rate/margin instead) whenever SCM is also
	present on the row - which would also erase our own reference to what
	the user asked for, since a later validate pass (e.g. submitting right
	after saving) would otherwise reread a discount_percentage core has
	already reset to 0. So the *first* pass where discount_percentage is
	still genuinely non-zero freezes the anchor; once discount_percentage
	reads back as 0 (core's reset, not the user clearing it), that anchor
	is reused instead of recomputed. Rate/Amount/tax math stays correct
	across however many times the document validates - only Discount % as
	displayed goes to 0.
	"""
	for row in doc.items:
		scm = flt(row.custom_scm_amount)
		discount_percentage = flt(row.discount_percentage)
		if not scm and not discount_percentage and not flt(row.custom_scm_rate_anchor):
			continue

		qty = flt(row.qty) or 1

		if discount_percentage:
			price_list_rate = flt(row.price_list_rate) or flt(row.rate)
			row.custom_scm_rate_anchor = price_list_rate * (1 - discount_percentage / 100.0)
		elif not flt(row.custom_scm_rate_anchor):
			row.custom_scm_rate_anchor = flt(row.price_list_rate) or flt(row.rate)

		row.rate = flt(row.custom_scm_rate_anchor) - (scm / qty)


def set_total_scm_amount(doc, method=None):
	"""Sum SCM across all item rows into the read-only header total."""
	doc.custom_total_scm_amount = sum(flt(row.custom_scm_amount) for row in doc.items)
