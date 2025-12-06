from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class DigitalQueueController(http.Controller):

    @http.route('/digitalqueue/services', type='http', auth='public', website=True)
    def list_services(self, **kw):
        services = request.env['digitalqueue.queue_service'].sudo().search([('active', '=', True)])

        html = """<html><head><meta charset="utf-8"/><title>File d'Attente</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet"/>
        <style>body { background: linear-gradient(135deg,#667eea,#764ba2); min-height: 100vh; }</style>
        </head><body><div class="container mt-5">
        <h1 class="text-center text-white mb-4">File d'Attente Digitale</h1><div class="row">"""

        for s in services:
            html += f"""
            <div class="col-md-4 mb-4">
                <div class="card shadow">
                    <div class="card-body text-center">
                        <h4>{s.name}</h4>
                        <p class="text-muted">{s.description or 'Service disponible'}</p>
                        <a href="/digitalqueue/take_ticket?service_id={s.id}" class="btn btn-primary">Prendre un ticket</a>
                    </div>
                </div>
            </div>"""

        html += "</div></div></body></html>"
        return html

    @http.route('/digitalqueue/take_ticket', type='http', auth='public', website=True)
    def take_ticket(self, service_id=None, **kw):
        service_id = int(service_id)

        waiting_count = request.env['digitalqueue.ticket'].sudo().search_count([
            ('service_id', '=', service_id),
            ('statut', '=', 'en_attente')
        ])

        priority = waiting_count + 1

        ticket = request.env['digitalqueue.ticket'].sudo().create({
            'service_id': service_id,
            'priorite': priority,
            'statut': 'en_attente'
        })

        ticket.sudo().write({
            'numero': f"T{priority}",
            'name': f"T{priority}"
        })

        return request.redirect(f"/digitalqueue/ticket_confirmation?ticket_id={ticket.id}")

    @http.route('/digitalqueue/ticket_confirmation', type='http', auth='public', website=True)
    def ticket_confirmation(self, ticket_id=None, **kw):
        ticket = request.env['digitalqueue.ticket'].sudo().browse(int(ticket_id))

        waiting_before = request.env['digitalqueue.ticket'].sudo().search([
            ('service_id', '=', ticket.service_id.id),
            ('statut', '=', 'en_attente'),
            ('create_date', '<', ticket.create_date)
        ])

        position = len(waiting_before) + 1

        people_text = (
            f"{len(waiting_before)} personne(s) avant vous"
            if len(waiting_before) > 0
            else "Vous êtes le premier !"
        )

        html = f"""<html><head><meta charset="utf-8"/><title>Ticket Créé</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet"/>
        <style>body {{ background: linear-gradient(135deg,#74b9ff,#0984e3); min-height: 100vh; }}</style></head>
        <body><div class="container py-5"><div class="card shadow">
        <div class="card-header bg-success text-white text-center py-4"><h1>Ticket Créé !</h1></div>
        <div class="card-body text-center p-4">
            <h2 class="text-muted mb-3">Votre numéro</h2>
            <div style="font-size:4rem;font-weight:bold;">{ticket.numero}</div>
            <p class="text-muted">{ticket.service_id.name}</p>
            <div class="alert alert-info">
               <h5>Position dans la file: {position}</h5><p>{people_text}</p>
            </div>
            <a href="/digitalqueue/services" class="btn btn-primary">Prendre un autre ticket</a>
        </div></div></div></body></html>"""

        return html

