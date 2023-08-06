# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.translate import _


class smp_teletac(models.Model):
  _inherit = 'smp.sm_teletac'
  _name = 'smp.sm_teletac'

  invoice_report_id = fields.Many2one('sm.invoice_report', string=_("Related invoice report"))
  report_reservation_compute_id = fields.Many2one('smp.sm_report_reservation_compute', string=_("Report"))

  def get_analytic_account(self):
    company = self.env.user.company_id
    analytic_account = company.notfound_teletac_analytic_account_id
    compute = self.reservation_compute_id
    if compute:
      analytic_account = compute.get_teletac_analytic_account()
    return analytic_account

  # @api.depends('invoice_report_id')
  # def report_reservation_compute_id(self):
  #   for record in self:
  #     if record.reservation_compute_id.id:
  #       record.reservation_compute_invoiced = record.reservation_compute_id.compute_invoiced
  #     else:
  #       record.reservation_compute_invoiced = False

  # @api.depends('invoice_report_id')
  # def _check_compute_forgiven(self):
  #   for record in self:
  #     if record.reservation_compute_id.id:
  #       record.reservation_compute_forgiven = record.reservation_compute_id.compute_forgiven
  #     else:
  #       record.reservation_compute_forgiven = False


smp_teletac()

