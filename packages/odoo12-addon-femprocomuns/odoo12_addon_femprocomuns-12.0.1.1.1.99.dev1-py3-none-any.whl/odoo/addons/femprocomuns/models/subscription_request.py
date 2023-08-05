from odoo import fields, models, api

class SubscriptionRequest(models.Model):

    _inherit = ["subscription.request"]
    
    ref = fields.Char(string='Internal Reference', index=True)
    
    def get_partner_vals(self):
        partner_vals = super().get_partner_vals()
        partner_vals['ref'] = self.ref
        return partner_vals

    @api.multi
    def validate_subscription_request(self):
        invoice = super().validate_subscription_request()
        if self.ref:
            self.partner_id.ref = self.ref
        return invoice
