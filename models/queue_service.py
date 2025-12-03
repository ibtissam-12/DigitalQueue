from odoo import models, fields, api

class QueueService(models.Model):
    _name = 'digitalqueue.queue_service'
    _description = 'Service de file'

    name = fields.Char(string='Nom du Service', required=True)
    code = fields.Char(string='Code', required=True)
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Actif', default=True)
    agents_ids = fields.One2many("digitalqueue.agent", "service_id", string="Agents assignés")