# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.translate import _


class sm_company(models.Model):
  _inherit = 'res.company'

  cs_carsharing_product_id = fields.Many2one('product.product',
    string=_("Carsharing product (predefined)"))
  cs_teletac_product_id = fields.Many2one('product.product',
    string=_("Teletac product (predefined)"))
  cs_discount_product_id = fields.Many2one('product.product',
    string=_("Discount product (predefined)"))

  invoice_mail_template_id = fields.Many2one('mail.template',
    string=_("Invoice notification template"))
  invoice_report_mail_template_id = fields.Many2one('mail.template',
    string=_("Invoice report notification template"))
  invoice_report_teletac_mail_template_id = fields.Many2one('mail.template',
    string=_("Invoice report teletac notification template"))

  notfound_car_analytic_account_id = fields.Many2one('account.analytic.account',
    string=_("Not found car analytic account"))
  notfound_teletac_analytic_account_id = fields.Many2one('account.analytic.account',
    string=_("Not found teletac analytic account"))
  cs_invoice_payment_mode_id = fields.Many2one('account.payment.mode',
    string=_("Payment Mode default for carsharing invoices"))

  cs_invoice_journal_id = fields.Many2one('account.journal',
    string=_("Journal default for carsharing invoices"))

  percentage_extra_minutes_cost = fields.Integer(_('Percentage of extra minutes cost'))
  percentage_not_used = fields.Integer(_('Percentage of extra minutes cost'))
  maxim_kms_per_hour = fields.Integer(_('Maxim kms per hour'))
  maxim_kms_per_day = fields.Integer(_('Maxim kms per day'))