{ 'name': "DigitalQueue",
'summary': "Digital Queue Management System",
'description': """
A simple digital queue management system for managing customer queues in various settings such as banks, hospitals, and service centers. It allows users to take a number, view their position in the queue, and receive notifications when it's their turn.
""",
'author': "Ibtissam Gaamouche & Fatima Achbout & Tarik Boukaidi",
'website': "http://www.exemple.com",
'category': 'Uncategorized',
'version': '16.0.1',
'depends': ['base', 'website'],
'data': [
    'security/ir.model.access.csv',
      'views/menu.xml',
         'views/queue_service_views.xml',
         
    'views/booking_template.xml',
        
        
         ],


'application': True,
    'installable': True,
}