function apply_scheme_and_discount(cdt, cdn) {
	const row = locals[cdt][cdn];
	const base_amount = flt(row.qty) * flt(row.rate);
	const discount_amount = (base_amount * flt(row.custom_dis_percent)) / 100.0;
	const amount = base_amount - flt(row.custom_scm) - discount_amount;

	frappe.model.set_value(cdt, cdn, "amount", amount);
}

frappe.ui.form.on("Purchase Receipt Item", {
	custom_scm(frm, cdt, cdn) {
		apply_scheme_and_discount(cdt, cdn);
	},
	custom_dis_percent(frm, cdt, cdn) {
		apply_scheme_and_discount(cdt, cdn);
	},
});
