// Define a new Odoo POS module for extending the ProductScreen
odoo.define('pos_unpaid_invoice.ProductScreen', function (require) {
    'use strict';

    // Import required modules
    const ProductScreen = require('point_of_sale.ProductScreen')
    const Registries = require('point_of_sale.Registries')
    const models = require('point_of_sale.models')
    const rpc = require('web.rpc');

    // Define a new class UnpaidInvoiceProductScreen which extends ProductScreen
    const UnpaidInvoiceProductScreen = (ProductScreen) =>
        class extends ProductScreen {

            // Add the clearCart method to remove all order lines from the current order when select or deselect customer
            async clearCart() {
                let selectedOrder = this.env.pos.get_order();
                if (selectedOrder.orderlines.models.length > 0) {
                    selectedOrder.orderlines.models.forEach(l => selectedOrder.remove_orderline(l))
                }
            }
            // Override the _onClickCustomer method to retrieve the customer's unpaid invoices and add them as a new order line
            async _onClickCustomer() {
                var self = this;
                // Call the parent _onClickCustomer method using super and wait for it to finish before executing the rest of the code
                return super._onClickCustomer().then(() => {
                    // Call the clearCart method to remove any existing order lines from the current order
                    var client = self.currentOrder.get_client()
                    self.clearCart()
                    // Check if there is a current order and a selected customer
                    if (self.currentOrder && self.currentOrder.get_client()){
                        var unpaid_invoice_amount = 0;

                        // Retrieve the customer's unpaid invoices using a search query with the rpc module
                        rpc.query({
                            model: 'account.move',
                            method: 'search_read',
                            domain: [['partner_id', '=', client.id], ['amount_residual', '>', 0], ['state', '=', 'posted']],
                            fields: ['id', 'partner_id', 'amount_residual'],
                        }).then(function(result) {
                            if (result.length > 0) {
                                // Get the unpaid invoice total amount
                                for (var i = 0; i < result.length; i++) {
                                    unpaid_invoice_amount += result[i].amount_residual;
                                }
                                if (unpaid_invoice_amount > 0) {
                                    // Get the unpaid invoice product using its ID from the Odoo POS configuration
                                    let unpaid_invoice_product = self.env.pos.db.get_product_by_id(self.env.pos.config.unpaid_invoice_product_id[0])
                                    if (!unpaid_invoice_product) {
                                        console.error('Unpaid Invoice Product not found!');
                                        return;
                                    }
                                    // Create a new order line for the unpaid invoice product and add it to the current order
                                    let new_line = new models.Orderline({}, {
                                        pos: self.env.pos,
                                        order: self.env.pos.get_order(),
                                        product: unpaid_invoice_product,
                                        price: unpaid_invoice_amount,
                                        price_manually_set: true,
                                    });
                                    self.env.pos.get_order().add_orderline(new_line);
                                }
                            }
                        });
                    }
                });
            }
        }
    // Register the UnpaidInvoiceProductScreen class as a component with the Registries module
    Registries.Component.extend(ProductScreen, UnpaidInvoiceProductScreen);
    // Export the UnpaidInvoiceProductScreen class for use in other modules
    return UnpaidInvoiceProductScreen;
});