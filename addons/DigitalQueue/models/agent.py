from odoo import models, fields, api

class Agent(models.Model):
    _name = "digitalqueue.agent"
    _description = "Agent de guichet"

    nom = fields.Char(required=True)
    service_id = fields.Many2one("digitalqueue.queue_service", string="Service", required=True)
    est_disponible = fields.Boolean(default=False)

    file_id = fields.Many2one("digitalqueue.file_attente", string="File assignée")
    ticket_courant_id = fields.Many2one("digitalqueue.ticket", string="Ticket en cours")

    def connecter(self):
        self.est_disponible = True

    def consulterFile(self):
        if not self.file_id:
            return False
        return {
            'name': "Tickets de la file",
            'type': 'ir.actions.act_window',
            'res_model': 'digitalqueue.ticket',
            'view_mode': 'tree,form',
            'domain': [('file_id', '=', self.file_id.id)],
        }

    def traiterClient(self):
        self.ensure_one()
        ticket = self.env['digitalqueue.ticket'].search([
            ('file_id', '=', self.file_id.id),
            ('statut', '=', 'en_attente')
        ], order="priorite asc, date_creation asc", limit=1)
        if ticket:
            ticket.statut = "appele"
            self.ticket_courant_id = ticket
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': f"Client {ticket.numero} appelé !",
                    'type': 'rainbow_man',
                }
            }
        else:
            return {
                'warning': {
                    'title': "Aucun client",
                    'message': "Il n’y a aucun client en attente.",
                }
            }

    def passerSuivant(self):
        if self.ticket_courant_id:
            self.ticket_courant_id.statut = "rate"
            self.ticket_courant_id = False
        return self.traiterClient()

    def terminerClient(self):
        if self.ticket_courant_id:
            self.ticket_courant_id.statut = "termine"
            self.ticket_courant_id = False
