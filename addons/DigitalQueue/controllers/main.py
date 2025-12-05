from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class DigitalQueueController(http.Controller):

    @http.route('/digitalqueue/services', type='http', auth='public', website=True)
    def list_services(self, **kw):
        _logger.info("=== 🚀 ROUTE /digitalqueue/services APPELEE ===")
        
        services = request.env['digitalqueue.queue_service'].sudo().search([('active', '=', True)])
        _logger.info(f"=== 📊 SERVICES TROUVÉS: {len(services)} ===")
        
        html = """<html><head><meta charset="utf-8"/><title>File d'Attente</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet"/>
        <style>body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }</style>
        </head><body><div class="container mt-5"><h1 class="text-center text-white mb-4">File d'Attente Digitale</h1>
        <div class="row">"""
        
        for service in services:
            html += f"""<div class="col-md-4 mb-4"><div class="card shadow"><div class="card-body text-center">
            <h4>{service.name}</h4><p class="text-muted">{service.description or 'Service disponible'}</p>
            <a href="/digitalqueue/take_ticket?service_id={service.id}" class="btn btn-primary">Prendre un ticket</a>
            </div></div></div>"""
        
        if not services:
            html += '<div class="alert alert-info text-center mt-5"><h4>Aucun service disponible</h4></div>'
        
        html += """</div></div><script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
        </body></html>"""
        
        return html

    @http.route('/digitalqueue/take_ticket', type='http', auth='public', website=True)
    def take_ticket(self, service_id=None, **kw):
        _logger.info(f"=== 🎫 CRÉATION TICKET pour service_id: {service_id} ===")
        service_id_int = int(service_id) if service_id else False
        
        # Count how many tickets are waiting for this service to set priority
        waiting_tickets_count = request.env['digitalqueue.ticket'].sudo().search_count([
            ('service_id', '=', service_id_int),
            ('statut', '=', 'en_attente')
        ])
        
        # Priority is based on position in queue (lower number = higher priority = called first)
        # Position 1 gets priority 1, position 2 gets priority 2, etc.
        priority = waiting_tickets_count + 1
        
        ticket = request.env['digitalqueue.ticket'].sudo().create({
            'service_id': service_id_int,
            'priorite': priority,
            'statut': 'en_attente'
        })
        try:
            ticket.sudo().write({'numero': f"T{ticket.id}"})
        except Exception:
            _logger.exception('Erreur lors de l\'écriture du numéro de ticket')
        return request.redirect(f'/digitalqueue/ticket_confirmation?ticket_id={ticket.id}')

    @http.route('/digitalqueue/ticket_confirmation', type='http', auth='public', website=True)
    def ticket_confirmation(self, ticket_id=None, **kw):
        ticket = request.env['digitalqueue.ticket'].sudo().browse(int(ticket_id))
        
        waiting_tickets_before = request.env['digitalqueue.ticket'].sudo().search([
            ('service_id', '=', ticket.service_id.id),
            ('statut', '=', 'en_attente'),
            ('create_date', '<', ticket.create_date)
        ])
        position_in_queue = len(waiting_tickets_before) + 1
        
        people_text = f"{len(waiting_tickets_before)} personne(s) avant vous" if len(waiting_tickets_before) > 0 else "Vous êtes le premier !"
        
        html = f"""<html><head><meta charset="utf-8"/><title>Ticket Créé</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet"/>
        <style>body {{ background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%); min-height: 100vh; }}</style>
        </head><body><div class="container py-5"><div class="row justify-content-center"><div class="col-md-8">
        <div class="card shadow"><div class="card-header bg-success text-white text-center py-4"><h1>Ticket Créé !</h1></div>
        <div class="card-body p-4"><div class="text-center mb-4">
        <h2 class="text-muted mb-3">Votre numéro</h2><div style="font-size: 4rem; font-weight: bold; color: #2d3436;">{ticket.name}</div>
        <p class="text-muted">{ticket.service_id.name}</p></div>
        <div class="alert alert-info"><h5>Position dans la file: {position_in_queue}</h5><p>{people_text}</p></div>
        <a href="/digitalqueue/services" class="btn btn-primary">Prendre un autre ticket</a>
        </div></div></div></div></div><script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
        </body></html>"""
        
        return html

    @http.route('/digitalqueue/debug', type='http', auth='public', website=True)
    def debug_test(self, **kw):
        services = request.env['digitalqueue.queue_service'].sudo().search([])
        
        html = f"""<html><body style="padding: 20px; font-family: Arial;">
        <h1>DEBUG INFORMATION</h1><h2>Services trouvés: {len(services)}</h2><ul>"""
        
        for service in services:
            html += f"<li><strong>{service.name}</strong> (ID: {service.id})</li>"
        
        html += """</ul><h2>Test des liens:</h2><a href="/digitalqueue/services">Services</a>
        </body></html>"""
        
        return html