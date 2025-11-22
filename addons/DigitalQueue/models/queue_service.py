from odoo import models, fields

class QueueService(models.Model):
    _name = 'queue.service'
    _description = 'Service de file'

    name = fields.Char(string='Nom du Service', required=True)
    code = fields.Char(string='Code', required=True)
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Actif', default=True)
