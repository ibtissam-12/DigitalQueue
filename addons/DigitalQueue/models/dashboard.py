from odoo import models, fields, api
from datetime import datetime, timedelta
import json

class DigitalQueueDashboard(models.Model):
    _name = 'digitalqueue.dashboard'
    _description = 'Dashboard'
    _auto = False  # Pas de table dans la base
    
    @api.model
    def get_stats(self):
        """Récupère les statistiques pour le dashboard"""
        today = datetime.now().date()
        today_start = datetime.combine(today, datetime.min.time())
        
        return {
            'total_today': self.env['digitalqueue.ticket'].search_count([
                ('create_date', '>=', today_start)
            ]),
            'waiting': self.env['digitalqueue.ticket'].search_count([
                ('statut', '=', 'en_attente')
            ]),
            'active_calls': self.env['digitalqueue.ticket'].search_count([
                ('statut', 'in', ['appele', 'en_cours'])
            ]),
            'finished_today': self.env['digitalqueue.ticket'].search_count([
                ('statut', 'in', ['termine', 'rate']),
                ('write_date', '>=', today_start)
            ]),
            'available_agents': self.env['digitalqueue.agent'].search_count([
                ('est_disponible', '=', True)
            ]),
            'total_agents': self.env['digitalqueue.agent'].search_count([]),
        }