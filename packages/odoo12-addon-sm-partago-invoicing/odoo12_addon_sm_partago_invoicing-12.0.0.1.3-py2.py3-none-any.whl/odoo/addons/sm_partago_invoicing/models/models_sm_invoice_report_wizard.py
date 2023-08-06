# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.translate import _


class sm_invoice_report_wizard(models.TransientModel):
  _name = "sm_partago_invoicing.sm_invoice_report_wizard"

  is_grouped = fields.Boolean(string=_("Is grouped"))
  member_id = fields.Many2one('res.partner', string=_("Member to collect"))
  timeframe_desc = fields.Char(string=_("Time frame desc"))

  @api.multi
  def create_invoice_report(self):
    if self.env.context:
      if 'active_ids' in self.env.context:
        batch_reservations = self.env['smp.sm_batch_reservation_compute'].browse(
          self.env.context['active_ids'])
        if batch_reservations.exists():
          for batch_reservation in batch_reservations:
            batch_reservation.prepare_report_invoices(self.member_id, self.timeframe_desc)
    return True
