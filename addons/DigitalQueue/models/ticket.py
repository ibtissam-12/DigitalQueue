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
    agent_id = fields.Many2one(
        "digitalqueue.agent",
        string="Agent assigné",
        help="Agent currently serving this ticket"
    )
    service_id = fields.Many2one('digitalqueue.queue_service', string='Service')

    name = fields.Char(string='Name', compute='_compute_name', store=True)

    # ----------------------------------------------------------
    # CREATE : calcul du numero avant creation
    # ----------------------------------------------------------
    @api.model
    def create(self, vals):
        service_id = vals.get('service_id')

        file_obj = self.env['digitalqueue.file_attente']
        file_id = vals.get('file_id')
        file_attente = None

        # nouvelle file si pas donnée
        if not file_id and service_id:
            file_attente = file_obj.search([('nom', '=', f"Service {service_id}")], limit=1)
            if not file_attente:
                file_attente = file_obj.create({'nom': f"Service {service_id}"})
            vals['file_id'] = file_attente.id
        else:
            file_attente = file_obj.browse(file_id)

        # Calcul position avant création
        if file_attente:
            position = self.search_count([
                ('file_id', '=', file_attente.id),
                ('statut', '=', 'en_attente')
            ]) + 1

            vals['numero'] = str(position)

        ticket = super(Ticket, self).create(vals)

        # recalcul des positions globales
        if ticket.file_id:
            self._recompute_positions(ticket.file_id.id)

        return ticket

    # ----------------------------------------------------------
    # name = numero
    # ----------------------------------------------------------
    @api.depends('numero')
    def _compute_name(self):
        for rec in self:
            rec.name = rec.numero

    # ----------------------------------------------------------
    # NEXT CLIENT
    # ----------------------------------------------------------
    def next_client(self):
        for ticket in self:
            ticket.agent_id = False
            ticket.statut = 'termine'

            next_ticket = self.search([
                ('file_id', '=', ticket.file_id.id),
                ('statut', '=', 'en_attente')
            ], order='priorite asc, date_creation asc', limit=1)

            if next_ticket:
                next_ticket.statut = 'appele'
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
                }

        return {
            'warning': {
                'title': 'Aucun client suivant',
                'message': "Il n'y a pas d'autre client en attente."
            }
        }

    # -----------------------------------------------------------
    # Recompute des positions
    # -----------------------------------------------------------
    def _recompute_positions(self, file_id):
        if not file_id:
            return

        tickets = self.search([
            ('file_id', '=', file_id),
            ('statut', '=', 'en_attente')
        ], order='priorite asc, date_creation asc')

        for idx, t in enumerate(tickets):
            t.numero = str(idx + 1)
            t.name = t.numero

