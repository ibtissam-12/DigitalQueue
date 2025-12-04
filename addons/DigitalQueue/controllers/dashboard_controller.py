from odoo import http
from odoo.http import request
import json
import logging

_logger = logging.getLogger(__name__)

class DigitalQueueDashboardController(http.Controller):
    
    @http.route('/digitalqueue/dashboard', type='http', auth='user', website=True)
    def admin_dashboard(self, **kw):
        """Dashboard principal pour l'administration"""
        try:
            if not request.env.user.has_group('base.group_system'):
                return "<h1>Accès refusé</h1><p>Réservé aux administrateurs</p>"
            
            # Récupérer les données du dashboard
            dashboard_data = request.env['digitalqueue.dashboard'].get_dashboard_data()
            
            html = '''<html>
            <head>
                <meta charset="utf-8"/>
                <title>Dashboard Admin - DigitalQueue</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet"/>
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.8.1/font/bootstrap-icons.css">
                <link href="https://cdn.jsdelivr.net/npm/chart.js@3.7.1/dist/chart.min.css" rel="stylesheet">
                <style>
                    body { background: #f8f9fa; font-family: 'Segoe UI', system-ui, sans-serif; }
                    .dashboard-header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
                    .stat-card { transition: transform 0.3s; border-radius: 10px; overflow: hidden; }
                    .stat-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.1); }
                    .stat-number { font-size: 2.5rem; font-weight: 700; }
                    .service-badge { font-size: 0.8em; padding: 3px 8px; }
                    .progress-thin { height: 8px; }
                    .chart-container { background: white; border-radius: 10px; padding: 20px; margin-bottom: 20px; }
                    .table-hover tbody tr:hover { background-color: rgba(0,123,255,0.05); }
                    .badge-efficiency { background: linear-gradient(90deg, #28a745, #20c997); }
                    .badge-waiting { background: linear-gradient(90deg, #ffc107, #fd7e14); }
                    .badge-unavailable { background: linear-gradient(90deg, #6c757d, #495057); }
                    .refresh-btn { position: fixed; bottom: 20px; right: 20px; z-index: 1000; }
                </style>
            </head>
            <body>
                <!-- En-tête -->
                <nav class="navbar navbar-expand-lg navbar-dark dashboard-header">
                    <div class="container-fluid">
                        <a class="navbar-brand" href="#">
                            <i class="bi bi-speedometer2 me-2"></i>
                            <strong>Dashboard Admin</strong> - DigitalQueue
                        </a>
                        <div class="navbar-text">
                            <span id="currentTime"></span> | 
                            <span>''' + request.env.user.name + '''</span>
                            <a href="/web" class="btn btn-light btn-sm ms-3">
                                <i class="bi bi-box-arrow-left"></i> Retour Odoo
                            </a>
                        </div>
                    </div>
                </nav>
                
                <!-- Contenu principal -->
                <div class="container-fluid mt-4">
                    <!-- En-tête des statistiques -->
                    <div class="row mb-4">
                        <div class="col-12">
                            <div class="d-flex justify-content-between align-items-center">
                                <h3 class="text-dark">
                                    <i class="bi bi-bar-chart-line me-2"></i>
                                    Vue d'ensemble
                                </h3>
                                <div class="text-muted">
                                    <i class="bi bi-clock me-1"></i>
                                    Dernière mise à jour: <span id="lastUpdate">''' + dashboard_data['last_update'] + '''</span>
                                    <button onclick="refreshDashboard()" class="btn btn-sm btn-outline-primary ms-3">
                                        <i class="bi bi-arrow-clockwise"></i> Actualiser
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Cartes de statistiques globales -->
                    <div class="row mb-4">
                        <div class="col-xl-2 col-md-4 col-sm-6 mb-3">
                            <div class="card stat-card border-primary">
                                <div class="card-body text-center">
                                    <h6 class="card-subtitle mb-2 text-muted">Tickets Aujourd'hui</h6>
                                    <div class="stat-number text-primary">''' + str(dashboard_data['global_stats']['total_today']) + '''</div>
                                    <p class="card-text small">
                                        <i class="bi bi-plus-circle text-success"></i>
                                        <span class="text-success">''' + str(dashboard_data['global_stats']['finished_today']) + ''' terminés</span>
                                    </p>
                                </div>
                            </div>
                        </div>
                        
                        <div class="col-xl-2 col-md-4 col-sm-6 mb-3">
                            <div class="card stat-card border-warning">
                                <div class="card-body text-center">
                                    <h6 class="card-subtitle mb-2 text-muted">En Attente</h6>
                                    <div class="stat-number text-warning">''' + str(dashboard_data['global_stats']['waiting']) + '''</div>
                                    <p class="card-text small">
                                        <i class="bi bi-people text-warning"></i>
                                        <span class="text-warning">''' + str(dashboard_data['global_stats']['active_calls']) + ''' appelés</span>
                                    </p>
                                </div>
                            </div>
                        </div>
                        
                        <div class="col-xl-2 col-md-4 col-sm-6 mb-3">
                            <div class="card stat-card border-success">
                                <div class="card-body text-center">
                                    <h6 class="card-subtitle mb-2 text-muted">Agents</h6>
                                    <div class="stat-number text-success">''' + dashboard_data['global_stats']['available_agents'] + '''</div>
                                    <p class="card-text small">
                                        <i class="bi bi-person-check text-success"></i>
                                        <span>Disponibles</span>
                                    </p>
                                </div>
                            </div>
                        </div>
                        
                        <div class="col-xl-2 col-md-4 col-sm-6 mb-3">
                            <div class="card stat-card border-info">
                                <div class="card-body text-center">
                                    <h6 class="card-subtitle mb-2 text-muted">Temps d'Attente</h6>
                                    <div class="stat-number text-info">''' + dashboard_data['global_stats']['avg_wait_time'] + '''</div>
                                    <p class="card-text small">
                                        <i class="bi bi-clock-history text-info"></i>
                                        <span>Moyenne</span>
                                    </p>
                                </div>
                            </div>
                        </div>
                        
                        <div class="col-xl-2 col-md-4 col-sm-6 mb-3">
                            <div class="card stat-card border-danger">
                                <div class="card-body text-center">
                                    <h6 class="card-subtitle mb-2 text-muted">Satisfaction</h6>
                                    <div class="stat-number text-danger">''' + dashboard_data['global_stats']['satisfaction_rate'] + '''</div>
                                    <p class="card-text small">
                                        <i class="bi bi-emoji-smile text-danger"></i>
                                        <span>Taux</span>
                                    </p>
                                </div>
                            </div>
                        </div>
                        
                        <div class="col-xl-2 col-md-4 col-sm-6 mb-3">
                            <div class="card stat-card border-secondary">
                                <div class="card-body text-center">
                                    <h6 class="card-subtitle mb-2 text-muted">Services Actifs</h6>
                                    <div class="stat-number text-secondary">''' + str(len([s for s in dashboard_data['service_stats'] if s['active']])) + '''</div>
                                    <p class="card-text small">
                                        <i class="bi bi-gear text-secondary"></i>
                                        <span>Services</span>
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Graphiques et données -->
                    <div class="row">
                        <!-- Graphique d'évolution -->
                        <div class="col-lg-8 mb-4">
                            <div class="chart-container">
                                <h5 class="mb-3">
                                    <i class="bi bi-graph-up me-2"></i>
                                    Évolution sur 7 jours
                                </h5>
                                <canvas id="dailyChart" height="100"></canvas>
                            </div>
                            
                            <!-- Performance des services -->
                            <div class="chart-container">
                                <h5 class="mb-3">
                                    <i class="bi bi-pie-chart me-2"></i>
                                    Performance par Service
                                </h5>
                                <div class="table-responsive">
                                    <table class="table table-hover">
                                        <thead class="table-light">
                                            <tr>
                                                <th>Service</th>
                                                <th>Code</th>
                                                <th>En attente</th>
                                                <th>Aujourd'hui</th>
                                                <th>Terminés</th>
                                                <th>Efficacité</th>
                                                <th>Statut</th>
                                            </tr>
                                        </thead>
                                        <tbody id="servicesTable">
                                            <!-- Rempli par JavaScript -->
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Colonne droite -->
                        <div class="col-lg-4">
                            <!-- Agents -->
                            <div class="chart-container mb-4">
                                <h5 class="mb-3">
                                    <i class="bi bi-people me-2"></i>
                                    Performance des Agents
                                </h5>
                                <div class="table-responsive">
                                    <table class="table table-sm">
                                        <thead>
                                            <tr>
                                                <th>Agent</th>
                                                <th>Service</th>
                                                <th>Tickets</th>
                                                <th>Efficacité</th>
                                            </tr>
                                        </thead>
                                        <tbody id="agentsTable">
                                            <!-- Rempli par JavaScript -->
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                            
                            <!-- Tickets récents -->
                            <div class="chart-container">
                                <h5 class="mb-3">
                                    <i class="bi bi-clock-history me-2"></i>
                                    Tickets Récents
                                </h5>
                                <div id="recentTickets">
                                    <!-- Rempli par JavaScript -->
                                </div>
                            </div>
                            
                            <!-- Actions rapides -->
                            <div class="chart-container mt-4">
                                <h5 class="mb-3">
                                    <i class="bi bi-lightning me-2"></i>
                                    Actions Rapides
                                </h5>
                                <div class="d-grid gap-2">
                                    <a href="/web#action=digitalqueue.action_queue_service" class="btn btn-primary">
                                        <i class="bi bi-gear me-2"></i>Gérer les Services
                                    </a>
                                    <a href="/web#action=digitalqueue.action_agent" class="btn btn-success">
                                        <i class="bi bi-people me-2"></i>Gérer les Agents
                                    </a>
                                    <a href="/web#action=digitalqueue.action_ticket" class="btn btn-warning">
                                        <i class="bi bi-ticket-detailed me-2"></i>Voir tous les Tickets
                                    </a>
                                    <a href="/digitalqueue/agent_dashboard" class="btn btn-info">
                                        <i class="bi bi-speedometer me-2"></i>Dashboard Agent
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Bouton de rafraîchissement flottant -->
                <div class="refresh-btn">
                    <button onclick="refreshDashboard()" class="btn btn-primary btn-lg rounded-circle shadow-lg" 
                            style="width: 60px; height: 60px;">
                        <i class="bi bi-arrow-clockwise"></i>
                    </button>
                </div>
                
                <!-- Scripts -->
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
                <script src="https://cdn.jsdelivr.net/npm/chart.js@3.7.1/dist/chart.min.js"></script>
                <script>
                    // Données du dashboard
                    const dashboardData = ''' + json.dumps(dashboard_data) + ''';
                    
                    // Mettre à jour l'heure
                    function updateTime() {
                        const now = new Date();
                        document.getElementById('currentTime').textContent = 
                            now.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
                    }
                    setInterval(updateTime, 1000);
                    updateTime();
                    
                    // Initialiser le graphique d'évolution
                    function initDailyChart() {
                        const ctx = document.getElementById('dailyChart').getContext('2d');
                        const labels = dashboardData.daily_stats.map(d => d.day + ' ' + d.date);
                        const ticketsData = dashboardData.daily_stats.map(d => d.tickets);
                        const finishedData = dashboardData.daily_stats.map(d => d.finished);
                        
                        new Chart(ctx, {
                            type: 'line',
                            data: {
                                labels: labels,
                                datasets: [
                                    {
                                        label: 'Tickets créés',
                                        data: ticketsData,
                                        borderColor: '#4A6FA5',
                                        backgroundColor: 'rgba(74, 111, 165, 0.1)',
                                        tension: 0.4,
                                        fill: true
                                    },
                                    {
                                        label: 'Tickets terminés',
                                        data: finishedData,
                                        borderColor: '#7FB685',
                                        backgroundColor: 'rgba(127, 182, 133, 0.1)',
                                        tension: 0.4,
                                        fill: true
                                    }
                                ]
                            },
                            options: {
                                responsive: true,
                                plugins: {
                                    legend: {
                                        position: 'top',
                                    },
                                    tooltip: {
                                        mode: 'index',
                                        intersect: false
                                    }
                                },
                                scales: {
                                    y: {
                                        beginAtZero: true,
                                        title: {
                                            display: true,
                                            text: 'Nombre de tickets'
                                        }
                                    }
                                }
                            }
                        });
                    }
                    
                    // Remplir le tableau des services
                    function populateServicesTable() {
                        const tbody = document.getElementById('servicesTable');
                        let html = '';
                        
                        dashboardData.service_stats.forEach(service => {
                            const efficiencyClass = service.efficiency >= 80 ? 'badge-efficiency' : 
                                                  service.efficiency >= 50 ? 'badge-waiting' : 'badge-unavailable';
                            
                            html += `
                                <tr>
                                    <td>
                                        <strong>${service.name}</strong>
                                        ${service.active ? 
                                            '<span class="badge bg-success ms-2">Actif</span>' : 
                                            '<span class="badge bg-secondary ms-2">Inactif</span>'}
                                    </td>
                                    <td><code>${service.code}</code></td>
                                    <td>
                                        <span class="badge bg-warning">${service.waiting}</span>
                                    </td>
                                    <td>${service.today_tickets}</td>
                                    <td>${service.today_finished}</td>
                                    <td>
                                        <div class="d-flex align-items-center">
                                            <div class="progress progress-thin flex-grow-1 me-2">
                                                <div class="progress-bar ${efficiencyClass}" 
                                                     role="progressbar" 
                                                     style="width: ${service.efficiency}%">
                                                </div>
                                            </div>
                                            <span>${service.efficiency}%</span>
                                        </div>
                                    </td>
                                    <td>
                                        ${service.active ? 
                                            '<i class="bi bi-check-circle text-success"></i>' : 
                                            '<i class="bi bi-x-circle text-danger"></i>'}
                                    </td>
                                </tr>
                            `;
                        });
                        
                        tbody.innerHTML = html;
                    }
                    
                    // Remplir le tableau des agents
                    function populateAgentsTable() {
                        const tbody = document.getElementById('agentsTable');
                        let html = '';
                        
                        dashboardData.agent_stats.forEach(agent => {
                            const efficiencyClass = agent.efficiency >= 80 ? 'badge-efficiency' : 
                                                   agent.efficiency >= 50 ? 'badge-waiting' : 'badge-unavailable';
                            
                            html += `
                                <tr>
                                    <td>
                                        <div class="d-flex align-items-center">
                                            ${agent.available ? 
                                                '<i class="bi bi-circle-fill text-success me-2" style="font-size: 0.6rem;"></i>' : 
                                                '<i class="bi bi-circle-fill text-danger me-2" style="font-size: 0.6rem;"></i>'}
                                            ${agent.name}
                                        </div>
                                    </td>
                                    <td><small>${agent.service}</small></td>
                                    <td>
                                        <span class="badge bg-info">${agent.tickets_today}</span>
                                    </td>
                                    <td>
                                        <div class="d-flex align-items-center">
                                            <div class="progress progress-thin flex-grow-1 me-2">
                                                <div class="progress-bar ${efficiencyClass}" 
                                                     role="progressbar" 
                                                     style="width: ${agent.efficiency}%">
                                                </div>
                                            </div>
                                            <small>${Math.round(agent.efficiency)}%</small>
                                        </div>
                                    </td>
                                </tr>
                            `;
                        });
                        
                        tbody.innerHTML = html;
                    }
                    
                    // Remplir les tickets récents
                    function populateRecentTickets() {
                        const container = document.getElementById('recentTickets');
                        let html = '';
                        
                        if (dashboardData.recent_tickets.length === 0) {
                            html = '<p class="text-center text-muted">Aucun ticket aujourd\'hui</p>';
                        } else {
                            dashboardData.recent_tickets.forEach(ticket => {
                                let statusBadge = '';
                                if (ticket.status === 'en_attente') statusBadge = '<span class="badge bg-info">En attente</span>';
                                else if (ticket.status === 'appele') statusBadge = '<span class="badge bg-warning">Appelé</span>';
                                else if (ticket.status === 'en_cours') statusBadge = '<span class="badge bg-primary">En cours</span>';
                                else if (ticket.status === 'termine') statusBadge = '<span class="badge bg-success">Terminé</span>';
                                else if (ticket.status === 'rate') statusBadge = '<span class="badge bg-danger">Raté</span>';
                                
                                html += `
                                    <div class="border-bottom py-2">
                                        <div class="d-flex justify-content-between">
                                            <div>
                                                <strong>${ticket.number}</strong>
                                                <br>
                                                <small class="text-muted">${ticket.service}</small>
                                            </div>
                                            <div class="text-end">
                                                ${statusBadge}
                                                <br>
                                                <small class="text-muted">${ticket.wait_time}</small>
                                            </div>
                                        </div>
                                    </div>
                                `;
                            });
                        }
                        
                        container.innerHTML = html;
                    }
                    
                    // Rafraîchir le dashboard
                    function refreshDashboard() {
                        document.querySelector('.refresh-btn button').innerHTML = 
                            '<div class="spinner-border spinner-border-sm" role="status"></div>';
                        
                        fetch('/digitalqueue/dashboard_data')
                            .then(response => response.json())
                            .then(data => {
                                if (data.success) {
                                    // Mettre à jour l'affichage
                                    document.getElementById('lastUpdate').textContent = data.data.last_update;
                                    location.reload();
                                }
                            })
                            .finally(() => {
                                document.querySelector('.refresh-btn button').innerHTML = 
                                    '<i class="bi bi-arrow-clockwise"></i>';
                            });
                    }
                    
                    // Exporter les données
                    function exportData(format) {
                        fetch('/digitalqueue/export_dashboard?format=' + format)
                            .then(response => response.blob())
                            .then(blob => {
                                const url = window.URL.createObjectURL(blob);
                                const a = document.createElement('a');
                                a.href = url;
                                a.download = `dashboard_${new Date().toISOString().split('T')[0]}.${format}`;
                                a.click();
                            });
                    }
                    
                    // Initialisation
                    document.addEventListener('DOMContentLoaded', function() {
                        initDailyChart();
                        populateServicesTable();
                        populateAgentsTable();
                        populateRecentTickets();
                    });
                </script>
            </body>
            </html>'''
            
            return html
            
        except Exception as e:
            _logger.error(f"Erreur admin_dashboard: {e}")
            return f"<h1>Erreur</h1><p>{str(e)}</p>"
    
    @http.route('/digitalqueue/dashboard_data', type='http', auth='user', methods=['GET'])
    def get_dashboard_data(self, **kw):
        """API pour récupérer les données du dashboard"""
        try:
            dashboard_data = request.env['digitalqueue.dashboard'].get_dashboard_data()
            return json.dumps({
                'success': True,
                'data': dashboard_data
            })
        except Exception as e:
            _logger.error(f"Erreur get_dashboard_data: {e}")
            return json.dumps({'success': False, 'error': str(e)})
    
    @http.route('/digitalqueue/export_dashboard', type='http', auth='user', methods=['GET'])
    def export_dashboard(self, format='csv', **kw):
        """Exporter les données du dashboard"""
        try:
            dashboard_data = request.env['digitalqueue.dashboard'].get_dashboard_data()
            
            if format == 'csv':
                # Exporter en CSV
                import csv
                import io
                
                output = io.StringIO()
                writer = csv.writer(output)
                
                # En-tête
                writer.writerow(['Dashboard DigitalQueue - Export', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
                writer.writerow([])
                
                # Statistiques globales
                writer.writerow(['STATISTIQUES GLOBALES'])
                for key, value in dashboard_data['global_stats'].items():
                    writer.writerow([key.replace('_', ' ').title(), value])
                writer.writerow([])
                
                # Services
                writer.writerow(['PERFORMANCE DES SERVICES'])
                writer.writerow(['Service', 'Code', 'En attente', 'Aujourd\'hui', 'Terminés', 'Efficacité', 'Statut'])
                for service in dashboard_data['service_stats']:
                    writer.writerow([
                        service['name'],
                        service['code'],
                        service['waiting'],
                        service['today_tickets'],
                        service['today_finished'],
                        f"{service['efficiency']}%",
                        'Actif' if service['active'] else 'Inactif'
                    ])
                
                csv_data = output.getvalue()
                output.close()
                
                headers = [
                    ('Content-Type', 'text/csv'),
                    ('Content-Disposition', 'attachment; filename="dashboard_export.csv"')
                ]
                return request.make_response(csv_data, headers=headers)
            
            else:
                # Export JSON par défaut
                headers = [
                    ('Content-Type', 'application/json'),
                    ('Content-Disposition', 'attachment; filename="dashboard_export.json"')
                ]
                return request.make_response(json.dumps(dashboard_data, indent=2), headers=headers)
                
        except Exception as e:
            _logger.error(f"Erreur export_dashboard: {e}")
            return json.dumps({'success': False, 'error': str(e)})