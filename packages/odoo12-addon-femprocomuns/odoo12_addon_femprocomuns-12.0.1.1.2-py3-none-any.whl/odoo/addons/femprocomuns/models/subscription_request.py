from odoo import fields, models, api

class SubscriptionRequest(models.Model):

    _inherit = ["subscription.request"]
    
    ref = fields.Char(string='Internal Reference', index=True)
    
    def get_partner_vals(self):
        partner_vals = super().get_partner_vals()
        partner_vals['ref'] = self.ref
        return partner_vals

    def get_invoice_vals(self, partner):
        vals = super().get_invoice_vals(partner)
        usense = self.env['operating.unit'].search([('code','=','USense')])
        vals['operating_unit_id'] = usense.id
        return vals

    @api.multi
    def validate_subscription_request(self):
        invoice = super().validate_subscription_request()
        if self.ref:
            self.partner_id.ref = self.ref
        return invoice
