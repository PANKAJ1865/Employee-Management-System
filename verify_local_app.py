import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employee_management.settings')
django.setup()

from django.test import Client
from employees.models import Employee

client = Client()

print("Total Employee Records in DB:", Employee.objects.count())

# 1. Test Dashboard Route at localhost
res_list = client.get('/', HTTP_HOST='localhost')
print("GET http://localhost:8000/ -> Status Code:", res_list.status_code)
assert res_list.status_code == 200, f"Expected 200, got {res_list.status_code}"

# 2. Test Admin Login Page
res_admin = client.get('/admin/login/?next=/admin/', HTTP_HOST='localhost')
print("GET http://localhost:8000/admin/ -> Status Code:", res_admin.status_code)
assert res_admin.status_code == 200, f"Expected 200, got {res_admin.status_code}"

# 3. Test Add Employee Route
res_add = client.get('/add/', HTTP_HOST='localhost')
print("GET http://localhost:8000/add/ -> Status Code:", res_add.status_code)
assert res_add.status_code == 200, f"Expected 200, got {res_add.status_code}"

# 4. Test Employee Detail Route
first_emp = Employee.objects.first()
if first_emp:
    res_detail = client.get(f'/{first_emp.pk}/', HTTP_HOST='localhost')
    print(f"GET http://localhost:8000/{first_emp.pk}/ -> Status Code:", res_detail.status_code)
    assert res_detail.status_code == 200, f"Expected 200, got {res_detail.status_code}"

print("\n--- ALL LOCALHOST ENDPOINTS CONFIRMED WORKING PERFECTLY! ---")
