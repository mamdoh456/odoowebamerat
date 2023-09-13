# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
import random
from datetime import date, datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

class ProductTemp(models.Model):
	_inherit = 'product.template'

	is_coupon_product = fields.Boolean(string='Coupon Product')
	coupon_ok = fields.Boolean("Is a Gift Coupon",default=False)


class web_gift_coupon(models.Model):
	_name = 'web.gift.coupon'
	_description = 'web gift coupon'

	_sql_constraints = [
		('name', 'UNIQUE(name)', "coupon already exist please enter different name for this coupon."),
	]
	
	
	def print_report_coupons(self):
		return self.env.ref('advance_website_all_in_one.action_report_print_gift_coupon').report_action(self)

	def existing_coupon(self,code):
		coupon_record =self.search([('c_barcode', '=',code)])
		if len(coupon_record) == 1:
			coupon_record = coupon_record[0]
			return True
		else:
			return False
	def pos_screen_search_coupon(self, code):
		coupon_record = self.search([('id', '=', code)])
		if coupon_record:
			return [coupon_record.id,coupon_record.name,coupon_record.expiry_date,
					coupon_record.amount,coupon_record.issue_date,coupon_record.c_barcode,
					coupon_record.amount_type,coupon_record.c_barcode_img
					]
	def search_coupon(self, code):
		coupon_record = self.search([('c_barcode', '=', code)])
		if coupon_record and coupon_record.product_id:
			return [coupon_record.id, coupon_record.amount,coupon_record.used,
					coupon_record.coupon_count, coupon_record.coupon_apply_times,
					coupon_record.expiry_date, coupon_record.partner_true,
					coupon_record.partner_id.id,coupon_record.amount_type,
					coupon_record.exp_dat_show,coupon_record.max_amount,
					coupon_record.apply_coupon_on,coupon_record.product_id.id,
					coupon_record.is_categ,coupon_record.categ_ids.ids,
					coupon_record.product_ids.ids,
					]
		else:
			return []

	@api.constrains('amount', 'exp_dat_show', 'issue_date', 'expiry_date', 'max_amount')
	def _check_config(self):

		if self.amount_type == 'fix':
			if self.max_amount and self.amount:
				if self.amount > self.max_amount:
					raise Warning(_("Coupon amount is greater than maximum amount"))

		if self.expiry_date and self.issue_date:
			if self.expiry_date < self.issue_date:
				raise Warning(_("Please Enter Valid Date.Expiry Date Should not be greater than Issue Date."))

	@api.model
	def search_user(self):
		res_partner = self.env['res.partner'].search([])
		user_list = []
		for i in res_partner:
			user_list.append(i.name)
		return user_list

	@api.model
	def create_coupon_from_ui(self, data):

		coup_obj = self.env['web.gift.coupon']
		amt_type = False

		if data['c_am_type'] == 'Fixed':
			amt_type = 'fix'
		else:
			amt_type = 'per'

		if data['c_expdt_box']:
			exp_check_box = True
			expiry_checked = data['c_exp_dt']
		else:
			exp_check_box = False
			expiry_checked = False

		if data['c_cust_box']:
			cust_check_box = True
			customer_select = self.partner_id.search([('name', '=', data['c_customer'])]).id
		else:
			cust_check_box = False
			customer_select = False

		categ = []
		if data.get('coupon_categ'):
			for c in data.get('coupon_categ'):
				categ.append(int(c))

		multi_ecom_categ = []
		if data.get('coupon_multi_ecom_categ'):
			for c in data.get('coupon_multi_ecom_categ'):
				multi_ecom_categ.append(int(c))

		products = []
		if data.get('coupon_multi_products'):
			for c in data.get('coupon_multi_products'):
				products.append(int(c))

		vals = {
			'name': data['c_name'],
			'product_id': int(data['c_product']),
			'coupon_apply_times': data['c_limit'],
			'issue_date': data['c_issue_dt'],
			'amount': data['c_amount'],
			'amount_type': amt_type,
			'expiry_date': expiry_checked,
			'partner_id': customer_select,
			'exp_dat_show': exp_check_box,
			'partner_true': cust_check_box,
			'max_amount': data['coupon_max_amount'],
			'active': True,
			'user_id': self.env.user.id,
		}

		if categ and multi_ecom_categ:
			vals.update({
				'is_categ': True,
				'categ_ids': [(6, 0, categ)],
				'ecommerce_category_ids': [(6, 0, multi_ecom_categ)],
			})

		if products:
			vals.update({
				'products_true': True,
				'product_ids': [(6, 0, products)]
			})

		res = coup_obj.sudo().create(vals)
		return [res.id, res.name, res.expiry_date, res.amount, res.issue_date,
				res.c_barcode, res.amount_type, res.c_barcode_img]
	@api.model
	def create(self, vals):
		rec = super(web_gift_coupon,self).create(vals)
		code =(random.randrange(1111111111111,9999999999999))
		rec.write({'c_barcode':str(code)})
		return rec


	name  = fields.Char('Name')
	product_id  = fields.Many2one('product.product','Product', domain = [('type', '=', 'service'),('is_coupon_product', '=', True)])
	c_barcode = fields.Char(string="Coupon Barcode")
	c_barcode_img = fields.Binary('Coupon Barcode Image')
	user_id  =  fields.Many2one('res.users' ,'Created By',default  = lambda self: self.env.user)
	issue_date  =  fields.Datetime(default = datetime.now())
	exp_dat_show = fields.Boolean('Is Expiry Date')
	expiry_date  = fields.Datetime("Expiry Date")
	max_amount = fields.Float("Maximum amount")
	partner_true = fields.Boolean('Allow for Specific Customer')
	partner_id  =  fields.Many2one('res.partner')
	sale_order_ids = fields.One2many('sale.order','sale_coupon_id')
	active = fields.Boolean('Active',default=True)
	amount  =  fields.Float('Coupon Amount')
	amount_type = fields.Selection([('fix','Fixed'),('per','%')],default='fix')
	description  =  fields.Text('Note')
	used = fields.Boolean('Used')   
	coupon_apply_times = fields.Integer('Coupon Code Apply Limit', default=1)
	coupon_count = fields.Integer('Coupon used count', default=0)
	coupon_desc = fields.Text('Discription')
	apply_coupon_on = fields.Selection([('taxed', 'Taxed Amount'),
										('untaxed', 'Untaxed Amount')], default='taxed', string="Apply Coupon on")

	is_categ = fields.Boolean('Allow for Specific Category')
	categ_ids = fields.Many2many('pos.category', string='POS Categories')
	ecommerce_category_ids = fields.Many2many('product.public.category', string='Ecommerce Categories')

	products_true = fields.Boolean(string='Allow for Specific Products')
	product_ids = fields.Many2many('product.product', string='Products')
	voucher_sent = fields.Boolean(string='Sent', readonly=True, default=False)
	product_ids = fields.Many2many('product.template',string='Products')
	product_categ_ids = fields.Many2many('product.category',string="Product Category")
	
	
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: