from odoo import models,fields,api
from odoo.exceptions import ValidationError

class CrmPatient(models.Model):
    _inherit="res.partner"
    related_patient_id=fields.Many2one('hms.patient',string="Related Patient")
    vat = fields.Char(required=True)
    website = fields.Char(required=True)


    @api.constrains('email')
    def validate_email(self):
        for record in self:
            if record.email:
                if self.env['hms.patient'].search([('email','=',record.email)]):
                    raise ValidationError(('this email is already registerd'))
                
    def unlink(self):
        for record in self:
            if record.related_patient_id:
                raise ValidationError(('This record cannt be unlinked'))
        return  super(CrmPatient, self).unlink()
    


    