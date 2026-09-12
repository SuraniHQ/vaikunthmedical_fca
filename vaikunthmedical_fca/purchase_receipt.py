import calendar
import re
from datetime import date

import frappe
from frappe.utils import flt

_MONTH_YEAR_PATTERN = re.compile(r"^\s*(\d{1,2})[-/](\d{2}|\d{4})\s*$")


def apply_expiry_month_year(doc, method=None):
	"""Let the GRN row's Expiry Date be entered as just MM-YY, the way it's
	printed on most medicine packaging, and expand it to the last calendar
	day of that month - the conventional reading of a printed MM/YY expiry.
	"""
	for row in doc.items:
		month_year = row.get("custom_expiry_month_year")
		if not month_year:
			continue

		match = _MONTH_YEAR_PATTERN.match(str(month_year))
		if not match:
			frappe.throw(f"Row #{row.idx}: Expiry (MM-YY) {month_year!r} is not in MM-YY format, e.g. 12-26")

		month = int(match.group(1))
		year = int(match.group(2))
		if year < 100:
			year += 2000

		if not 1 <= month <= 12:
			frappe.throw(f"Row #{row.idx}: {month_year!r} is not a valid month")

		last_day = calendar.monthrange(year, month)[1]
		row.custom_expiry_date = date(year, month, last_day)


def apply_scheme_and_discount(doc, method=None):
	"""Let "Scm" (a flat per-line scheme/promotional discount) and "Dis %"
	(a percentage discount) both reduce Amount directly, leaving Rate exactly
	as entered - either one alone, or both together on the same row. Runs
	after core's own calculate_taxes_and_totals(), which recomputes Amount/
	Net Amount and the document totals fresh from qty x rate on *every*
	validate - unlike Rate, Amount never "remembers" a previous reduction
	between saves, so the full deduction is computed from that fresh
	baseline every time, not just the change since the last save (there's
	nothing to double-count against). Dis % is applied against the same
	fresh baseline as Scm, not against Scm's already-reduced amount, so the
	two don't compound into each other.

	Note: this does not re-run tax calculation, so if Purchase Taxes and
	Charges are configured, tax amounts stay based on the pre-deduction value.
	"""
	conversion_rate = flt(doc.conversion_rate) or 1
	total_deduction = 0.0
	total_base_deduction = 0.0

	for row in doc.items:
		base_amount = flt(row.amount)
		scm = flt(row.custom_scm)
		discount_amount = base_amount * flt(row.custom_dis_percent) / 100.0
		deduction = scm + discount_amount

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


def snapshot_typed_batch_no(doc, method=None):
	"""Core's set_missing_item_details() (part of the base validate() chain)
	overwrites a manually typed Batch No back to blank whenever
	use_serial_batch_fields is set - that field is designed for *picking* an
	existing batch with available stock, not typing a brand-new incoming one,
	so its auto-suggest finds nothing and clobbers it. Snapshot what was
	actually typed here (before_validate runs before that clobber) so
	ensure_batch_with_expiry can restore it afterwards.
	"""
	for row in doc.items:
		row.set("_typed_batch_no", row.batch_no)


def ensure_batch_with_expiry(doc, method=None):
	"""Create the Batch for a freshly typed supplier batch number ourselves,
	before core tries to auto-create it. Core's own auto-create only sets
	batch_id + item (no expiry), which hard-fails for items that don't have
	a Shelf Life set. Creating it here with the row's Expiry Date avoids that.
	"""
	for row in doc.items:
		typed_batch_no = row.get("_typed_batch_no")
		if typed_batch_no and not row.batch_no:
			row.batch_no = typed_batch_no

		if row.batch_no and not frappe.db.exists("Batch", row.batch_no):
			batch = frappe.new_doc("Batch")
			batch.batch_id = row.batch_no
			batch.item = row.item_code
			if row.custom_expiry_date:
				batch.expiry_date = row.custom_expiry_date
			batch.insert(ignore_permissions=True)


def sync_batch_expiry_and_selling_price(doc, method=None):
	"""On GRN submission: push each row's Expiry Date onto the batch(es) it
	received, and roll the row's MRP (entered per Purchase UOM) into the
	default Selling Price List, converted to Stock UOM. When the row has a
	batch, the price is recorded against that batch specifically, so
	different batches of the same item can carry different selling prices.
	"""
	for row in doc.items:
		batch_nos = _get_row_batch_nos(row)

		if row.custom_expiry_date:
			for batch_no in batch_nos:
				_set_batch_expiry(batch_no, row.custom_expiry_date)

		if row.custom_mrp:
			if batch_nos:
				for batch_no in batch_nos:
					_update_selling_price(row, batch_no)
			else:
				_update_selling_price(row)


def _get_row_batch_nos(row):
	if row.batch_no:
		return [row.batch_no]

	if row.serial_and_batch_bundle:
		return frappe.get_all(
			"Serial and Batch Entry",
			filters={"parent": row.serial_and_batch_bundle},
			pluck="batch_no",
			distinct=True,
		)

	return []


def _set_batch_expiry(batch_no, expiry_date):
	if batch_no and frappe.db.exists("Batch", batch_no):
		frappe.db.set_value("Batch", batch_no, "expiry_date", expiry_date)


def _update_selling_price(row, batch_no=None):
	price_list = frappe.db.get_single_value("Selling Settings", "selling_price_list")
	if not price_list:
		return

	rate_in_stock_uom = flt(row.custom_mrp) / flt(row.conversion_factor or 1)
	batch_no = batch_no or ""

	existing = frappe.db.get_value(
		"Item Price",
		{
			"item_code": row.item_code,
			"price_list": price_list,
			"uom": row.stock_uom,
			"selling": 1,
			"batch_no": batch_no,
		},
		"name",
	)

	if existing:
		frappe.db.set_value("Item Price", existing, "price_list_rate", rate_in_stock_uom)
	else:
		frappe.get_doc(
			{
				"doctype": "Item Price",
				"item_code": row.item_code,
				"price_list": price_list,
				"uom": row.stock_uom,
				"selling": 1,
				"batch_no": batch_no,
				"price_list_rate": rate_in_stock_uom,
			}
		).insert(ignore_permissions=True)
