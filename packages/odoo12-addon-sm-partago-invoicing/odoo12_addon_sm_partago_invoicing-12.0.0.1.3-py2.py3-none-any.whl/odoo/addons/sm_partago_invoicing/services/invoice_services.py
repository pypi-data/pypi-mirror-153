# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64

from odoo import _
from odoo.addons.base_rest.components.service import skip_secure_response
from odoo.addons.component.core import Component
from odoo.exceptions import MissingError
from odoo.http import request


class PartnerService(Component):
  _inherit = 'base.rest.service'
  _name = 'invoice.service'
  _usage = 'invoice'
  _collection = 'invoice.rest.public.services'
  _description = """
     
  """

  @skip_secure_response
  def get_invoice(self, _id, **params):
    partner = self.get_res_partner_by_uid(uid=params['uid'])
    invoice = self.get_account_invoice(conditions=[
      ('partner_id', '=', partner.id),
      ('id', '=', _id)
    ])
    attachment = self.get_attachment_or_create(invoice=invoice)
    return self.prepare_attachment_header(attachment=attachment)

  def get_invoices(self, _id=None, **params):
    partner = self.get_res_partner_by_uid(uid=params['uid'])
    partner_invoices = self.get_account_invoice(conditions=[
      ('partner_id', '=', partner.id)
    ])
    return self.prepare_invoices_data(partner_invoices)

  # Validator

  def _validator_get_invoice(self):
    return {
      'uid': {'type': 'string'},
    }

  def _validator_return_get_invoice(self):
    return {}

  def _validator_get_invoices(self):
    return {
      'uid': {'type': 'string'},
    }

  def _validator_return_get_invoices(self):
    return {}

  # helper

  def get_res_partner_by_uid(self, uid):
    return self.env['res.partner'].sudo().search([('firebase_uid', '=', uid)])

  def get_account_invoice(self, conditions):
    return self.env['account.invoice'].sudo().search(conditions)

  def get_attachment(self, conditions):
    return self.env['ir.attachment'].sudo().search(conditions, limit=1)

  def get_attachment_or_create(self, invoice):
    invoice_number = str(invoice.number).split("/")

    attachment = self.get_attachment(conditions=[
      ('name', 'like', "%" + invoice_number[1] + "%"),
      ('name', 'like', "%" + invoice_number[2] + "%")
    ])

    if not attachment.exists():
      attachment = self.create_invoice_attach(invoice)

    return attachment

  def create_invoice_attach(self, invoice):
    template = self.env.ref('account.email_template_edi_invoice', False).sudo()

    values = template.generate_email(invoice.id)

    attachment = False
    if len(values['attachments']):
      for attach in values['attachments']:
        if attachment is False:
          filename = attach[0]
          filedata = attach[1]
          return self.env['ir.attachment'].sudo().create({
            'res_model': 'account.invoice',
            'res_id': invoice.id,
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

  def prepare_invoices_data(self, invoices):
    data = {}

    for invoice in invoices:
      data[invoice.id] = {
        "name": invoice.number,
        "date": invoice.date_invoice,
        "quantity": invoice.amount_total
      }

    return data

  # DEPRECATED

  def test(self, _id=None, **params):
    invoice = self.env['ir.attachment'].sudo().search([('id', '=', 1)])

    data = {
      "binary": str(invoice.datas),
      "content": invoice.index_content
    }
    return data

  def _validator_test(self):
    return {}

  def _validator_return_test(self):
    return {
      'binary': {'type': 'string'},
      'content': {'type': 'string'}
    }
