# -*- coding: utf-8 -*-

from odoo import api, models, fields
from odoo.tools.translate import _


class smp_invoice_line(models.Model):
  _inherit = 'account.invoice.line'
  _name = 'account.invoice.line'

  related_tariff_id = fields.Many2one('smp.sm_carsharing_tariff',
    string=_("Related tariff"))
  related_reservation_compute_id = fields.Many2one('smp.sm_reservation_compute',
    string=_("Related reservaion compute"))
  invoice_report_id = fields.Many2one('sm.invoice_report',
    string=_("Related invoice report"))
  partner_id = fields.Many2one('res.partner', string=_("Partner"))
  initial_price_computed = fields.Float(string=_("Initial price"),
    compute="_get_line_initial_price",store=False)

  line_type = fields.Selection([
    ('default', 'Default'),
    ('cs_default', 'Carsharing default'),
    ('cs_extra', 'Carsharing extra time'),
    ('cs_teletac', 'Teletac'),
    ('cs_discount', 'Discount')
  ], string=_("Line type"), default="default")

  @api.depends('related_reservation_compute_id')
  def _get_line_initial_price(self):
    for record in self:
      record.initial_price_computed = 0
      if record.related_reservation_compute_id.id != False:
        if record.related_reservation_compute_id.carconfig_id.id != False:
          record.initial_price_computed = record.related_reservation_compute_id.cs_carconfig_id.initial_price

smp_invoice_line()
