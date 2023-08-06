# -*- coding: utf-8 -*-

from datetime import datetime

from odoo import models, fields, api
from odoo.addons.sm_maintenance.models.models_sm_utils import sm_utils
from odoo.tools.translate import _

from odoo.addons.sm_partago_invoicing.models.batch_type_enum import BatchType


def clean_maintenance_users_reservation(initial_list):
  return initial_list.filtered(lambda r: r.member_id.cs_user_type != 'maintenance')


def clean_promo_users_reservation(initial_list):
  return initial_list.filtered(lambda r: r.member_id.cs_user_type != 'promo')


def clean_maintenance_users_teletacs(initial_list):
  return initial_list.filtered(lambda r: r.reservation_compute_id.member_id.cs_user_type != 'maintenance')


def clean_promo_users_teletacs(initial_list):
  return initial_list.filtered(lambda r: r.reservation_compute_id.member_id.cs_user_type != 'promo')


class sm_batch_reservation_compute_wizard(models.TransientModel):
  _name = "sm_partago_invoicing.sm_batch_reservation_compute.wizard"

  description = fields.Char(string=_('Description'))

  compute_reservations = fields.Boolean(string=_("Compute reservations"))
  compute_teletacs = fields.Boolean(string=_("Compute teletacs"))

  batch_type = fields.Selection([
    (str(BatchType.USAGES.value), 'Reservations'),
    (str(BatchType.TELETAC.value), 'Teletacs'),
  ], string=_("Batch type"), store=True)

  reservations = fields.Many2many(
    'smp.sm_reservation_compute',
    relation="smp_reservation_wizard_relation",
    # column1="wizard_id",
    # column2="reservation_id",
    string=_("Reservations"),
    ondelete='cascade'
  )

  teletacs = fields.Many2many(
    'smp.sm_teletac',
    relation="smp_teletacs_wizard_relation",
    # column1="wizard_id",
    # column2="teletac_id",
    string=_("Teletacs"),
    ondelete='cascade'
  )

  @api.multi
  def create_batch(self):
    self.create_batch_compute()

  @api.model
  def create_batch_compute(self):

    if self.compute_reservations:
      list_to_process = self.discard_invalid_reservations()
      self.create_reservation_batch_for_companies(list_to_process)
      self.create_reservation_batch_for_users(list_to_process)

    if self.compute_teletacs:
      list_to_process = self.discard_invalid_teletacs()
      self.create_teletac_batch_for_companies(list_to_process)
      self.create_teletac_batch_for_users(list_to_process)

  def discard_invalid_reservations(self):
    final_list = clean_maintenance_users_reservation(self.reservations)
    final_list = clean_promo_users_reservation(final_list)

    return final_list

  def discard_invalid_teletacs(self):
    final_list = clean_maintenance_users_teletacs(self.teletacs)

    return final_list

  def create_teletac_batch_for_users(self, list_to_process):
    individual_usages = list_to_process.filtered(
      lambda t: t.reservation_compute_id.related_company_object.id is False and 
      t.related_member_id.parent_id.id is False and t.related_member_id.is_company is False)

    teletac_usages = individual_usages.filtered(
      lambda t: t.reservation_compute_id.id is not False)
    if teletac_usages:
      self.process_teletacs(batch_to_process=teletac_usages)

  def create_teletac_batch_for_companies(self, list_to_process):
    company_usages = list_to_process.filtered(
      lambda t: t.reservation_compute_id.related_company_object.id is not False or 
      t.related_member_id.parent_id or t.related_member_id.is_company)

    companies = {}

    for teletac_usage in company_usages:
      company = teletac_usage.reservation_compute_id.related_company_object

      if not company:
        company = teletac_usage.related_member_id.parent_id

      if company.paymaster.id is not False:
        company = company.paymaster

      company_batches = companies.get(company)

      if company_batches is None:
        companies[company] = []

      companies.get(company).append(teletac_usage)

    for company, company_teletacs in companies.items():
      self.process_teletacs(batch_to_process=company_teletacs, company=company)

  def create_reservation_batch_for_users(self, list_to_process):
    # Only individual reservations
    individual_usages = list_to_process.filtered(
      lambda r: r.related_company_object.id is False and r.member_id.parent_id.id is False and 
      r.member_id.is_company is False)
    
    if individual_usages:
      self.process_reservations(batch_to_process=individual_usages)

  def create_reservation_batch_for_companies(self, list_to_process):
    company_usages = list_to_process.filtered(
      lambda r: r.related_company_object.id is not False or r.member_id.parent_id or r.member_id.is_company)

    companies = {}

    for reservation in company_usages:
      company = reservation.related_company_object  # Looks for reservation compute related company

      if not company:
        company = reservation.member_id.parent_id  # Looks for reservation member parent

        if not company and reservation.member_id.is_company:  # Looks if the reservation member is a company
          company = reservation.member_id

      if company.paymaster.id is not False:
        company = company.paymaster

      company_batches = companies.get(company)

      if company_batches is None:
        companies[company] = []

      companies.get(company).append(reservation)

    for company, company_reservations in companies.items():
      self.process_reservations(company=company, batch_to_process=company_reservations)

  @api.model
  def process_teletacs(self, batch_to_process, company=False):

    batch = sm_utils.get_create_existing_model(model_env=self.env['smp.sm_batch_reservation_compute'],
      query=[('name', '=', datetime.now())], creation_data={'name': datetime.now(),
      'batch_type': BatchType.TELETAC.value})
    
    for teletac in batch_to_process:
      member = teletac.reservation_compute_id.member_id
      report_name = batch.name + '-' + member.name

      report = sm_utils.get_create_existing_model(model_env=self.env['smp.sm_report_reservation_compute'],
        query=[('name', '=', report_name)],creation_data={
        'name': report_name,'report_type': BatchType.TELETAC.value,'member_id': member.id,
        'batch_reservation_compute_id': batch.id})

      teletac.write({
        'report_reservation_compute_id': report.id
      })

    batch.description = self.compute_batch_description(batch_to_process=batch_to_process,company=company,batch_type=BatchType.TELETAC.value)

    return True

  @api.model
  def process_reservations(self, batch_to_process, company=False):

    batch = sm_utils.get_create_existing_model(model_env=self.env['smp.sm_batch_reservation_compute'],
      query=[('name', '=', datetime.now())],creation_data={
      'name': datetime.now(),'batch_type': BatchType.USAGES.value})

    for compute in batch_to_process:
      if not compute.compute_invoiced and not compute.compute_forgiven:
        report_name = batch.name + '-' + compute.member_id.name
        report = sm_utils.get_create_existing_model(model_env=self.env['smp.sm_report_reservation_compute'],
          query=[('name', '=', report_name)],creation_data={
          'name': report_name,'member_id': compute.member_id.id,
          'report_type': BatchType.USAGES.value,'batch_reservation_compute_id': batch.id})

        compute.write({
          'report_reservation_compute_id': report.id,
          'compute_invoiced': True
        })

    batch.description = self.compute_batch_description(batch_to_process=batch_to_process,company=company,batch_type=BatchType.USAGES.value)

    return True

  def compute_batch_description(self, batch_to_process, company, batch_type):

    batch_description = self.description

    if company:
      batch_description += " - " + company.name

    return batch_description

