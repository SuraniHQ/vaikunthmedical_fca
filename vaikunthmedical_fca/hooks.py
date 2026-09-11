app_name = "vaikunthmedical_fca"
app_title = "Vaikunthmedical Fca"
app_publisher = "Vaikunthmedical"
app_description = "Custom app for Vaikunthmedical Pharmacy customisations"
app_email = "harshsurani00@gmail.com"
app_license = "mit"

# Apps
# ------------------

required_apps = ["erpnext"]

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "vaikunthmedical_fca",
# 		"logo": "/assets/vaikunthmedical_fca/logo.png",
# 		"title": "Vaikunthmedical Fca",
# 		"route": "/vaikunthmedical_fca",
# 		"has_permission": "vaikunthmedical_fca.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/vaikunthmedical_fca/css/vaikunthmedical_fca.css"
# app_include_js = "/assets/vaikunthmedical_fca/js/vaikunthmedical_fca.js"

# include js, css files in header of web template
# web_include_css = "/assets/vaikunthmedical_fca/css/vaikunthmedical_fca.css"
# web_include_js = "/assets/vaikunthmedical_fca/js/vaikunthmedical_fca.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "vaikunthmedical_fca/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "vaikunthmedical_fca/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "vaikunthmedical_fca.utils.jinja_methods",
# 	"filters": "vaikunthmedical_fca.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "vaikunthmedical_fca.install.before_install"
# after_install = "vaikunthmedical_fca.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "vaikunthmedical_fca.uninstall.before_uninstall"
# after_uninstall = "vaikunthmedical_fca.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "vaikunthmedical_fca.utils.before_app_install"
# after_app_install = "vaikunthmedical_fca.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "vaikunthmedical_fca.utils.before_app_uninstall"
# after_app_uninstall = "vaikunthmedical_fca.utils.after_app_uninstall"

# Build
# ------------------
# To hook into the build process

# after_build = "vaikunthmedical_fca.build.after_build"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "vaikunthmedical_fca.notifications.get_notification_config"

# Awesome Bar
# -----------
# Extra search results: list of dicts with label, description, route, index.
# route: ["List", "ToDo"], "/desk/docs/some/page", or "https://example.com"
# awesomebar_search = ["vaikunthmedical_fca.search.awesomebar_results"]

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Company": {
		"validate": "vaikunthmedical_fca.branding.set_company_logo",
	},
	"Purchase Receipt": {
		"validate": "vaikunthmedical_fca.purchase_receipt.ensure_batch_with_expiry",
		"on_submit": "vaikunthmedical_fca.purchase_receipt.sync_batch_expiry_and_selling_price",
	},
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"vaikunthmedical_fca.tasks.all"
# 	],
# 	"daily": [
# 		"vaikunthmedical_fca.tasks.daily"
# 	],
# 	"hourly": [
# 		"vaikunthmedical_fca.tasks.hourly"
# 	],
# 	"weekly": [
# 		"vaikunthmedical_fca.tasks.weekly"
# 	],
# 	"monthly": [
# 		"vaikunthmedical_fca.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "vaikunthmedical_fca.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "vaikunthmedical_fca.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "vaikunthmedical_fca.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "vaikunthmedical_fca.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["vaikunthmedical_fca.utils.before_request"]
# after_request = ["vaikunthmedical_fca.utils.after_request"]

# Job Events
# ----------
# before_job = ["vaikunthmedical_fca.utils.before_job"]
# after_job = ["vaikunthmedical_fca.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"vaikunthmedical_fca.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

