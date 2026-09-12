import frappe
from frappe.utils import flt


def apply_scm_to_rate(doc, method=None):
	"""Let "SCM" (a flat per-line scheme discount, on top of Discount %) reduce
	Rate further, applied pre-tax. Runs in before_validate, ahead of core's
	own discount_percentage/pricing-rule reconciliation and tax calculation,
	so GST ends up computed on the post-SCM amount rather than the full one.

	Only touches rows where SCM is actually used - a plain Discount %
	row with no SCM is left entirely to core's native handling.

	Rate is a persisted field, so a naive per-save delta on SCM alone would
	either double-subtract on resave, or (since discount_percentage is a
	percentage, not a flat amount) compound incorrectly if combined the same
	way. Instead, price_list_rate is used as a stable "gross rate" anchor
	(captured once, from the first typed Rate, since Purchase Receipt/
	Invoice rows don't reliably have one already) and Rate is recomputed
	fresh from it every time: price_list_rate x (1 - discount% / 100) -
	SCM / qty. That's stateless and idempotent - re-saving without changes,
	or changing Discount % or SCM later, always recomputes correctly with
	no drift.

	Known trade-off: because our Rate no longer matches what core's own
	reconciliation would derive from price_list_rate/discount_percentage
	alone, core resets the *displayed* Discount % to 0 after save (folding
	the equivalent reduction into Rate/margin instead) whenever SCM is also
	present on the row - which would also erase our own reference to what
	the user asked for, since a later validate pass (e.g. submitting right
	after saving) would otherwise reread a discount_percentage core has
	already reset to 0. So the *first* pass where discount_percentage is
	still genuinely non-zero freezes the post-discount, pre-SCM rate into
	price_list_rate as a stable anchor; once discount_percentage reads back
	as 0 (core's reset, not the user clearing it), that anchor is reused
	instead of recomputed. Rate/Amount/tax math stays correct across
	however many times the document validates - only Discount % as
	displayed goes to 0.

	Editing Discount % again after SCM has already been applied re-anchors
	from the already-reduced Rate rather than the original gross rate; for
	the normal flow - enter qty/rate/discount%/SCM once, then save/submit -
	this isn't hit.

	This is a doc_events hook (hooks.py -> before_validate), not a client
	script, so it runs identically for every entry path - desk UI, REST
	API, Data Import Tool, bench console - there is no client-side-only
	code path to bypass. It also validates: SCM can't be negative (that's
	a surcharge, not a discount), and SCM can't exceed the post-Discount %
	amount for the row (which would drive the line negative).
	"""
	for row in doc.items:
		scm = flt(row.custom_scm_amount)
		if not scm:
			continue

		if scm < 0:
			frappe.throw(f"Row #{row.idx} ({row.item_code}): SCM cannot be negative.")

		qty = flt(row.qty) or 1
		discount_percentage = flt(row.discount_percentage)

		if discount_percentage:
			row.price_list_rate = flt(row.rate) * (1 - discount_percentage / 100.0)
		elif not flt(row.price_list_rate):
			row.price_list_rate = flt(row.rate)

		amount_after_discount = flt(row.price_list_rate) * qty
		if scm > amount_after_discount:
			frappe.throw(
				f"Row #{row.idx} ({row.item_code}): SCM ({scm}) cannot exceed the line amount "
				f"after Discount % ({amount_after_discount})."
			)

		row.rate = flt(row.price_list_rate) - (scm / qty)


def set_total_scm_amount(doc, method=None):
	"""Sum SCM across all item rows into the read-only header total."""
	doc.custom_total_scm_amount = sum(flt(row.custom_scm_amount) for row in doc.items)
