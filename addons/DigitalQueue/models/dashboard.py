from odoo import models, fields, api


class Dashboard(models.TransientModel):
    _name = 'digitalqueue.dashboard'
    _description = 'Digital Queue Dashboard'

    total_tickets = fields.Integer(string='Total tickets', compute='_compute_counts')
    en_attente = fields.Integer(string='En attente', compute='_compute_counts')
    appele = fields.Integer(string='Appelés', compute='_compute_counts')
    en_cours = fields.Integer(string='En cours', compute='_compute_counts')
    termine = fields.Integer(string='Terminés', compute='_compute_counts')

    def _compute_counts(self):
        Ticket = self.env['digitalqueue.ticket']
        totals = {
            'total': Ticket.search_count([]),
            'en_attente': Ticket.search_count([('statut', '=', 'en_attente')]),
            'appele': Ticket.search_count([('statut', '=', 'appele')]),
            'en_cours': Ticket.search_count([('statut', '=', 'en_cours')]),
            'termine': Ticket.search_count([('statut', '=', 'termine')]),
        }
        for rec in self:
            rec.total_tickets = totals['total']
            rec.en_attente = totals['en_attente']
            rec.appele = totals['appele']
            rec.en_cours = totals['en_cours']
            rec.termine = totals['termine']

    @api.model
    def default_get(self, fields_list):
        res = super(Dashboard, self).default_get(fields_list)
        Ticket = self.env['digitalqueue.ticket']
        res_counts = {
            'total_tickets': Ticket.search_count([]),
            'en_attente': Ticket.search_count([('statut', '=', 'en_attente')]),
            'appele': Ticket.search_count([('statut', '=', 'appele')]),
            'en_cours': Ticket.search_count([('statut', '=', 'en_cours')]),
            'termine': Ticket.search_count([('statut', '=', 'termine')]),
        }
        for k, v in res_counts.items():
            if k in fields_list or not fields_list:
                res[k] = v
        return res
