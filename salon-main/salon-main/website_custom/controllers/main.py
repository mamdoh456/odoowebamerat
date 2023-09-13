from odoo import http, fields
from odoo.http import request
from odoo.addons.acs_hms_online_appointment.controllers.main import HMSWebsite
import json
from datetime import timedelta, datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT



class HMSWebsiteInherit(HMSWebsite):

    def check_have_slots(self, staff_id):
        last_date = fields.Date.today() + timedelta(
            days=request.env.user.sudo().company_id.allowed_booking_online_days)
        domain = [('coiffure_id', '=', int(staff_id)), ('slot_date', '>=', fields.Date.today()),
                  ('slot_date', '<=', last_date)]
        slots = request.env['appointment.schedule.slot'].sudo().search(domain)
        if slots:
            return True
        return False

    def staff_availability(self, product_id, appointment_type=False):
        """This function checks if there are employees available in this service"""
        domain = [('product_services_ids', 'in', product_id)]
        if appointment_type and appointment_type == 'home_booking':
            domain += [('allow_home_appointment', '=', True)]
        staff_ids = request.env['hms.coiffure'].sudo().search(domain)
        for staff_id in staff_ids:
            have_slots = self.check_have_slots(staff_id)
            if have_slots:
                return True
        return False

    def prepare_data_invoice(self, product_ids):
        """This function returns details of the invoice displayed in the appointment process"""
        appointment_booking = request.session.appointment_booking
        total = 0
        products = request.env['product.product'].sudo().search_read([('id', 'in', product_ids)],
                                                                     ['name', 'list_price', 'time'])
        for p in products:
            p['time'] = self.covert_time_float_to_text(p['time'])
            total += p['list_price']

            item = next((item for item in appointment_booking if item["product_id"] == p['id']), False)

            # Display staff name
            if item and item.get('staff_id', False):
                p['staff_name'] = request.env['hms.coiffure'].sudo().search(
                    [('id', '=', int(item.get('staff_id')))]).name
            else:
                p['staff_name'] = ''

            # Display date and time
            p['date_time'] = ''
            if item and item.get('slot_date', False):
                slot_date = request.env['appointment.schedule.slot'].sudo().search(
                    [('id', '=', int(item.get('slot_date')))])
                p['date_time'] += slot_date.slot_date.strftime("%d %B %Y")
            if item and item.get('schedule_slot_id', False):
                schedule_slot_id = request.env['appointment.schedule.slot.lines'].sudo().search(
                    [('id', '=', int(item.get('schedule_slot_id')))])
                p['date_time'] += " at " + schedule_slot_id.name

        return {'products': products, 'total': total}

    def covert_time_float_to_text(self, time):
        t = h = m = ''
        if time:
            time = str(timedelta(hours=time)).rsplit(':', 1)[0]
            time = time.split(':')
            if time[0] and int(time[0]) > 0:
                h = time[0] + 'h'
            if time[1] and int(time[1]) > 0:
                m = time[1] + 'min'
            if h and m:
                t = h + ' and ' + m
            elif h and not m:
                t = h
            elif m and not h:
                t = m
        return t

    def get_categories_services(self, post):
        domain = [('is_published', '=', True), ('type', '=', 'service')]
        appointment_type = post.get('appointment_type', False)
        if appointment_type and appointment_type == 'home_booking':
            domain += [('home_booking', '=', True)]
        elif appointment_type and appointment_type == 'local_reservation':
            domain += [('local_reservation', '=', True)]
        product_ids = request.env['product.product'].sudo().search(domain)
        categories = product_ids.filtered(lambda p: p.categ_id.parent_id.id == request.env.ref(
            'website_custom.product_category_appointment').id).mapped('categ_id')
        return categories

    @http.route(['/appointment/<appointment_type>/services'], type='http', auth='public', website=True, sitemap=True)
    def categories_services(self, **post):
        values = {
            "appointment_type": post.get('appointment_type', False),
            "categories": self.get_categories_services(post)
        }
        return request.render("website_custom.categories_services", values)

    @http.route(['/appointment/<appointment_type>/booking'], type='http', auth='public', website=True, sitemap=True)
    def services_appointment(self, **post):
        domain = [('is_published', '=', True), ('type', '=', 'service')]
        appointment_type = post.get('appointment_type', False)
        if appointment_type and appointment_type == 'home_booking':
            domain += [('home_booking', '=', True)]
        elif appointment_type and appointment_type == 'local_reservation':
            domain += [('local_reservation', '=', True)]
        categories = self.get_categories_services(post)

        # get all products ids selected
        product_selected_ids = [int(v) for k, v in post.items() if 'checkboxProduct' in k]

        # init session empty if no product selected
        if not product_selected_ids:
            request.session.appointment_booking = []

        products_by_categ = []
        for categ in categories:
            domain_categ = domain + [('categ_id', '=', categ.id)]
            product_ids = request.env['product.product'].sudo().search_read(domain_categ,
                                                                            ['name', 'list_price', 'time'])
            for product in product_ids:
                product['time'] = self.covert_time_float_to_text(product['time'])

                staff_availability = self.staff_availability(product['id'], appointment_type)
                if staff_availability:
                    product['disabled'] = False
                else:
                    product['disabled'] = True

                if product['id'] in product_selected_ids:
                    product['checked'] = True
                else:
                    product['checked'] = False
            products_by_categ.append({
                'id': categ.id,
                'name': categ.name,
                'products': product_ids
            })

        values = {
            "appointment_type": appointment_type,
            "categories": self.get_categories_services(post),
            'products_by_categ': products_by_categ,
        }
        # return request.render("acs_hms_online_appointment.appointment_thank_you", {'appointment': request.env['hms.appointment'].browse(1)})

        return request.render("website_custom.appointment_booking", values)

    @http.route('/get/products/invoice/book', auth='public', methods=['POST'], type='json', website=True)
    def get_products_invoice_book(self, **kwg):
        """Get list product selected on mini invoice in booking page"""
        products = []
        total = 0
        products_ids = kwg.get('products_ids', False)
        if products_ids:
            products = request.env['product.product'].sudo().search_read([('id', 'in', products_ids)],
                                                                         ['name', 'list_price', 'time'])
            for p in products:
                p['time'] = self.covert_time_float_to_text(p['time'])
                total += p['list_price']
        return json.dumps([{'products': products, 'total': total}])

    @http.route(['/appointment/<appointment_type>/booking/staff/<int:product_id>',
                 '/appointment/<appointment_type>/booking/staff'],
                type='http', auth='public',
                website=True, sitemap=True)
    def staff_appointment(self, product_id=None, **post):

        appointment_booking = []
        if request.session.appointment_booking:
            appointment_booking = request.session.appointment_booking

        appointment_type = post.get('appointment_type', False)
        slot_date = post.get('slot_date', False)
        schedule_slot_id = post.get('schedule_slot_id', False)
        staff_id = post.get('coiffure_id', False)
        product_ids = [v for k, v in post.items() if 'checkboxProduct' in k]
        if not product_ids:
            return request.redirect('/appointment/%s/booking' % (appointment_type))
        domain = [('product_services_ids', 'in', product_ids)]
        if product_id:
            product_name = request.env['product.product'].sudo().browse(product_id).name
            domain = [('product_services_ids', 'in', product_id)]
            if schedule_slot_id and staff_id and slot_date:
                appointment_booking[len(appointment_booking) - 1]['slot_date'] = slot_date
                appointment_booking[len(appointment_booking) - 1]['schedule_slot_id'] = schedule_slot_id
            if not next((item for item in appointment_booking if item["product_id"] == product_id), False):
                appointment_booking.append({'product_id': product_id})
        request.session.appointment_booking = appointment_booking

        if appointment_type and appointment_type == 'home_booking':
            domain += [('allow_home_appointment', '=', True)]
        staff_ids = request.env['hms.coiffure'].sudo().search(domain)
        staff_ids = staff_ids.filtered(lambda s: self.check_have_slots(s.id) == True)
        # Prepare content mini invoice
        data_invoice = self.prepare_data_invoice(product_ids)

        values = {
            "appointment_type": appointment_type,
            'staffs': staff_ids,
            'invoice': data_invoice,
            'action_url': '/appointment/%s/booking/time/%s' % (appointment_type, product_id),
            'product_name': product_name or ''
        }

        return request.render("website_custom.appointment_booking_staff", values)

    @http.route(['/appointment/<appointment_type>/booking/time',
                 '/appointment/<appointment_type>/booking/time/<int:product_id>/<int:staff_id>'], type='http',
                auth='public', website=True,
                sitemap=True)
    def time_appointment(self, product_id=None, staff_id=None, **post):
        appointment_type = post.get('appointment_type', False)
        product_ids = [v for k, v in post.items() if 'checkboxProduct' in k]
        if not product_ids:
            return request.redirect('/appointment/%s/booking' % (appointment_type))

        coiffure_id = post.get('coiffure_id', False)
        appointment_booking = request.session.appointment_booking
        if coiffure_id:
            index = appointment_booking.index(
                next(filter(lambda n: n.get('product_id') == product_id, appointment_booking)))
            appointment_booking[index]['staff_id'] = coiffure_id
        request.session.appointment_booking = appointment_booking
        # Prepare content mini invoice
        data_invoice = self.prepare_data_invoice(product_ids)

        values = self.user_booking_data(post)
        slot_date = post.get('slot_date', False)
        if not slot_date:
            if 'slots_data' in values.keys():
                if len(list(values['slots_data'].values())) > 0:
                    slot_date = list(values['slots_data'].values())[0]['id']

        action_url = '/appointment/%s/booking/personaldata' % appointment_type
        index_current_product = product_ids.index(str(product_id))
        if index_current_product + 1 < len(product_ids):
            action_url = '/appointment/%s/booking/staff/%s' % (appointment_type, product_ids[index_current_product + 1])

        values.update({
            'slot_date': slot_date,
            'appointment_type': appointment_type,
            'invoice': data_invoice,
            'action_url': action_url
        })
        return request.render("website_custom.appointment_booking_time", values)

    @http.route('/appointment/<appointment_type>/booking/personaldata', type='http', auth='public',
                website=True, sitemap=True)
    def personaldata_appointment(self, **post):
        appointment_type = post.get('appointment_type', False)
        coiffure_id = post.get('coiffure_id', False)
        schedule_slot_id = post.get('schedule_slot_id', False)
        appointment_booking = request.session.appointment_booking
        if schedule_slot_id and coiffure_id:
            appointment_booking[len(appointment_booking) - 1]['schedule_slot_id'] = schedule_slot_id
            request.session.appointment_booking = appointment_booking
        coiffure = ''
        if coiffure_id:
            coiffure = request.env['hms.coiffure'].sudo().search([('id', '=', int(coiffure_id))])
        product_ids = [v for k, v in post.items() if 'checkboxProduct' in k]
        if not product_ids:
            return request.redirect('/appointment/%s/booking' % (appointment_type))
        total = 0
        products = request.env['product.product'].sudo().search_read([('id', 'in', product_ids)],
                                                                     ['name', 'list_price', 'time'])
        for p in products:
            p['time'] = self.covert_time_float_to_text(p['time'])
            total += p['list_price']
        slot_date = post.get('slot_date', False)
        if slot_date:
            slot_date = request.env['appointment.schedule.slot'].sudo().search([('id', '=', int(slot_date))])
        if schedule_slot_id:
            schedule_slot_id = request.env['appointment.schedule.slot.lines'].sudo().search(
                [('id', '=', int(schedule_slot_id))])

        # Prepare content mini invoice
        data_invoice = self.prepare_data_invoice(product_ids)

        values = {
            'appointment_type': appointment_type,
            'coiffure': coiffure,
            'slot_date': slot_date.id,
            'schedule_slot_id': schedule_slot_id.id,
            'invoice': data_invoice
        }
        return request.render("website_custom.appointment_booking_personaldata", values)

    @http.route(['/save/appointment'], type='http', auth='public', website=True, sitemap=False)
    def save_appointment(self, redirect=None, **post):
        env = request.env
        app_obj = env['hms.appointment'].sudo()
        res_patient = env['hms.patient'].sudo()
        slot_line = env['appointment.schedule.slot.lines']
        user = env.user.sudo()
        mobile = post.get('mobile', False)
        patient = res_patient.search([('mobile', '=', mobile)], limit=1)
        product_selected_ids = [int(v) for k, v in post.items() if 'checkboxProduct' in k]
        if patient:
            partner = patient.partner_id
        else:
            partner = env['res.partner'].sudo().create({
                'name': post.get('firstname', '') + ' ' + post.get('lastname', ''),
                'email': post.get('email', ''),
                'phone': post.get('phone', ''),
                'mobile': post.get('mobile', ''),
            })
            birthday = post.get('birthday', '')
            if birthday:
                birthday = datetime.strptime(birthday, "%Y/%M/%d")
            patient = res_patient.create({
                'name': post.get('firstname', '') + ' ' + post.get('lastname', ''),
                'email': post.get('email', ''),
                'mobile': post.get('mobile', ''),
                'birthday': birthday,
                'partner_id': partner.id
            })
        post = {key: value for key, value in post.items() if
                key not in ['firstname', 'lastname', 'email', 'mobile', 'birthday'] and 'checkboxProduct' not in key}
        values = {
            'error': {},
            'error_message': [],
            'partner': partner,
        }

        # error, error_message = self.validate_application_details(patient, post)
        # if error_message:
        #     values = self.user_booking_data(post)
        #     values.update({
        #         'redirect': redirect,
        #     })
        #     values.update({'error': error, 'error_message': error_message})
        #     return request.render("acs_hms_online_appointment.appointment_slot_details", values)

        if post:
            slot = slot_line.browse(int(post.get('schedule_slot_id')))
            now = datetime.now()
            # user_tz = pytz.timezone(request.context.get('tz') or env.user.tz or 'UTC')
            # app_date = user_tz.localize(slot.from_slot).astimezone(pytz.utc)
            # app_date.replace(tzinfo=None)
            app_date = slot.from_slot
            app_end_date = slot.to_slot

            if app_date < now:
                values.update({'error_message': ['Appointment date is past please enter valid.']})
                return request.render("acs_hms_online_appointment.appointment_details", values)

            diff = app_end_date - app_date
            planned_duration = (diff.days * 24) + (diff.seconds / 3600)

            post.update({
                'schedule_slot_id': slot.id,
                'booked_online': True,
                'patient_id': patient.id,
                'date': app_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                'planned_duration': planned_duration,
                'date_to': app_end_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
            })

            if slot.slot_id.coiffure_id:
                post.update({
                    'coiffure_id': slot.slot_id.coiffure_id.id,
                })

            if post.get('location'):
                post.update({
                    'outside_appointment': True,
                })
            if product_selected_ids:
                post.update({
                    'product_services_line_ids': [(0, 0, {'product_id': p.id}) for p in
                                                  request.env['product.product'].sudo().search(
                                                      [('id', 'in', product_selected_ids)])],
                })
            post.pop('name', '')
            post.pop('slot_date', '')
            post.pop('coiffure_name', '')
            post.pop('department_name', '')
            # POP Accept T&C field. if needed can be stored also.
            post.pop('acs_appointment_tc', '')

            # Create Appointment
            app_id = app_obj.sudo().create(post)

            if user.sudo().company_id.allowed_booking_payment:
                app_id.onchange_date_duration()
                app_id.sudo().with_context(default_create_stock_moves=False).create_invoice()
                # Instead of validating invoice just set appointment no to make it working on portal payment.
                # app_id.invoice_id.name = app_id.name
                invoice = app_id.invoice_id
                # return request.redirect('/my/invoices/%s#portal_pay' % (invoice.id))
                for line in app_id.product_services_line_ids:
                    if line.product_id.need_partial_payment or line.product_id.need_full_payment:
                        self.cart_update(line.product_id, 1, 0, partner)
                return request.redirect("/shop/cart")

            return request.render("acs_hms_online_appointment.appointment_thank_you", {'appointment': app_id})

        return request.redirect('/my/account')
