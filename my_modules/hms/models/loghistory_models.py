from odoo import models,fields

class LogHistory(models.Model):
    _name = "hms.log"

    description = fields.Char(required=True)
    patient_id = fields.Many2one("hms.patient")
