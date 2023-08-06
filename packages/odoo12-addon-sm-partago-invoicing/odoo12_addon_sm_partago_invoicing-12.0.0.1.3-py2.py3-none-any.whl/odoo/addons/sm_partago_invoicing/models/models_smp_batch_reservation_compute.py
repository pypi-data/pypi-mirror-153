# -*- coding: utf-8 -*-

import time

from odoo import models, fields, api
from odoo.tools.translate import _

from odoo.addons.sm_maintenance.models.models_sm_resources import sm_resources
from odoo.addons.sm_maintenance.models.models_sm_utils import sm_utils
from odoo.addons.sm_partago_invoicing.models.batch_type_enum import BatchType

class smp_batch_reservation_compute(models.Model):
  _name = 'smp.sm_batch_reservation_compute'

  # batch_type = fields.Char(string=_("Batch type"))
  batch_type = fields.Selection([
      ('usage', 'Usage'),
      ('teletac', 'Teletac')
  ], string=_("Batch type"), default="usage")
  name = fields.Char(string=_("Name"), required=True)
  description = fields.Char(string=_("Description"))
  reports_id = fields.One2many(comodel_name='smp.sm_report_reservation_compute',
                               inverse_name='batch_reservation_compute_id',
                               string=_("Reports"))
  state = fields.Selection([
        ('invoice_report', 'Inv report'),
        # ('test_cepa', 'test SEPA'),
        ('account_invoices_report', 'Account invoice report'),
        ('apply_discounts', 'Apply discounts'),
        ('generate_invoices', 'Generate invoices'),
        ('validate_invoices', 'Validate invoices'),
        # ('update_totals', 'Update totals'),
        # ('create_cepa', 'create SEPA'),
        ('closed', 'Closed'),
        ('closed_sent', 'SEPA sent'),
    ], default='invoice_report')
  invoice_report_id = fields.Many2one('sm.invoice_report', string=_("Invoice Report"))
  invoice_id = fields.Many2one('account.invoice',
    string=_("Related Invoice"),compute="_get_related_invoice")
  total_invoiced_amount_no_discount = fields.Float(string=_("Total income base (before discounts)"),
    compute="_get_inv_report_total_no_discount")
  total_discount = fields.Float(string=_("Total discount base"),compute="_get_total_discount")
  total_invoiced_amount = fields.Float(string=_("Total income base (after discounts)"),
    compute="_get_inv_report_total")
  invoice_total = fields.Float(string=_("Invoiced total"),compute="_get_invoice_total")
  invoice_taxes = fields.Float(string=_("Invoiced taxes"),compute="_get_invoice_taxes")
  is_grouped_report = fields.Boolean(string=_("is_grouped_report"),
    compute="check_is_grouped_report", store=False)

  _order = "name desc"

  @api.depends('invoice_report_id', 'reports_id')
  def check_is_grouped_report(self):
    for record in self:
      record.is_grouped_report = False
      if record.invoice_report_id.id != False:
        if record.invoice_report_id.grouped_report:
          record.is_grouped_report = True

  @api.depends('invoice_report_id')
  def _get_related_invoice(self):
    for record in self:
      if record.is_grouped_report:
        if record.invoice_report_id.id != False:
          record.invoice_id =record.invoice_report_id.invoice_id


  @api.depends('invoice_report_id', 'reports_id')
  def _get_inv_report_total_no_discount(self):
    for record in self:
      if record.is_grouped_report:
        if record.invoice_report_id.id != False:
          record.total_invoiced_amount_no_discount = record.invoice_report_id.total_amount_lines_untaxed
      else:
        total = 0
        for report in record.reports_id:
          if report.invoice_report_id.id != False:
            total += report.report_total_no_discounts
        record.total_invoiced_amount_no_discount = total

  @api.depends('invoice_report_id', 'reports_id', 'name')
  def _get_total_discount(self):
    for record in self:
      if record.is_grouped_report:
        if record.invoice_report_id.id != False:
          record.total_discount = record.invoice_report_id.discount_amount_subtotal
      else:
        total = 0
        for report in record.reports_id:
          if report.invoice_report_id.id != False:
            total += report.report_discount
        record.total_discount = total

  @api.depends('invoice_report_id', 'reports_id')
  def _get_inv_report_total(self):
    for record in self:
      if record.is_grouped_report:
        if record.invoice_report_id.id != False:
          record.total_invoiced_amount = record.invoice_report_id.ir_total_amount_signed
      else:
        total = 0
        for report in record.reports_id:
          if report.invoice_report_id.id != False:
            total += report.report_total
        record.total_invoiced_amount = total

  @api.depends('invoice_report_id', 'reports_id')
  def _get_invoice_total(self):
    for record in self:
      if record.is_grouped_report:
        if record.invoice_report_id.id != False:
          record.invoice_total = record.invoice_report_id.total_amount_in_invoice
      else:
        total = 0
        for report in record.reports_id:
          if report.invoice_report_id.id != False:
            total += report.invoice_total
        record.invoice_total = total

  @api.depends('invoice_report_id', 'reports_id')
  def _get_invoice_taxes(self):
    for record in self:
      if record.is_grouped_report:
        if record.invoice_report_id.id != False:
          record.invoice_taxes = record.invoice_report_id.total_taxes_in_invoice
      else:
        total = 0
        for report in record.reports_id:
          if report.invoice_report_id.id != False:
            total += report.invoice_taxes
        record.invoice_taxes = total

  @api.multi
  def reset_state(self):
    if self.env.context:
      if 'active_ids' in self.env.context:
        active_record = self.env['smp.sm_batch_reservation_compute'].browse(self.env.context['active_ids'])
        if active_record.exists():
          for rec in active_record:
            rec.state = "invoice_report"

  @api.multi
  def create_invoice_report(self):
    self.set_status_bar('account_invoices_report')
    return {
      "context": self.env.context,
      "view_type": "form",
      "view_mode": "form",
      "res_model": "sm_partago_invoicing.sm_invoice_report_wizard",
      "type": "ir.actions.act_window",
      "name": "Create collected invoice report",
      "target": "new",
    }

  @api.multi
  def sanitize_members_tariffs(self):
    self.ensure_one()
    if self.reports_id.exists():
      for report in self.reports_id:
        if report.report_type != BatchType.TELETAC.value:
          report.member_id.sanitize_tariffs()
    return True


  def prepare_report_invoices(self, collected_member=False, timeframe_desc=''):
    batch_to_compute = [self.batch_type]
    if collected_member.id:
      collected_member.sanitize_tariffs()
      report_invoice_report = self.env['sm.invoice_report'].create({
        'name': self.name + '-' + collected_member.name,
        'partner_id': collected_member.id,
        'company_id': 1,
        'date': str(time.strftime("%Y-%m-%d")),
        'timeframe_desc': timeframe_desc,
        'grouped_report': True
      })
      self.write({
        'invoice_report_id': report_invoice_report.id
      })
      report_invoice_report.compute_report_lines(False, batch_to_compute)
      report_invoice_report.assign_previous_pocketbook()
    else:
      if self.reports_id.exists():
        for report in self.reports_id:
          if report.member_id.id:
            report.member_id.sanitize_tariffs()
            report_invoice_report = self.env['sm.invoice_report'].create({
                'name': self.name + '-' + report.member_id.name,
                'partner_id': report.member_id.id,
                'company_id': 1,
                'date': str(time.strftime("%Y-%m-%d")),
                'timeframe_desc': timeframe_desc,
                'grouped_report': False
            })
            report.write({
                'invoice_report_id': report_invoice_report.id
            })
            report_invoice_report.compute_report_lines(False, batch_to_compute)
            report_invoice_report.assign_previous_pocketbook()
    return True

  @api.multi
  def account_invoice_reports(self):
    self.ensure_one()
    self.sanitize_members_tariffs()
    total = 0
    batch_to_compute = [self.batch_type]
    if not self.invoice_report_id.id:
      if self.reports_id.exists():
        for report in self.reports_id:
          if report.invoice_report_id.id:
            invoice_report = report.invoice_report_id
            invoice_report.compute_report_lines(True, batch_to_compute)
    else:
      if self.invoice_report_id.id:
        invoice_report = self.invoice_report_id
        invoice_report.compute_report_lines(True, batch_to_compute)
    self.set_status_bar('apply_discounts')

  @api.multi
  def apply_discounts(self):
    self.ensure_one()
    if not self.invoice_report_id.id:
      if self.reports_id.exists():
        for report in self.reports_id:
          if report.invoice_report_id.id:
            invoice_report = report.invoice_report_id
            invoice_report.create_discount_lines()
    else:
      if self.invoice_report_id.id:
        invoice_report = self.invoice_report_id
        invoice_report.create_discount_lines()
    self.set_status_bar('generate_invoices')

  @api.multi
  def generate_invoices(self):
    self.ensure_one()
    if not self.invoice_report_id.id:
      if self.reports_id.exists():
        for report in self.reports_id:
          if report.invoice_report_id.id:
            invoice_report = report.invoice_report_id
            invoice_report.create_related_invoice(self.batch_type)
    else:
      invoice_report = self.invoice_report_id
      invoice_report.create_related_invoice(self.batch_type)
    self.set_status_bar('validate_invoices')

  @api.multi
  def validate_invoices(self):
    self.ensure_one()
    if not self.invoice_report_id.id:
      if self.reports_id.exists():
        for report in self.reports_id:
          if report.invoice_report_id.id:
            report.invoice_report_id.validate_related_invoice()
    else:
      self.invoice_report_id.validate_related_invoice()
    self.set_status_bar('closed')

  @api.one
  def email_send_invoices(self):
    company = self.env.user.company_id
    email_template = company.invoice_mail_template_id
    email_values = {'send_from_code': True}
    if email_template.id:
      if self.invoice_id.id:
        invoice = self.invoice_id
        if not invoice.invoice_email_sent:
          email_template.with_context(email_values).send_mail(invoice.id, True)
          invoice.write({'invoice_email_sent': True})
      else:
          if self.reports_id.exists():
            for report in self.reports_id:
              if report.invoice_id.exists():
                invoice = report.invoice_id
                if invoice.exists():
                  if not invoice.invoice_email_sent:
                    email_template.with_context(email_values).send_mail(invoice.id, True)
                    invoice.write({'invoice_email_sent': True})

  def set_closed_sent(self):
        self.set_status_bar("closed_sent")
        return True

  def set_status_bar(self, state):
    self.write({
      'state': state,
    })

# @api.one
# def email_send_invoice_reports(self):
#   company = self.env.user.company_id
#   email_values = {'send_from_code': True}
#   if self.batch_type == BatchType.USAGES.value:
#     email_template = company.invoice_report_mail_template_id
#   if self.batch_type == BatchType.TELETAC.value:
#     email_template = company.invoice_report_teletac_mail_template_id
#   if email_template.id:
#     if self.invoice_report_id.id:
#       invoice_report = self.invoice_report_id
#       if not invoice_report.email_sent:
#         email_template.with_context(email_values).send_mail(invoice_report.id, True)
#         invoice_report.write({'email_sent': True})
#     else:
#       if self.reports_id.exists():
#         for report in self.reports_id:
#           invoice_report = report.invoice_report_id
#           if invoice_report.id:
#             if not invoice_report.email_sent:
#               email_template.with_context(email_values).send_mail(invoice_report.id, True)
#               invoice_report.write({'email_sent': True})