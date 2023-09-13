odoo.define('bi_pos_website_gift_coupon.pos_coupons_gift_voucher', function(require) {
	"use strict";

	var models = require('point_of_sale.models');

	models.load_fields('product.product', ['type','is_coupon_product']);

	models.load_models({
		model:  'product.public.category',
		fields: ['id', 'display_name', 'parent_id', 'child_id'],
		domain: null,
		loaded: function(self, ecom_categories){
			self.ecom_categories = ecom_categories;
		},
	});

	var OrderSuper = models.Order;
	models.Order = models.Order.extend({
		init: function(parent,options){
			this._super(parent,options);
			this.is_coupon_used = this.is_coupon_used || false;
			this.coupon_id = this.coupon_id || false;
			this.coup_maxamount = this.coup_maxamount || 0;
		},

		set_is_coupon_used: function(is_coupon_used){
			this.is_coupon_used = is_coupon_used;
			this.trigger('change',this);
		},

		get_is_coupon_used: function(is_coupon_used){
			return this.is_coupon_used;
		},
		
		export_as_JSON: function() {
			var self = this;
			var loaded = OrderSuper.prototype.export_as_JSON.call(this);
			loaded.is_coupon_used = self.is_coupon_used || false;
			loaded.coupon_id = this.coupon_id;
			loaded.coup_maxamount = this.coup_maxamount;
			return loaded;
		},

		init_from_JSON: function(json){
			OrderSuper.prototype.init_from_JSON.apply(this,arguments);
			this.is_coupon_used = json.is_coupon_used || false;
			this.coupon_id = json.coupon_id;
			this.coup_maxamount = json.coup_maxamount;
		},

		remove_orderline: function( line ){
			var prod = line.product;
			if(prod.is_coupon_product){
				this.set_is_coupon_used(false);
			}
			this.assert_editable();
			this.orderlines.remove(line);
			this.coupon_id = false;	
			this.select_orderline(this.get_last_orderline());
		},

	});
});
