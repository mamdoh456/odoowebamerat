# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name": "Discount Coupons and Gift voucher for POS and Website",
    "version": "14.0.0.2",
    "category": "Point of Sale, Website",
    "depends": ['base', 'sale', 'point_of_sale', 'website', 'website_sale', 'barcodes'],
    "author": "BrowseInfo",
    "price": 89.00,
    "currency": 'EUR',
    'summary': 'Point Of Sales discount Coupons POS Gift Vouchers Discount website Discount Coupons website gift Discount pos discount website discount POS promo Discount pos offer discount point of sales Vouchers point of sales gifts discount pos Vouchers website voucher',
    "description": """
	A promotional tool called “vouchers” are essentially provided by the sellers to increase sales, to become competitive, to re-activate old customers. Those customers that have been lured away by your competitors will start buying from you again when you give them a good reason to do so.
	They feel special and privileged to get voucher codes for discounts to be applied on the cart. Voucher allows you to generate codes, which can be used to provide flat or percentage based discount on a customers order.
	Create Gift Vouchers/Coupons for discount on special occasions for grabbing more customers.
	POS discount Point of Sale Discount POS Gift Vouchers, Point of Sale Gift Voucher, Point of sale Coupons
	POS coupon code, point of sales coupon code, POS promo-code, Point of sale promocode, POS promocode, Point of sale promo-code, Point of sales Discount.Discount on POS, Disount on point of sales, Deducation on POS, POS deducation, Point of sale deduction, Gift Voucher on POS, Gift Voucher on Point of sales.
	pos gift coupons, pos gift voucher, point of sale gift coupon, point of sale gift voucher
	pos discount coupon, pos gift discount, pos discount vouhcer, pos coupon discount, pos voucher coupon 
	gift coupons, POS gift coupons Point of sales gift coupons , POS offer discount POS , points of sales gift voucher 
	pos discount vouchers , point of sales Gift Coupons
	Gift Coupons  Gift Vouchers
point of sale gift coupon, point of sale discount coupon, point of sale discount vouchers, 
point of sale coupon voucher, point of sale coupon discount
Create Gift Vouchers/Coupons for discount on special occasions for grabbing more customers.
discount vouchers , gift discount , pos promotion , pos promo coupon point of sales promo code , point of sales promo coupon 
pos promotional discount , Gift Coupons Discount in pos pos Gift Coupons Discount pos vouchers discount pos gift vouchers discount
pos discount coupon, pos gift discount, pos discount vouhcer, pos coupon discount, pos voucher coupon 
POS discount, Point of Sale Discount, POS Gift Vouchers, Point of Sale Gift Voucher, Point of sale Coupons
POS coupon code, point of sales coupon code, POS promo-code, Point of sale promocode, POS promocode, Point of sale promo-code, Point of sales Discount.Discount on POS, Disount on point of sales, Deducation on POS, POS deducation, Point of sale deduction, Gift Voucher on POS, Gift Voucher on Point of sales.

Website discount vouchers Website gift discount Website promotion  website promo coupon website promo code website promo coupon 
website promotional discount website Gift Coupons Discount in website Gift Coupons Discount website vouchers discount website gift vouchers discount
website discount coupon website gift discount website discount vouhcer website coupon discount, website voucher coupon 
website coupons discount Website Discount, website Gift Vouchers website discount Coupons
website coupon code website promo-code,website promocode,Discount on website Gift Deducation on website,Website deducation
Gift Voucher on website
   
webshop discount vouchers webshop gift discount webshop promotion webshop promo coupon webshop promo code ,webshop promo coupon 
webshop promotional discount ,webshop Gift Coupons Discount in webshop Gift Coupons Discount webshop vouchers discount webshop gift vouchers discount
webshop discount coupon webshop gift discount webshop discount vouhcer webshop coupon discount, webshop voucher coupon 
webshop coupons discount webshop Discount webshop Gift Vouchers webshop discount Coupons
webshop coupon code webshop promo-code,webshop promocode Discount on webshop Gift Deducation on webshop webshop deducation
Gift Voucher on webshop

eCommerce discount vouchers eCommerce gift discount eCommerce promotion eCommerce promo coupon eCommerce promo code eCommerce promo coupon 
eCommerce promotional discount eCommerce Gift Coupons Discount in eCommerce Gift Coupons Discount eCommerce vouchers discount eCommerce gift vouchers discount
eCommerce discount coupon eCommerce gift discount eCommerce discount vouhcer eCommerce coupon discount eCommerce voucher coupon 
eCommerce coupons discount eCommerce Discount eCommerce Gift Vouchers eCommerce discount Coupons
eCommerce coupon code eCommerce promo-code eCommerce promocode Discount on eCommerce Gift Deducation on eCommerce,eCommerce deducation
Gift Voucher on eCommerce


	odoo gift coupons POS gift coupons Point of sales gift coupons POS offer discount POS
	odoo points of sales gift voucher pos discount vouchers point of sales Gift Coupons pos Gift Coupons pos Gift Vouchers
odoo Create Gift Vouchers/Coupons for discount on special occasions for grabbing more customers.
odoo pos discount vouchers gift discount pos promotion pos promo coupon point of sales promo code
odoo point of sales promo coupon odoo pos promotional discount Gift Coupons Discount in pos pos Gift Coupons Discount pos vouchers discount pos gift vouchers discount
odoo pos discount coupon pos gift discount pos discount vouhcer pos coupon discount pos voucher coupon 
odoo POS discount Point of Sale Discount POS Gift Vouchers Point of Sale Gift Voucher Point of sale Coupons
odoo pos gift coupon pos discount coupon pos discount vouchers pos coupon voucher pos coupon discount
odoo point of sale gift coupon point of sale discount coupon point of sale discount vouchers
odoo point of sale coupon voucher point of sale coupon discount POS coupon code point of sales coupon code
odoo POS promo-code Point of sale promocode POS promocode Point of sale promo-code 
odoo Point of sales Discount odoo Discount on POS Disount on point of sales Deducation on POS 
odoo POS deducation Point of sale deduction Gift Voucher on POS Gift Voucher on Point of sales.

odoo pos coupons discoun pos voucher discount pos gift vouchers pos gift vouchers
odoo pos gift vouchers card pos giftcard pos gift card odoo giftcards in pos
odoo gift cards in point of sales odoo pos gifts cards pos gift cards pos gift promotion
odoo pos giftcards POS Gift Card point of sales gift cards point of sales giftcards
odoo giftcards in pos odoo pos offer giftcards odoo point of sales giftcards in pos odoo point of sale offer giftcards odoo

	""",
    "website": "https://www.browseinfo.in",
    "depends": ['website_all_in_one'],
    "data": [
        'views/assets.xml',
        'views/orders_view.xml',
        'views/pos_gift_coupon.xml',
    ],
    'qweb': [
        'static/src/xml/pos_coupons_gift_voucher.xml',
    ],
    "auto_install": False,
    "installable": True,
    'live_test_url': 'https://youtu.be/O8BRA3tydqc',
    "images": ['static/description/Banner.png'],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
