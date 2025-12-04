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
        
        html = """<!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="utf-8"/>
            <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
            <title>File d'Attente Digitale</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet"/>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"/>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                
                body {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    padding: 20px;
                }
                
                .header-section {
                    text-align: center;
                    margin-bottom: 50px;
                    animation: fadeInDown 0.8s ease;
                }
                
                .header-section h1 {
                    color: white;
                    font-size: 3rem;
                    font-weight: 700;
                    margin-bottom: 10px;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
                }
                
                .header-section p {
                    color: rgba(255,255,255,0.9);
                    font-size: 1.2rem;
                }
                
                .services-container {
                    max-width: 1200px;
                    margin: 0 auto;
                }
                
                .service-card {
                    background: white;
                    border-radius: 20px;
                    padding: 30px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                    transition: all 0.3s ease;
                    height: 100%;
                    display: flex;
                    flex-direction: column;
                    animation: fadeInUp 0.8s ease;
                }
                
                .service-card:hover {
                    transform: translateY(-10px);
                    box-shadow: 0 15px 40px rgba(0,0,0,0.3);
                }
                
                .service-icon {
                    width: 80px;
                    height: 80px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin: 0 auto 20px;
                    font-size: 2rem;
                    color: white;
                }
                
                .service-card h4 {
                    color: #2d3436;
                    font-size: 1.5rem;
                    font-weight: 600;
                    margin-bottom: 15px;
                    text-align: center;
                }
                
                .service-card p {
                    color: #636e72;
                    text-align: center;
                    margin-bottom: 25px;
                    flex-grow: 1;
                }
                
                .btn-take-ticket {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border: none;
                    padding: 15px 30px;
                    border-radius: 50px;
                    font-size: 1.1rem;
                    font-weight: 600;
                    transition: all 0.3s ease;
                    text-decoration: none;
                    display: inline-block;
                    width: 100%;
                    text-align: center;
                }
                
                .btn-take-ticket:hover {
                    transform: scale(1.05);
                    box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
                    color: white;
                }
                
                .no-services {
                    background: white;
                    border-radius: 20px;
                    padding: 60px;
                    text-align: center;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                    animation: fadeInUp 0.8s ease;
                }
                
                .no-services i {
                    font-size: 4rem;
                    color: #dfe6e9;
                    margin-bottom: 20px;
                }
                
                .no-services h4 {
                    color: #2d3436;
                    font-size: 1.8rem;
                    margin-bottom: 10px;
                }
                
                .no-services p {
                    color: #636e72;
                    font-size: 1.1rem;
                }
                
                @keyframes fadeInDown {
                    from {
                        opacity: 0;
                        transform: translateY(-30px);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }
                
                @keyframes fadeInUp {
                    from {
                        opacity: 0;
                        transform: translateY(30px);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }
                
                @media (max-width: 768px) {
                    .header-section h1 {
                        font-size: 2rem;
                    }
                    
                    .service-card {
                        margin-bottom: 20px;
                    }
                }
            </style>
        </head>
        <body>
            <div class="services-container">
                <div class="header-section">
                    <h1><i class="fas fa-ticket-alt"></i> File d'Attente Digitale</h1>
                    <p>Sélectionnez un service pour obtenir votre ticket</p>
                </div>
                
                <div class="row g-4">"""
        
        # Icônes différentes pour varier
        icons = ['fa-user-md', 'fa-comments', 'fa-laptop', 'fa-briefcase', 'fa-cog', 'fa-phone']
        
        for idx, service in enumerate(services):
            icon = icons[idx % len(icons)]
            html += f"""
                    <div class="col-lg-4 col-md-6">
                        <div class="service-card">
                            <div class="service-icon">
                                <i class="fas {icon}"></i>
                            </div>
                            <h4>{service.name}</h4>
                            <p>{service.description or 'Service disponible pour vous servir'}</p>
                            <a href="/digitalqueue/take_ticket?service_id={service.id}" class="btn-take-ticket">
                                <i class="fas fa-ticket-alt"></i> Prendre un ticket
                            </a>
                        </div>
                    </div>"""
        
        if not services:
            html += """
                    <div class="col-12">
                        <div class="no-services">
                            <i class="fas fa-inbox"></i>
                            <h4>Aucun service disponible</h4>
                            <p>Les services seront bientôt disponibles. Revenez plus tard !</p>
                        </div>
                    </div>"""
        
        html += """
                </div>
            </div>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
        </body>
        </html>"""
        
        return html

    @http.route('/digitalqueue/take_ticket', type='http', auth='public', website=True)
    def take_ticket(self, service_id=None, **kw):
        _logger.info(f"=== 🎫 CRÉATION TICKET pour service_id: {service_id} ===")
        service_id_int = int(service_id) if service_id else False
        
        # Compter TOUS les tickets en attente pour ce service (pas seulement ceux créés avant)
        waiting_tickets_count = request.env['digitalqueue.ticket'].sudo().search_count([
            ('service_id', '=', service_id_int),
            ('statut', '=', 'en_attente')
        ])
        
        # La priorité ET le numéro sont basés sur la position dans la file
        priority = waiting_tickets_count + 1
        
        # Obtenir le préfixe du service (première lettre du nom)
        service = request.env['digitalqueue.queue_service'].sudo().browse(service_id_int)
        service_prefix = service.name[0].upper() if service.name else 'T'
        
        # Créer le ticket avec un numéro basé sur la position
        ticket = request.env['digitalqueue.ticket'].sudo().create({
            'service_id': service_id_int,
            'priorite': priority,
            'statut': 'en_attente'
        })
        
        try:
            # Utiliser la priorité comme numéro de ticket pour cohérence
            ticket.sudo().write({'numero': f"{service_prefix}{priority}"})
            _logger.info(f"✅ Ticket créé: {ticket.numero} - Position: {priority}")
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
        
        html = f"""<!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="utf-8"/>
            <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
            <title>Ticket Créé - {ticket.name}</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet"/>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"/>
            <style>
                body {{
                    background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
                    min-height: 100vh;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    padding: 20px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }}
                
                .confirmation-container {{
                    max-width: 600px;
                    width: 100%;
                    animation: zoomIn 0.5s ease;
                }}
                
                .ticket-card {{
                    background: white;
                    border-radius: 25px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                    overflow: hidden;
                }}
                
                .ticket-header {{
                    background: linear-gradient(135deg, #00b894 0%, #00cec9 100%);
                    color: white;
                    padding: 40px;
                    text-align: center;
                }}
                
                .ticket-header i {{
                    font-size: 4rem;
                    margin-bottom: 15px;
                    animation: bounceIn 1s ease;
                }}
                
                .ticket-header h1 {{
                    font-size: 2.5rem;
                    font-weight: 700;
                    margin: 0;
                }}
                
                .ticket-body {{
                    padding: 40px;
                }}
                
                .ticket-number-section {{
                    text-align: center;
                    margin-bottom: 30px;
                    padding: 30px;
                    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                    border-radius: 15px;
                }}
                
                .ticket-label {{
                    color: #636e72;
                    font-size: 1.2rem;
                    margin-bottom: 10px;
                    font-weight: 500;
                }}
                
                .ticket-number {{
                    font-size: 5rem;
                    font-weight: 800;
                    color: #2d3436;
                    line-height: 1;
                    margin-bottom: 15px;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
                }}
                
                .service-name {{
                    color: #0984e3;
                    font-size: 1.3rem;
                    font-weight: 600;
                }}
                
                .queue-info {{
                    background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
                    color: white;
                    padding: 25px;
                    border-radius: 15px;
                    margin-bottom: 25px;
                }}
                
                .queue-info h5 {{
                    font-size: 1.4rem;
                    font-weight: 700;
                    margin-bottom: 10px;
                }}
                
                .queue-info p {{
                    font-size: 1.1rem;
                    margin: 0;
                    opacity: 0.95;
                }}
                
                .btn-return {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border: none;
                    padding: 15px 40px;
                    border-radius: 50px;
                    font-size: 1.1rem;
                    font-weight: 600;
                    transition: all 0.3s ease;
                    text-decoration: none;
                    display: inline-block;
                    width: 100%;
                    text-align: center;
                }}
                
                .btn-return:hover {{
                    transform: translateY(-3px);
                    box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
                    color: white;
                }}
                
                @keyframes zoomIn {{
                    from {{
                        opacity: 0;
                        transform: scale(0.8);
                    }}
                    to {{
                        opacity: 1;
                        transform: scale(1);
                    }}
                }}
                
                @keyframes bounceIn {{
                    0%, 20%, 40%, 60%, 80%, 100% {{
                        animation-timing-function: cubic-bezier(0.215, 0.610, 0.355, 1.000);
                    }}
                    0% {{
                        opacity: 0;
                        transform: scale3d(.3, .3, .3);
                    }}
                    20% {{
                        transform: scale3d(1.1, 1.1, 1.1);
                    }}
                    40% {{
                        transform: scale3d(.9, .9, .9);
                    }}
                    60% {{
                        opacity: 1;
                        transform: scale3d(1.03, 1.03, 1.03);
                    }}
                    80% {{
                        transform: scale3d(.97, .97, .97);
                    }}
                    100% {{
                        opacity: 1;
                        transform: scale3d(1, 1, 1);
                    }}
                }}
                
                @media (max-width: 768px) {{
                    .ticket-number {{
                        font-size: 3.5rem;
                    }}
                    
                    .ticket-header h1 {{
                        font-size: 2rem;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="confirmation-container">
                <div class="ticket-card">
                    <div class="ticket-header">
                        <i class="fas fa-check-circle"></i>
                        <h1>Ticket Créé !</h1>
                    </div>
                    
                    <div class="ticket-body">
                        <div class="ticket-number-section">
                            <div class="ticket-label">Votre numéro</div>
                            <div class="ticket-number">{ticket.name}</div>
                            <div class="service-name">
                                <i class="fas fa-briefcase"></i> {ticket.service_id.name}
                            </div>
                        </div>
                        
                        <div class="queue-info">
                            <h5><i class="fas fa-users"></i> Position dans la file: {position_in_queue}</h5>
                            <p>{people_text}</p>
                        </div>
                        
                        <a href="/digitalqueue/services" class="btn-return">
                            <i class="fas fa-plus-circle"></i> Prendre un autre ticket
                        </a>
                    </div>
                </div>
            </div>
            
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
        </body>
        </html>"""
        
        return html

    @http.route('/digitalqueue/debug', type='http', auth='public', website=True)
    def debug_test(self, **kw):
        services = request.env['digitalqueue.queue_service'].sudo().search([])
        
        html = f"""<!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="utf-8"/>
            <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
            <title>Debug - File d'Attente</title>
            <style>
                body {{
                    font-family: 'Courier New', monospace;
                    padding: 30px;
                    background: #2d3436;
                    color: #dfe6e9;
                }}
                
                h1 {{ color: #74b9ff; }}
                h2 {{ color: #00b894; margin-top: 30px; }}
                
                ul {{
                    background: #1e272e;
                    padding: 20px;
                    border-radius: 10px;
                    list-style: none;
                }}
                
                li {{
                    padding: 10px;
                    border-bottom: 1px solid #636e72;
                }}
                
                li:last-child {{ border-bottom: none; }}
                
                a {{
                    color: #74b9ff;
                    text-decoration: none;
                    padding: 10px 20px;
                    background: #0984e3;
                    border-radius: 5px;
                    display: inline-block;
                    margin-top: 20px;
                }}
                
                a:hover {{ background: #0652DD; }}
            </style>
        </head>
        <body>
            <h1>🔧 DEBUG INFORMATION</h1>
            <h2>Services trouvés: {len(services)}</h2>
            <ul>"""
        
        for service in services:
            html += f"<li><strong>{service.name}</strong> (ID: {service.id})</li>"
        
        html += """</ul>
            <h2>Test des liens:</h2>
            <a href="/digitalqueue/services">↗️ Voir les Services</a>
        </body>
        </html>"""
        
        return html