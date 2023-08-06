# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.translate import _


class sm_member(models.Model):
  _inherit = 'res.partner'
  _name = 'res.partner'

  paymaster = fields.Many2one('res.partner', string=_("Paymaster for company reservations"))
