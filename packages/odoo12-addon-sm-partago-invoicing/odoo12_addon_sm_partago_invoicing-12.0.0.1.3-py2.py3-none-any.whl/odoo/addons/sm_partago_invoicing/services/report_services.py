# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64

from odoo import _
from odoo.addons.base_rest.components.service import skip_secure_response
from odoo.addons.component.core import Component
from odoo.exceptions import MissingError
from odoo.http import request


class ReportService(Component):
  _inherit = 'base.rest.service'
  _name = 'report.service'
  _usage = 'report'
  _collection = 'report.rest.public.services'
  _description = """
     
  """

  @skip_secure_response
  def get_use_report(self, _id, **params):
    partner = self.get_res_partner_by_uid(uid=params['uid'])
    use_report = self.get_partner_use_reports(conditions=[
      ('partner_id', '=', partner.id),
      ('id', '=', _id)
    ])
    attachment = self.get_attachment_or_create(use_report=use_report)
    return self.prepare_attachment_header(attachment=attachment)

  def get_use_reports(self, _id=None, **params):
    partner = self.get_res_partner_by_uid(uid=params['uid'])
    partner_reports = self.get_partner_use_reports(conditions=[
      ('partner_id', '=', partner.id)
    ])
    return self.prepare_use_report_data(partner_reports)

  # Validator

  def _validator_get_use_report(self):
    return {
      'uid': {'type': 'string'},
    }

  def _validator_return_get_use_report(self):
    return {}

  def _validator_get_use_reports(self):
    return {
      'uid': {'type': 'string'},
    }

  def _validator_return_get_use_reports(self):
    return {}

  # helper

  def get_res_partner_by_uid(self, uid):
    return self.env['res.partner'].sudo().search([('firebase_uid', '=', uid)])

  def get_partner_use_reports(self, conditions):
    return self.env['sm.invoice_report'].sudo().search(conditions)

  def get_attachment(self, conditions):
    return self.env['ir.attachment'].sudo().search(conditions, limit=1)

  def get_attachment_or_create(self, use_report):
    attachment = self.get_attachment(conditions=[
      ('name', 'like', use_report.name)
    ])

    if not attachment.exists():
      attachment = self.create_use_report_attach(use_report=use_report)

    return attachment

  def create_use_report_attach(self, use_report):
    template = self.env.ref('mail_templates.email_template_edi_invoice_report', False).sudo()

    values = template.generate_email(use_report.id)

    attachment = False
    if len(values['attachments']):
      for attach in values['attachments']:
        if attachment is False:
          filename = attach[0]
          filedata = attach[1]
          return self.env['ir.attachment'].sudo().create({
            'res_model': 'sm.invoice_report',
            'res_id': use_report.id,
            'name': filename,
            'datas': filedata,
            'datas_fname': filename
          })

  def prepare_attachment_header(self, attachment):
    headers = [('X-Content-Type-Options', 'nosniff'),
           ('ETag', '"89e20a46d157479a35eeca1347d1ee1b"'),
           ('Cache-Cvalontrol', 'max-age=0')]

    attachment_base64 = base64.b64decode(attachment.datas)

    headers.append(('Content-Type', attachment.mimetype))
    headers.append(('Content-Length', len(attachment_base64)))

    response = request.make_response(attachment_base64, headers)
    response.status_code = 200

    return response

  def prepare_use_report_data(self, use_reports):
    data = {}

    for report in use_reports:
      data[report.id] = {
        "date": report.date,
        "total_mileage": report.total_mileage
      }

    return data
