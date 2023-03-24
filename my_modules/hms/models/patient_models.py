from odoo import models,fields
from odoo.models import ValidationError
from datetime import datetime
from odoo import api, models


class Patient(models.Model):
    _name = "hms.patient"

    firstname = fields.Char(required=True)
    lastname = fields.Char(required=True)
    email = fields.Char(unique=True,string='Email')
    birthdate = fields.Date()
    history = fields.Html()
    cr_ratio = fields.Float()
    bloodtype = fields.Selection([('A+','A+'),('B+','B+'),('O-','O-')],default='O-')
    pcr = fields.Boolean()
    image = fields.Image()
    address = fields.Text()
    age = fields.Integer()
    department = fields.Many2one("hms.department", string="Department")
    doctor = fields.Many2many("hms.doctor", string="Doctor")
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')], string='Patient State', default='fair')
    log_id = fields.One2many("hms.log", "patient_id", string="log")


    _sql_constraints = [
        ('email_uniq', 'UNIQUE(email)', 'The email must be unique!')
    ]
###################  Computing Age ### #################


    @api.depends('birthdate')
    def get_age(self):
        for rec in self:
            if rec.birhtdate:
                rec.age=datetime.now().year-rec.birhtdate.year

###################  change state  ###################
    def write(self, vals):
        if 'state' in vals:
            description = vals['state']
            logValues={
                'description':description,
                'patient_id':self.id
            }
            self.env['hms.log'].create(logValues)
        return super(Patient, self).write(vals)

###################  warning message if age < 30 #################

    @api.onchange('birthdate')
    def check_pcr_field(self):
        if self.age < 30:
            if not self.pcr:
                self.pcr= True
                return {
                    'warning': {
                        'title': 'PCR Field Checked',
                        'message': 'PCR field has been automatically checked.'
                    }
                }
        else:
            return True
        

###################  email validation  #################


    @api.constrains('email')
    def check_email(self):
        for record in self:
            if '@' not in record.email:
                raise ValidationError("please enter a valid email")




