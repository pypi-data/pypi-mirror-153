# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.translate import _

from odoo.addons.sm_partago_invoicing.models.batch_type_enum import BatchType

class smp_report_reservation_compute(models.Model):
  _name = 'smp.sm_report_reservation_compute'

  report_type = fields.Selection([
    (str(BatchType.USAGES.value), 'Reservations'),
    (str(BatchType.TELETAC.value), 'Teletacs'),
  ], string=_("Batch type"), store=True)

  name = fields.Char(string=_("Name"), required=True)

  batch_reservation_compute_id = fields.Many2one('smp.sm_batch_reservation_compute',
    string=_("Batch reservation compute"))

  member_id = fields.Many2one('res.partner', string=_("Member"))

  reservation_computes_id = fields.One2many(comodel_name='smp.sm_reservation_compute',
    inverse_name='report_reservation_compute_id',
    string=_("Reservations"))

  teletacs_compute_id = fields.One2many(comodel_name='smp.sm_teletac',
    inverse_name='report_reservation_compute_id',
    string=_("Teletacs"))

  invoice_report_id = fields.Many2one('sm.invoice_report', string=_("Invoice Report"))

  report_total_no_discounts = fields.Float(string=_("Report total base (no discounts)"),
    compute="_get_report_total_no_discounts",store=False)
  report_discount = fields.Float(string=_("Report discount base"), compute="_get_report_discount",
    store=False)

  report_total = fields.Float(string=_("Report total base"), compute="_get_report_total",
    store=False)
  invoice_total = fields.Float(string=_("Invoice total"),compute="_get_invoice_total",
    store=False)
  invoice_taxes = fields.Float(string=_("Invoice taxes"),compute="_get_invoice_taxes",
    store=False)

  invoice_id = fields.Many2one('account.invoice', string=_("Invoice"),compute="_get_report_invoice")

  _order = "name desc"

  @api.depends('invoice_report_id')
  def _get_report_invoice(self):
    for record in self:
      if record.invoice_report_id.id != False:
        record.invoice_id = record.invoice_report_id.invoice_id

  @api.depends('invoice_report_id')
  def _get_report_total_no_discounts(self):
    for record in self:
      if record.invoice_report_id.id != False:
        record.report_total_no_discounts = record.invoice_report_id.total_amount_lines_untaxed

  @api.depends('invoice_report_id')
  def _get_report_discount(self):
    for record in self:
      if record.invoice_report_id.id != False:
        record.report_discount = record.invoice_report_id.discount_amount_subtotal

  @api.depends('invoice_report_id')
  def _get_report_total(self):
    for record in self:
      if record.invoice_report_id.id != False:
        record.report_total = record.invoice_report_id.ir_total_amount_signed

  @api.depends('invoice_report_id')
  def _get_invoice_total(self):
    for record in self:
      if record.invoice_report_id.id != False:
        record.invoice_total = record.invoice_report_id.total_amount_in_invoice

  @api.depends('invoice_report_id')
  def _get_invoice_taxes(self):
    for record in self:
      if record.invoice_report_id.id != False:
        record.invoice_taxes = record.invoice_report_id.total_taxes_in_invoice
