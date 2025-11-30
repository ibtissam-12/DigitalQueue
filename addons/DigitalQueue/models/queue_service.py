from odoo import models, fields, api

class QueueService(models.Model):
    _name = 'queue.service'
    _description = 'Service de file'

    name = fields.Char(string='Nom du Service', required=True)
    code = fields.Char(string='Code', required=True)
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Actif', default=True)
    current_number = fields.Integer(string='Dernier numéro', default=0)

class QueueTicket(models.Model):
    _name = 'queue.ticket'
    _description = 'Ticket de file d\'attente'
    _order = 'create_date asc'
    
    name = fields.Char(string='Numéro du ticket', required=True, readonly=True)
    service_id = fields.Many2one('queue.service', string='Service', required=True)
    status = fields.Selection([
        ('waiting', 'En attente'),
        ('in_progress', 'En cours'),
        ('completed', 'Terminé'),
    ], string='Statut', default='waiting')
    create_date = fields.Datetime(string='Date de création', default=fields.Datetime.now)
    
    @api.model
    def create(self, vals):
        if 'service_id' in vals:
            service = self.env['queue.service'].browse(vals['service_id'])
            service.current_number += 1
            service_code = service.name[:3].upper()
            vals['name'] = f"{service_code}{service.current_number:03d}"
        return super().create(vals)
    
    def get_position_in_queue(self):
        """Retourne la position dans la file d'attente"""
        for ticket in self:
            waiting_tickets_before = self.search([
                ('service_id', '=', ticket.service_id.id),
                ('status', '=', 'waiting'),
                ('create_date', '<', ticket.create_date)
            ])
            ticket.position_in_queue = len(waiting_tickets_before) + 1
        return True
    
    position_in_queue = fields.Integer(
        string='Position dans la file',
        compute='get_position_in_queue',
        store=False
    )