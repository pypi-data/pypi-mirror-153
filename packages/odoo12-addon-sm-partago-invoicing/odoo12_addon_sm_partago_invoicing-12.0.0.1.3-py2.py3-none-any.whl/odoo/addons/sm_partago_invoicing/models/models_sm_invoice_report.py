# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.sm_maintenance.models.models_sm_utils import sm_utils
from odoo.addons.sm_partago_invoicing.models.batch_type_enum import BatchType
from odoo.tools.translate import _
from datetime import datetime
import openerp.addons.decimal_precision as dp

class sm_invoice_report(models.Model):
  _name = 'sm.invoice_report'
  _inherit = ['mail.thread']
  _description = "CS Invoice Report"

  name = fields.Char(string=_("Name"), store=True)
  partner_id = fields.Many2one('res.partner', string=_("Partner"))
  cs_line_ids = fields.One2many(comodel_name='account.invoice.line',
    inverse_name='invoice_report_id',string='Lines')
  previous_pocketbook = fields.Float(string=_("Pocketbook state initial"))
  previous_pocketbook_taxed = fields.Float(string=_("Pocketbook state initial (taxed)"))
  final_pocketbook = fields.Float(string=_("Pocketbook state final"))
  final_pocketbook_taxed = fields.Float(string=_("Pocketbook state final (taxed)"))
  total_amount_lines_untaxed = fields.Float(string=_("Total in lines (untaxed)"),
    compute="_get_total_amount_lines_untaxed")
  discount_amount_subtotal = fields.Float(string=_("Discount amount (untaxed)"),
    compute="_get_discount_amount_subtotal")
  total_mileage = fields.Float(string=_("Total mileage"),compute="_get_total_mileage")
  ir_total_amount_signed = fields.Float(string=_("Amount to pay (untaxed)(signed)"),
    compute="_get_total_amount_signed")
  invoice_id = fields.Many2one('account.invoice', string=_("Related Invoice"))
  date = fields.Date(string=_("Date"))
  company_id = fields.Many2one('res.company', string=_('Company'))
  grouped_report = fields.Boolean(string=_("Is a grouped report?"))
  timeframe_desc = fields.Char(string=_("Timeframe description"))
  email_sent = fields.Boolean(string=_("Email sent?"))
  predetermined_tariff = fields.Char(string=_("Predetermined tariff"),
    compute="prepapre_predetermined_tariff")
  predetermined_tariff_description = fields.Html(string=_("predetermined tariff description"))
  related_batch_reservation_ids = fields.One2many(comodel_name='smp.sm_batch_reservation_compute',
    inverse_name='invoice_report_id',string=_("Related batch reservation (grouped)"))
  related_report_reservation_ids = fields.One2many(comodel_name='smp.sm_report_reservation_compute',
    inverse_name='invoice_report_id',string=_("Related report reservation (single)"))
  total_amount_in_invoice = fields.Float(string=_('Total amount on invoice'),
    compute="_get_total_amount_in_invoice")
  total_taxes_in_invoice = fields.Float(string=_('Total taxes on invoice'),
    compute="_get_total_taxes_in_invoice")
  ####################################################################################################################
  # DEPRECATED
  ####################################################################################################################
  has_cs_usage = fields.Boolean(string=_("Has carsharing usage"),
    compute="_has_cs_usage", store=False)
  has_teletacs = fields.Boolean(string=_("Has teletacs"),
    compute="_has_teletac_lines", store=False)
  show_payment_info = fields.Boolean(string=_("Show payment info?"),
    compute="_show_payment_info", store=False)
  initial_price = fields.Float(string=_("Initial price (deprecated)"))
  total_amount_lines_taxed_no_initial = fields.Float(
    string=_("Total in lines (taxed) sense preu inicial (deprecated)"))
  total_amount_lines_taxed = fields.Float(string=_("Total in lines (taxed) (deprecated)"))
  fixed_amount_topay = fields.Float(string=_("Minimum fixed amount to pay (deprecated)"))
  afterfee_pocketbook = fields.Float(string=_("Pocketbook state after adding fee (deprecated)"))
  discount_amount = fields.Float(string=_("Pocketbook discount (deprecated)"))
  total_amount = fields.Float(string=_("Amount to pay (deprecated)"))
  total_amount_signed = fields.Float(string=_("Amount to pay (signed) (deprecated)"))

  _order = "create_date desc"

  @api.depends('invoice_id')
  def _get_total_amount_in_invoice(self):
    for record in self:
      if record.invoice_id:
        record.total_amount_in_invoice = record.invoice_id.amount_total

  @api.depends('invoice_id')
  def _get_total_taxes_in_invoice(self):
    for record in self:
      if record.invoice_id:
        record.total_taxes_in_invoice = record.invoice_id.amount_tax

  @api.depends('cs_line_ids')
  def _get_total_amount_lines_untaxed(self):
    for record in self:
      amount = 0
      if record.cs_line_ids.exists():
        for line in record.cs_line_ids:
          if line.line_type == 'cs_default' or line.line_type == 'cs_extra' or line.line_type == 'cs_teletac':
            amount += line.price_subtotal_signed
      record.total_amount_lines_untaxed = amount


  @api.depends('cs_line_ids')
  def _get_discount_amount_subtotal(self):
    for record in self:
      discount = 0
      if record.cs_line_ids.exists():
        for line in record.cs_line_ids:
          if line.line_type == 'cs_discount':
            discount += line.price_subtotal_signed
      record.discount_amount_subtotal = discount

  @api.depends('cs_line_ids')
  def _get_total_mileage(self):
    for record in self:
      mileage = 0
      if record.cs_line_ids.exists():
        for line in record.cs_line_ids:
          if line.line_type == 'cs_default' and line.related_reservation_compute_id.id != False:
            mileage += line.related_reservation_compute_id.used_mileage
      record.total_mileage = mileage

  @api.depends('cs_line_ids')
  def _get_total_amount_signed(self):
    for record in self:
      amount = 0
      if record.cs_line_ids.exists():
        for line in record.cs_line_ids:
          amount += line.price_subtotal_signed
      record.ir_total_amount_signed = amount

  @api.depends('cs_line_ids')
  def _has_cs_usage(self):
    for record in self:
      has_cs_usage = False
      if record.cs_line_ids.exists():
        for line in record.cs_line_ids:
          if line.line_type == 'cs_default' or line.line_type == 'cs_extra':
            has_cs_usage = True
      record.has_cs_usage = has_cs_usage

  @api.depends('cs_line_ids')
  def _has_teletac_lines(self):
    for record in self:
      has_teletacs = False
      if record.cs_line_ids.exists():
        for line in record.cs_line_ids:
          if line.line_type == 'cs_teletac':
            has_teletacs = True
      record.has_teletacs = has_teletacs

  def assign_previous_pocketbook(self):
    self.write({
      'previous_pocketbook': self.partner_id.pocketbook_records_total,
      'previous_pocketbook_taxed': self.partner_id.pocketbook_records_total_taxed
    })

  @api.model
  def prepapre_predetermined_tariff(self):
    company = self.env.user.company_id
    self.predetermined_tariff = company.default_tariff_model_id.name
    self.predetermined_tariff_description = company.default_tariff_model_id.description

  @api.model
  def _show_payment_info(self):
    self.show_payment_info = False
    batch_reservation = self.env['smp.sm_batch_reservation_compute'].search([('invoice_report_id', '=', self.id)])
    if batch_reservation.exists():
      self.show_payment_info = True
    else:
      report_reservation_computes = self.env['smp.sm_report_reservation_compute'].search(
        [('invoice_report_id', '=', self.id)])
      if report_reservation_computes.exists():
        if not report_reservation_computes[0].batch_reservation_compute_id.invoice_report_id.id:
          self.show_payment_info = True

  def create_discount_lines(self):
    company = self.env.user.company_id
    discount_product = company.cs_discount_product_id
    default_line_account = discount_product.property_account_income_id
    taxes_l = []
    # total_amount_taxed = self.total_amount_lines_taxed
    total_amount_untaxed = self.total_amount_lines_untaxed

    if discount_product.taxes_id.exists():
      for tax in discount_product.taxes_id:
        taxes_l.append((4, tax.id))

    pb_records = self.env['pocketbook.pocketbook_record'].search(
      [('amount', '>', '0'), ('related_member_id', '=',self.partner_id.id)])
    if pb_records.exists():
      for pb_record in pb_records:
        invoice_line_name = _("Descompte: ") + pb_record.name
        if pb_record.related_account_id.id != False:
          line_account = pb_record.related_account_id
        else:
          line_account = default_line_account
        if pb_record.amount >= total_amount_untaxed:
          # create discount amount for total_amount_lines_untaxed and break
          descompte_line = self.env['account.invoice.line'].create({
            'name': invoice_line_name,
            'invoice_report_id': self.id,
            'product_id': discount_product.id,
            'price_unit': -1 * total_amount_untaxed,
            'quantity': 1,
            'discount': 0,
            'account_id': line_account.id,
            'account_analytic_id': pb_record.related_analytic_account_id.id,
            'line_type': 'cs_discount',
            'partner_id': self.partner_id.id
          })
          descompte_line.invoice_line_tax_ids = taxes_l
          pb_record_history = self.env['pocketbook.pocketbook_record_history'].create({
            'name': 'Report: '+self.name,
            'date': datetime.now(),
            'amount': -1 * total_amount_untaxed,
            'related_invoice_line_id': descompte_line.id,
            'related_pb_record_id': pb_record.id
          })
          break
        else:
          # create discount amount for pb_record.amount
          descompte_line = self.env['account.invoice.line'].create({
            'name': invoice_line_name,
            'invoice_report_id': self.id,
            'product_id': discount_product.id,
            'price_unit': -1 * pb_record.amount,
            'quantity': 1,
            'discount': 0,
            'account_id': line_account.id,
            'account_analytic_id': pb_record.related_analytic_account_id.id,
            'line_type': 'cs_discount',
            'partner_id': self.partner_id.id
          })
          descompte_line.invoice_line_tax_ids = taxes_l
          total_amount_untaxed = total_amount_untaxed + descompte_line.price_subtotal_signed
          # total_amount_taxed = total_amount_taxed - descompte_line.price_unit - descompte_line.tax_par_line
          pb_record_history = self.env['pocketbook.pocketbook_record_history'].create({
            'name': 'Report: ' + self.name,
            'date': datetime.now(),
            'amount': -1 * pb_record.amount,
            'related_invoice_line_id': descompte_line.id,
            'related_pb_record_id': pb_record.id
          })

  def create_related_invoice(self,batch_type=False):
    company = self.env.user.company_id

    # TODO: This could be done better? a map somewhere
    # setup invoice template based on batch_type
    invoice_template = 'default'
    if batch_type:
      if batch_type == 'usage':
        invoice_template = 'cs_default'
      if batch_type == 'teletac':
        invoice_template = 'cs_teletac'

    invoice_vals = {
      'partner_id': self.partner_id.id,
      'amount_tax': 5,
      'company_id': 1,
      'state': 'draft',
      'type': 'out_invoice',
      'journal_id': company.cs_invoice_journal_id.id,
      'invoice_email_sent': False,
      'invoice_report_id': self.id,
      'invoice_template': invoice_template
      # 'is_sm_invoice': True
    }
    # Assign payment mode only if the partner has at least one valid mandate #
    mandates = self.env['account.banking.mandate'].search([('partner_id', '=', self.partner_id.id),('state','=','valid')])
    if mandates.exists():
      invoice_vals['payment_mode_id'] = company.cs_invoice_payment_mode_id.id

    invoice = self.env['account.invoice'].create(invoice_vals)

    if self.cs_line_ids.exists():
      for rep_line in self.cs_line_ids:
        inv_line = rep_line.copy({'invoice_report_id':False,'invoice_id':invoice.id})
        if rep_line.line_type == 'cs_teletac':
          if rep_line.related_reservation_compute_id.id:
            query = [
              ('reservation_compute_id', '=',
               rep_line.related_reservation_compute_id.id)
            ]
            teletacs = self.env['smp.sm_teletac'].search(query)
            if teletacs.exists():
              teletacs[0].write({
                'related_invoice_id': invoice.id
              })
    invoice.compute_taxes()
    self.update_pocketbook_finals()
    self.write({
      'invoice_id': invoice.id
    })

  def validate_related_invoice(self):
    if self.invoice_id.id != False:
      self.invoice_id.action_invoice_open()

  def update_pocketbook_finals(self):
    self.write({
      'final_pocketbook': self.partner_id.pocketbook_records_total,
      'final_pocketbook_taxed': self.partner_id.pocketbook_records_total_taxed
    })

  @api.multi
  def action_report_sent(self):
    self.ensure_one()
    self.send_carsharing_report_email()

  def send_carsharing_report_email(self, record=None):
    if record is None:
      record = self

    company = record.env.user.company_id
    email_template = company.invoice_report_mail_template_id

    if email_template.id:
      email_values = {'send_from_code': True}
      email_template.with_context(email_values).send_mail(record.id, True)

  def compute_report_lines(self, compute_pb, type_of_batch_to_compute):
    batch_reservation = self.env['smp.sm_batch_reservation_compute'].search([('invoice_report_id', '=', self.id)])

    if BatchType.USAGES.value in type_of_batch_to_compute:
      if batch_reservation:
        if batch_reservation.reports_id.exists():
          for report in batch_reservation.reports_id:
            for compute in report.reservation_computes_id:
              self.generate_invoice_report_line(compute, compute_pb)
      else:
        report_reservation_compute = self.env['smp.sm_report_reservation_compute'].search([
          ('invoice_report_id', '=', self.id)
        ])

        if report_reservation_compute:
          for compute in report_reservation_compute:
            for x in compute.reservation_computes_id:
              self.generate_invoice_report_line(x, compute_pb)

    if BatchType.TELETAC.value in type_of_batch_to_compute:
      # Don't update pocketbook tariff when applies to teletac
      compute_teletacs_pb = False
      if batch_reservation:
        if batch_reservation.reports_id.exists():
          for report in batch_reservation.reports_id:
            self.generate_teletac_lines(compute_pb=compute_teletacs_pb, rel_teletacs=report.teletacs_compute_id)
      else:
        report_reservation_compute = self.env['smp.sm_report_reservation_compute'].search(
          [('invoice_report_id', '=', self.id)])

        if report_reservation_compute:
          for compute in report_reservation_compute:
            self.generate_teletac_lines(compute_pb=compute_teletacs_pb, rel_teletacs=compute.teletacs_compute_id)

  def generate_invoice_report_line(self, compute, compute_pb):
    company = self.env.user.company_id
    invoice_report = self
    cs_product = company.cs_carsharing_product_id

    if cs_product.id:
      line_member = compute.member_id
      member = invoice_report.partner_id
      taxes_l = []
      line_account = cs_product.property_account_income_id
      line_analytic_account = compute.get_analytic_account()


      if cs_product.taxes_id.exists():
        for tax in cs_product.taxes_id:
          taxes_l.append((4, tax.id))

      tariff = member.get_current_tariff(compute.carconfig_id)

      compute.compute_report_invoice_vals(tariff)  # computing invoice vals for compute

      if tariff['tariff_aval']:
        quantity_time = compute.compute_invoice_report_tariff_time_quantities(tariff['tariff_model_id'])
        quantity_tariff_extra = compute.compute_invoice_report_nontariff_time_quantities(tariff['extra_tariff_model_id'])
      else:
        quantity_time = compute.compute_invoice_report_nontariff_time_quantities(tariff['tariff_model_id'])
        quantity_tariff_extra = 0

      line_quantity = quantity_time + compute.compute_invoice_report_km_quantities(tariff['tariff_model_id'])

      # calculate invoice line name
      invoice_line_name = ''
      if compute:
        invoice_line_name = compute.name_nice

      query = [
        ('name', '=', invoice_line_name),
        ('invoice_report_id', '=', invoice_report.id),
        ('product_id', '=', cs_product.id),
        ('related_reservation_compute_id', '=', compute.id)
      ]
      creation_data = {
        'name': invoice_line_name,
        'invoice_report_id': invoice_report.id,
        'product_id': cs_product.id,
        'price_unit': line_quantity,
        'quantity': 1,
        'discount': 0,
        'account_id': line_account.id,
        'account_analytic_id': line_analytic_account.id,
        'related_reservation_compute_id': compute.id,
        'line_type': 'cs_default'
        # 'line_tariff_type': tariff['tariff_model_type']
      }

      if compute.cs_carconfig_id:
        line_quantity = line_quantity +  compute.cs_carconfig_id.initial_price

      invoice_line = sm_utils.get_create_existing_model(self.env['account.invoice.line'], query, creation_data)

      invoice_line.write({
        'partner_id': line_member.id,
        'related_tariff_id': tariff['tariff_id'],
        'price_unit': line_quantity
      })

      member.update_member_tariff_by_invoice_line(invoice_line, compute_pb)

      # adding taxes that apply
      invoice_line.invoice_line_tax_ids = taxes_l

      if quantity_tariff_extra != 0:
        invoice_line_name = "Temps extra: " + invoice_line_name

        query = [
          ('name', '=', invoice_line_name),
          ('invoice_report_id', '=', invoice_report.id),
          ('product_id', '=', cs_product.id),
          ('related_reservation_compute_id', '=', compute.id)
        ]
        creation_data = {
          'name': invoice_line_name,
          'invoice_report_id': invoice_report.id,
          'product_id': cs_product.id,
          'price_unit': quantity_tariff_extra,
          'quantity': 1,
          'discount': 0,
          'account_id': line_account.id,
          'account_analytic_id': line_analytic_account.id,
          'related_reservation_compute_id': compute.id,
          'line_type': 'cs_extra',
          # 'line_tariff_type': tariff['tariff_model_type']
        }
        invoice_line_extra = sm_utils.get_create_existing_model(self.env['account.invoice.line'], query,
                                    creation_data)

        invoice_line_extra.write({
          'partner_id': line_member.id,
          'related_tariff_id': tariff['tariff_id'],
          'price_unit': quantity_tariff_extra
        })
        member.update_member_tariff_by_invoice_line(invoice_line_extra, compute_pb)

        # adding taxes that apply
        invoice_line_extra.invoice_line_tax_ids = taxes_l

      return invoice_line
    return False

  def generate_teletac_lines(self, compute_pb, rel_teletacs):
    # check if there is viat related products
    company = self.env.user.company_id
    teletac_p = company.cs_teletac_product_id

    # rel_teletacs = self.env['smp.sm_teletac'].search([('reservation_compute_id', '=', compute.id)])

    if teletac_p.id != False and rel_teletacs.exists():
      taxes_l = []
      if teletac_p.taxes_id.exists():
        for tax in teletac_p.taxes_id:
          taxes_l.append((4, tax.id))
      for rel_teletac in rel_teletacs:
        if rel_teletac.id:
          line_analytic_account = rel_teletac.get_analytic_account()
          if not rel_teletac.related_invoice_id.id:
            invoice_line_name = rel_teletac.description + ' (' + str(rel_teletac.date) + ')'
            t_quantity = rel_teletac.amount - rel_teletac.discount

            query = [
              ('name', '=', invoice_line_name),
              ('invoice_report_id', '=', self.id),
              ('product_id', '=', teletac_p.id),
              ('related_reservation_compute_id', '=', rel_teletac.reservation_compute_id.id)
            ]
            creation_data = {
              'name': invoice_line_name,
              'invoice_report_id': self.id,
              'product_id': teletac_p.id,
              'price_unit': t_quantity,
              'quantity': 1,
              'discount': 0,
              'account_id': teletac_p.property_account_income_id.id,
              'account_analytic_id': line_analytic_account.id,
              'related_reservation_compute_id': rel_teletac.reservation_compute_id.id,
              'partner_id': rel_teletac.related_member_id.id,
              'line_type': 'cs_teletac'
            }

            teletac_line = sm_utils.get_create_existing_model(model_env=self.env['account.invoice.line'],
                                      query=query,
                                      creation_data=creation_data)

            # TO-DO: need to investigate why can't we pass this on line creation (previous function)
            teletac_line.write({
              'partner_id': rel_teletac.related_member_id.id
            })

            teletac_line.invoice_line_tax_ids = taxes_l

            rel_teletac.sudo().write({
              'invoice_report_id': self.id
            })
            # we don't update member tariff for teletacs lines
            # self.partner_id.update_member_tariff_by_invoice_line(teletac_line, compute_pb)