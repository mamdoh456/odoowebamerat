# -*- coding: utf-8 -*-

import babel.dates
import time
import pytz
from datetime import timedelta, datetime
from dateutil import tz

from odoo import http, fields
from odoo.http import request
from odoo.tools.translate import _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager
from odoo.addons.website.controllers.main import Website


class HMSWebsite(Website):

    # Appointment Booking
    def create_booking_data(self, product_id=None):
        user = request.env['res.users'].sudo().browse(request.uid)
        values = {
            'error': {},
            'error_message': []
        }

        department_ids = request.env['hr.department'].sudo().search(
            [('patient_department', '=', True), ('allowed_online_booking', '=', True)])

        domain_phy = [('allowed_online_booking', '=', True)]
        if product_id:
            domain_phy += [('product_services_ids', 'in', product_id)]
        coiffure_ids = request.env['hms.coiffure'].sudo().search(domain_phy)

        values.update({
            'slots': [],
            'slot_lines': [],
            'partner': user.partner_id,
            'department_ids': department_ids,
            'coiffure_ids': coiffure_ids,
            'appointment_tz': False,
            'allow_department_selection': True if department_ids else False,
            'allow_coiffure_selection': True if coiffure_ids else False,
        })
        return values

    def user_booking_data(self, post):
        values = {
            'error': {},
            'error_message': []
        }
        coiffure_id = post.get('coiffure_id', False)
        department_id = post.get('department_id', False)
        appoitment_by = post.get('appoitment_by', 'coiffure')
        coiffure = department = ''
        allow_home_appointment = False

        if coiffure_id:
            coiffure = request.env['hms.coiffure'].sudo().search([('id', '=', int(coiffure_id))])
            allow_home_appointment = coiffure.allow_home_appointment
        if department_id:
            department = request.env['hr.department'].sudo().search([('id', '=', int(department_id))])
            allow_home_appointment = department.allow_home_appointment
        if appoitment_by == 'coiffure':
            department = ''
        if appoitment_by == 'department':
            coiffure = ''

        slot_data = request.env['hms.appointment'].get_slot_data(coiffure_id, department_id)
        user = request.env['res.users'].sudo().browse(request.uid)

        schedule_slot_id = False
        schedule_slot_name = schedule_slot_date = ''
        if post.get('schedule_slot_id'):
            slot_line = request.env['appointment.schedule.slot.lines'].browse(int(post.get('schedule_slot_id')))
            schedule_slot_name = slot_line.name
            schedule_slot_date = slot_line.slot_id.slot_date
            schedule_slot_id = slot_line.id

        values.update({
            'terms_page_link': user.company_id.acs_appointment_tc,
            'department_id': department_id,
            'department': department,
            'coiffure_id': coiffure_id,
            'coiffure': coiffure,
            'partner': user.partner_id,
            'slots_data': slot_data,
            'schedule_slot_id': schedule_slot_id,
            'schedule_slot_name': schedule_slot_name,
            'schedule_slot_date': schedule_slot_date,
            'allow_home_appointment': allow_home_appointment,
        })
        return values

    @http.route(['/create/appointment', '/create/appointment/<int:product_id>'], type='http', auth='public',
                website=True, sitemap=True)
    def create_appointment(self, redirect=None, product_id=None, **post):
        values = self.create_booking_data(product_id)
        values.update({
            'product_id': product_id or None,
            'redirect': redirect,
        })
        return request.render("acs_hms_online_appointment.appointment_details", values)

    @http.route(['/get/appointment/data'], type='http', auth='public', website=True, sitemap=False)
    def create_appointment_data(self, redirect=None, **post):
        appoitment_by = post.get('appoitment_by', 'coiffure')
        if appoitment_by == 'coiffure' and 'department_id' in post:
            post.pop('department_id')
        if appoitment_by == 'department' and 'coiffure_id' in post:
            post.pop('coiffure_id')
        values = self.user_booking_data(post)
        return request.render("acs_hms_online_appointment.appointment_slot_details", values)

    @http.route(['/get/appointment/personaldata'], type='http', auth='public', website=True, sitemap=False)
    def appointment_personal_data(self, redirect=None, **post):
        values = self.user_booking_data(post)
        return request.render("acs_hms_online_appointment.appointment_personal_details", values)

    def cart_update(self, product_id, add_qty=1, set_qty=0, partner=False, **kw):
        """This route is called when adding a product to cart (no options)."""
        sale_order = request.website.sale_get_order(force_create=True)
        if partner:
            sale_order.partner_id = partner
        if sale_order.state != 'draft':
            request.session['sale_order_id'] = None
            sale_order = request.website.sale_get_order(force_create=True)

        product_custom_attribute_values = None
        if kw.get('product_custom_attribute_values'):
            product_custom_attribute_values = json.loads(kw.get('product_custom_attribute_values'))

        no_variant_attribute_values = None
        if kw.get('no_variant_attribute_values'):
            no_variant_attribute_values = json.loads(kw.get('no_variant_attribute_values'))

        sale_order._cart_update(
            product_id=int(product_id),
            add_qty=add_qty,
            set_qty=set_qty,
            product_custom_attribute_values=product_custom_attribute_values,
            no_variant_attribute_values=no_variant_attribute_values
        )
        for line in sale_order.order_line.filtered(lambda l: l.product_id.need_partial_payment == True):
            line.price_unit = line.price_unit - (line.price_unit * line.product_id.advance_payment_amount)
        return True



    def validate_application_details(self, patient, data):
        error = dict()
        error_message = []
        mandatory_fields = ['schedule_slot_id']

        # If no patient
        # if not patient:
        #     error_message.append(
        #         _('No patient is linked with user. Please Contact Administration for further support.'))

        if not data.get('schedule_slot_id'):
            error_message.append(_('Please Select Available Appointment Slot Properly.'))

        # Mandatory Field Validation
        for field_name in mandatory_fields:
            if not data.get(field_name):
                error[field_name] = 'missing'

        # error message for empty required fields
        if [err for err in error.values() if err == 'missing']:
            error_message.append(_('Some required fields are empty.'))

        return error, error_message
