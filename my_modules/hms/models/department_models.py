from odoo import models,fields

class Department(models.Model):
    _name = "hms.department"

    name = fields.Char(required=True)
    capacity = fields.Integer()
    is_open = fields.Boolean(default=True)
    patients = fields.One2many("hms.patient", "department", string="Patients")

