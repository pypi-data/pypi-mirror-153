# -*- coding: utf-8 -*-
from odoo import fields, models, _

class ResConfigSettings(models.TransientModel):
  _inherit = 'res.config.settings'

  # INVOICING
  cs_carsharing_product_id = fields.Many2one(
    related='company_id.cs_carsharing_product_id',
    string=_("Carsharing product (predefined)"),
    readonly=False)

  cs_teletac_product_id = fields.Many2one(
    related='company_id.cs_teletac_product_id',
    string=_("Teletac product (predefined)"),
    readonly=False)
  cs_discount_product_id = fields.Many2one(
    related='company_id.cs_discount_product_id',
    string=_("Discount product (predefined)"),
    readonly=False)

  # MAIL TEMPLATES
  invoice_mail_template_id = fields.Many2one(
    related='company_id.invoice_mail_template_id',
    string=_("Invoice notification template"),
    readonly=False)
  invoice_report_mail_template_id = fields.Many2one(
    related='company_id.invoice_report_mail_template_id',
    string=_("Invoice report notification template"),
    readonly=False)
  invoice_report_teletac_mail_template_id = fields.Many2one(
    related='company_id.invoice_report_teletac_mail_template_id',
    string=_("Invoice report teletacs notification template"),
    readonly=False)

  # ANALYTIC ACCOUNTING
  notfound_car_analytic_account_id = fields.Many2one(
    related='company_id.notfound_car_analytic_account_id',
    string=_("Not found car analytic account"),
    readonly=False)

  notfound_teletac_analytic_account_id = fields.Many2one(
    related='company_id.notfound_teletac_analytic_account_id',
    string=_("Not found teletac analytic account"),
    readonly=False)

  # INVOICE CONFIG
  cs_invoice_payment_mode_id = fields.Many2one(
    related='company_id.cs_invoice_payment_mode_id',
    string=_("Payment Mode default for carsharing invoices"),
    readonly=False)
  cs_invoice_journal_id = fields.Many2one(
    related='company_id.cs_invoice_journal_id',
    string=_("Journal default for carsharing invoices"),
    readonly=False)

  # RESERVATION RATING
  percentage_extra_minutes_cost = fields.Integer(
    related='company_id.percentage_extra_minutes_cost',
    string=_("percentage_extra_minutes_cost"),
    readonly=False)

  percentage_not_used = fields.Integer(
    related='company_id.percentage_not_used',
    string=_("percentage_not_used"),
    readonly=False)

  maxim_kms_per_hour = fields.Integer(
    related='company_id.maxim_kms_per_hour',
    string=_("Maxim kms per hour"),
    readonly=False)

  maxim_kms_per_day = fields.Integer(
    related='company_id.maxim_kms_per_day',
    string=_("Maxim kms per day"),
    readonly=False)
