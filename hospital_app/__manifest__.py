{'name': 'Hospital Management',
 'description': 'Hospital Management Appilication.',
 'license': "AGPL-3",
 'author': 'Biju Pattera',
 'category': 'Hospital',
 'depends': ['base', 'board', 'mail'],
 'data': [
     'security/hospital_security.xml',
     'security/ir.model.access.csv',
     'views/hospital_menu.xml',
     'views/patient.xml',
     'views/appointment.xml',
 ],
 'application': True,
 'installable': True,
 'assets': {},
 }