from odoo import models, fields, api


class TicketStat(models.Model):
    _name = 'digitalqueue.ticket.stat'
    _description = 'Tickets statistics per day and agent'
    _auto = False

    id = fields.Integer(string='ID', readonly=True)
    day = fields.Date(string='Date', readonly=True)
    agent_id = fields.Many2one('digitalqueue.agent', string='Agent', readonly=True)
    ticket_count = fields.Integer(string='Ticket Count', readonly=True)

    def init(self):
        cr = self.env.cr
        cr.execute("""
            CREATE OR REPLACE VIEW digitalqueue_ticket_stat AS (
                SELECT
                    MIN(t.id) as id,
                    date(t.date_creation) as day,
                    t.agent_id,
                    COUNT(*) AS ticket_count
                FROM digitalqueue_ticket t
                GROUP BY date(t.date_creation), t.agent_id
            )
        """)
