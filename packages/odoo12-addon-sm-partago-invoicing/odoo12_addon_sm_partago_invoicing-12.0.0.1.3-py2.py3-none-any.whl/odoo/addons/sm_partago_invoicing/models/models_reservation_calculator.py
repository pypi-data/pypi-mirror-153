# -*- coding: utf-8 -*-
from datetime import datetime

class reservation_calculator(object):

  @staticmethod
  def get_general_values(compute, comesFrom):

    update_values = {}

    if comesFrom == 'object':
      effectiveStartTime = datetime.strptime(str(compute.effectiveStartTime), "%Y-%m-%d %H:%M:%S")
      startTime = datetime.strptime(str(compute.startTime), "%Y-%m-%d %H:%M:%S")
      effectiveEndTime = datetime.strptime(str(compute.effectiveEndTime), "%Y-%m-%d %H:%M:%S")
      endTime = datetime.strptime(str(compute.endTime), "%Y-%m-%d %H:%M:%S")
    elif comesFrom == 'list':
      effectiveStartTime = compute['effectiveStartTime']
      startTime = compute['startTime']
      effectiveEndTime = compute['effectiveEndTime']
      endTime = compute['endTime']

    if effectiveStartTime < startTime:
      real_start = effectiveStartTime
    else:
      real_start = startTime

    # Calculate real end for computation
    if effectiveEndTime < endTime:
      real_end = effectiveEndTime
    else:
      real_end = endTime

    update_values['usage_mins'] = (real_end - real_start).total_seconds() / 60.0

    if endTime >= effectiveEndTime:
      update_values['non_usage_mins'] = (endTime - effectiveEndTime).total_seconds() / 60.0
      update_values['extra_usage_mins'] = 0

    else:
      update_values['extra_usage_mins'] = (effectiveEndTime - endTime).total_seconds() / 60.0
      update_values['non_usage_mins'] = 0

    return update_values

  @staticmethod
  def decouple_reservation_days_and_mins(rmins):
    max_mins_day = 10 * 60
    twenty_hours_mins = 24 * 60

    invoice_days = 0
    invoice_mins = 0
    computing = True

    while computing:
      if rmins >= max_mins_day:
        if rmins >= twenty_hours_mins:
          invoice_days = invoice_days + 1
          rmins = rmins - twenty_hours_mins
        else:
          invoice_days = invoice_days + 1
          saved_by_day_mins = rmins - max_mins_day
          computing = False
      else:
        invoice_mins = rmins
        computing = False
    return {
      'days': invoice_days,
      'mins': invoice_mins
    }

  @staticmethod
  def get_hours_from_minutes(minutes):
    return minutes / 60
