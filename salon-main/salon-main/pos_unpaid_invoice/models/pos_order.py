from odoo import api, fields, models,_
from odoo.exceptions import UserError


class PosOrder(models.Model):
    _inherit = 'pos.order'

    def _get_unpaid_invoice_line(self, order):
        # Get the line containing the unpaid invoice product from the given order
        return next((line for line in order['data']['lines'] if
                     line[2]['product_id'] == self.env.ref("pos_unpaid_invoice.product_product_unpaid_invoice").id),
                    None)

    def _get_payment_amount(self, invoice, unpaid_invoice_line):
        # Get the payment amount to be made for the given invoice and unpaid invoice line
        return min(invoice.amount_residual, unpaid_invoice_line[2]['price_unit'])

    def _create_payment(self, partner_id, payment_amount, order):
        # Create a payment for the given partner and payment amount
        payment = self.env['account.payment'].create({
            'payment_type': 'inbound',
            'partner_type': 'customer',
            'partner_id': partner_id,
            'journal_id': self.env['account.journal'].search([('name','=','Cash')]).id,  # TO DO LATER
            'amount': payment_amount,
            'date': fields.Date.today(),
            'ref': _('Payment of POS Order %s') % order['data']['name'],
        })
        payment.action_post()
        return payment

    def _reconcile_payment_with_invoice(self, payment, invoice):
        # Reconcile the given payment with the given invoice
        to_reconcile = []
        to_reconcile.append(invoice.line_ids)
        domain = [('account_internal_type', 'in', ('receivable', 'payable')), ('reconciled', '=', False)]
        for payment_object, lines in zip(payment, to_reconcile):
            payment_lines = payment_object.line_ids.filtered_domain(domain)
            for account in payment_lines.account_id:
                (payment_lines + lines) \
                    .filtered_domain([('account_id', '=', account.id), ('reconciled', '=', False)]) \
                    .reconcile()
    @api.model
    def _process_order(self, order, draft, existing_order):
        # Call the parent method to process the order
        res = super(PosOrder, self)._process_order(order, draft, existing_order)

        # Check if the order contains the unpaid invoice product
        unpaid_invoice_line = self._get_unpaid_invoice_line(order)
        if unpaid_invoice_line:
            # Create a payment for the unpaid invoice(s)
            partner = order['data']['partner_id']
            # Search for all unpaid invoices for this partner
            invoices = self.env['account.move'].search(
                [('partner_id', '=', partner), ('state', '=', 'posted'), ('move_type', '=', 'out_invoice'),
                 ('amount_residual', '>', 0)], order='invoice_date desc')
            for invoice in invoices:
                # Determine the payment amount (minimum of the unpaid invoice amount and the amount of the unpaid invoice product line)
                payment_amount = self._get_payment_amount(invoice,unpaid_invoice_line)
                # Create a payment
                payment = self._create_payment(partner,payment_amount,order)
                # Reconcile the payment with the invoice(s)
                self._reconcile_payment_with_invoice(payment,invoice)
                # Reduce the payment amount from the price of the unpaid invoice product line
                unpaid_invoice_line[2]['price_unit'] -= payment_amount
                if unpaid_invoice_line[2]['price_unit'] <= 0:
                    break
        return res



