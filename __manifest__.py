{
    'name': "DigitalQueue",
    'summary': "Digital Queue Management System",
    'description': """
A simple digital queue management system for managing customer queues in various settings such as banks, hospitals, and service centers.
It allows agents to process clients through a digital queue system.
""",
    'author': "Ibtissam Gaamouche, Fatima Achbout & Tarik Boukaidi",
    'website': "http://www.exemple.com",
    'category': 'Services',
    'version': '16.0.1',
    'depends': ['base'],

    'data': [
        # Sécurité
        'security/groups.xml',
        'security/ir.model.access.csv',

        # Vues Agents
        'views/agent_view.xml',

        # Vues Files / Queue
        'views/queue_service_views.xml',

        # Vues Tickets
        'views/ticket_view.xml',

        # Menus (doivent être chargés après les actions)
        'views/menu.xml',

        # Website templates
        'views/booking_template.xml',
    ],

    'application': True,
    'installable': True,
}
