import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employee_management.settings')
django.setup()

from django.contrib import admin
from django.test import Client
from employees.models import Employee

# 1. Check Model Admin Registration
registered = admin.site.is_registered(Employee)
print(f"Employee model registered in admin site: {registered}")

model_admin = admin.site._registry[Employee]

print("List Display:", model_admin.list_display)
print("Search Fields:", model_admin.search_fields)
print("List Filter:", model_admin.list_filter)

# Verify required fields
assert 'name' in model_admin.search_fields or any('name' in f for f in model_admin.search_fields), "Missing 'name' in search_fields"
assert 'department' in model_admin.search_fields or any('department' in f for f in model_admin.search_fields), "Missing 'department' in search_fields"
assert 'department' in model_admin.list_filter, "Missing 'department' in list_filter"

# 2. HTTP Admin Client Test
client = Client()
login_success = client.login(username='admin', password='adminpassword123')
print(f"Admin login status: {login_success}")

response = client.get('/admin/employees/employee/')
print(f"Admin Employee list HTTP response status code: {response.status_code}")
assert response.status_code == 200, f"Expected 200, got {response.status_code}"

# Test admin search query by name
res_search_name = client.get('/admin/employees/employee/?q=Sarah')
print(f"Admin search by name status code: {res_search_name.status_code}")
assert res_search_name.status_code == 200

# Test admin filter by department
res_filter_dept = client.get('/admin/employees/employee/?department__exact=Engineering')
print(f"Admin filter by department status code: {res_filter_dept.status_code}")
assert res_filter_dept.status_code == 200

print("\n--- ALL ADMIN VERIFICATION TESTS PASSED SUCCESSFULLY! ---")
