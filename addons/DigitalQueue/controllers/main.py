from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class DigitalQueueController(http.Controller):

    @http.route('/digitalqueue/services', type='http', auth='public', website=True)
    def list_services(self, **kw):
        _logger.info("=== 🚀 ROUTE /digitalqueue/services APPELEE ===")
        
        services = request.env['queue.service'].sudo().search([('active', '=', True)])
        _logger.info(f"=== 📊 SERVICES TROUVÉS: {len(services)} ===")
        
        for service in services:
            _logger.info(f"=== 🔧 Service: {service.name} (ID: {service.id}) ===")
        
        return request.render('DigitalQueue.services_template', {
            'services': services
        })

    @http.route('/digitalqueue/take_ticket', type='http', auth='public', website=True)
    def take_ticket(self, service_id=None, **kw):
        _logger.info(f"=== 🎫 CRÉATION TICKET pour service_id: {service_id} ===")
        ticket = request.env['queue.ticket'].sudo().create({
            'service_id': int(service_id)
        })
        return request.redirect(f'/digitalqueue/ticket_confirmation?ticket_id={ticket.id}')

    @http.route('/digitalqueue/ticket_confirmation', type='http', auth='public', website=True)
    def ticket_confirmation(self, ticket_id=None, **kw):
        ticket = request.env['queue.ticket'].sudo().browse(int(ticket_id))
        
        # ⭐⭐ CALCULER LA POSITION DANS LA FILE ⭐⭐
        waiting_tickets_before = request.env['queue.ticket'].sudo().search([
            ('service_id', '=', ticket.service_id.id),
            ('status', '=', 'waiting'),
            ('create_date', '<', ticket.create_date)
        ])
        position_in_queue = len(waiting_tickets_before) + 1
        
        _logger.info(f"=== 📊 POSITION CALCULÉE: {position_in_queue} (personnes avant: {len(waiting_tickets_before)}) ===")
        
        return request.render('DigitalQueue.ticket_template', {
            'ticket': ticket,
            'position_in_queue': position_in_queue,
            'people_before': len(waiting_tickets_before)
        })

    # Route de debug
    @http.route('/digitalqueue/debug', type='http', auth='public', website=True)
    def debug_test(self, **kw):
        services = request.env['queue.service'].sudo().search([])
        
        debug_html = f"""
        <html>
        <body style="padding: 20px; font-family: Arial;">
            <h1>🧪 DEBUG INFORMATION</h1>
            <h2>Services trouvés: {len(services)}</h2>
            <ul>
        """
        
        for service in services:
            debug_html += f"<li><strong>{service.name}</strong> (ID: {service.id})</li>"
        
        debug_html += """
            </ul>
            <h2>Test des liens:</h2>
            <a href="/digitalqueue/services">Lien vers services</a><br/>
            <h2>Si aucun service, créez-en dans:</h2>
            <p>Paramètres → Technique → Base → Modèles → queue.service</p>
        </body>
        </html>
        """
        
        return debug_html