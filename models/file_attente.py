from odoo import models, fields

class FileAttente(models.Model):
    _name = "digitalqueue.file_attente"
    _description = "File d'attente"

    nom = fields.Char(required=True)
    capacite_max = fields.Integer()
    tickets_ids = fields.One2many("digitalqueue.ticket", "file_id", string="Tickets")
