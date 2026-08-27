import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employee_management.settings')
django.setup()

from employees.models import Employee

sample_data = [
    {
        "name": "Sarah Connor",
        "email": "sarah.connor@cyberdyne.io",
        "phone": "+1 (555) 123-4567",
        "department": "Engineering",
        "designation": "Lead System Architect",
        "salary": 125000.00
    },
    {
        "name": "Alex Rivera",
        "email": "alex.rivera@company.com",
        "phone": "+1 (555) 987-6543",
        "department": "Design",
        "designation": "Principal UX Strategist",
        "salary": 110000.00
    },
    {
        "name": "Marcus Vance",
        "email": "m.vance@enterprise.org",
        "phone": "+1 (555) 456-7890",
        "department": "Product",
        "designation": "Senior Product Director",
        "salary": 135000.00
    },
    {
        "name": "Elena Rostova",
        "email": "elena.rostova@techcorp.com",
        "phone": "+1 (555) 321-7654",
        "department": "Engineering",
        "designation": "Backend Engineer",
        "salary": 98000.00
    }
]

for data in sample_data:
    Employee.objects.get_or_create(email=data['email'], defaults=data)

print("Sample employee data successfully seeded!")
