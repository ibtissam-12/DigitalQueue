from odoo import models, fields, api

class Ticket(models.Model):
    _name = "digitalqueue.ticket"
    _description = "Ticket"

    numero = fields.Char(string="Numéro")
    date_creation = fields.Datetime(default=lambda self: fields.Datetime.now())
    priorite = fields.Integer(default=1)
    statut = fields.Selection([
        ('en_attente', 'En attente'),
        ('appele', 'Appelé'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('rate', 'Raté'),
    ], default="en_attente")
    file_id = fields.Many2one("digitalqueue.file_attente", string="File")
    agent_id = fields.Many2one("digitalqueue.agent", string="Agent assigné", help="Agent currently serving this ticket")
    service_id = fields.Many2one('digitalqueue.queue_service', string='Service')
    name = fields.Char(string='Name', compute='_compute_name', store=True)

    @api.model
    def create(self, vals):
        # Ensure file_attente exists for the selected service
        service_id = vals.get('service_id')
        file_obj = self.env['digitalqueue.file_attente']
        file_id = vals.get('file_id')
        file_attente = None
        if not file_id and service_id:
            # Try to find an existing queue for this service
            file_attente = file_obj.search([('nom', '=', f'Service {service_id}')], limit=1)
            if not file_attente:
                # Create queue for this service
                file_attente = file_obj.create({'nom': f'Service {service_id}'})
            vals['file_id'] = file_attente.id
        elif file_id:
            file_attente = file_obj.browse(file_id)
        # Create the ticket
        ticket = super(Ticket, self).create(vals)
        # Set ticket number as position in queue
        if ticket.file_id:
            position = self.search_count([('file_id', '=', ticket.file_id.id)])
            ticket.numero = str(position)
            ticket.name = ticket.numero
        return ticket

    @api.depends('numero')
    def _compute_name(self):
        for rec in self:
            rec.name = rec.numero

    def next_client(self):
        """
        Passe le ticket actuel comme terminé,
        puis met le ticket suivant en 'appele'.
        Ferme la fenêtre actuelle et ouvre le suivant en popup.
        """
        for ticket in self:
            # Clear agent reference when ticket is finished
            ticket.agent_id = False
            ticket.statut = 'termine'

            # Trouver le prochain ticket en attente dans la même file
            # Consistent with traiterClient: priorite ASC (lowest=highest), then oldest
            next_ticket = self.search([
                ('file_id', '=', ticket.file_id.id),
                ('statut', '=', 'en_attente')
            ], order='priorite asc, date_creation asc', limit=1)

            if next_ticket:
                next_ticket.statut = 'appele'
                # Open the next ticket and close current window
                view_id = False
                try:
                    view_id = self.env.ref('DigitalQueue.view_ticket_form').id
                except Exception:
                    view_id = False

                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Ticket',
                    'res_model': 'digitalqueue.ticket',
                    'view_mode': 'form',
                    'res_id': next_ticket.id,
                    'views': [(view_id, 'form')] if view_id else False,
                    'target': 'new',
                    'close': True,
                }

        # If no next ticket was found, show a warning to the user
        return {
            'warning': {
                'title': 'Aucun client suivant',
                'message': "Il n'y a pas d'autre client en attente dans la file."
            }
        }
