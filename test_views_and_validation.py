import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employee_management.settings')
django.setup()

from django.test import Client
from employees.models import Employee
from employees.forms import EmployeeForm

client = Client()

print("--- 1. Testing EmployeeForm Validation ---")

# Test 1: Negative Salary Validation
form_bad_salary = EmployeeForm(data={
    'name': 'Test User',
    'email': 'test.user@example.com',
    'phone': '1234567890',
    'department': 'Testing',
    'designation': 'QA Engineer',
    'salary': -500.00
})
assert not form_bad_salary.is_valid(), "Form should be invalid for salary <= 0"
assert 'salary' in form_bad_salary.errors, "Expected error on salary field"
print("Passed: Negative salary correctly rejected with error:", form_bad_salary.errors['salary'])

# Test 2: Invalid Email Format
form_bad_email = EmployeeForm(data={
    'name': 'Test User',
    'email': 'not-an-email',
    'phone': '1234567890',
    'department': 'Testing',
    'designation': 'QA Engineer',
    'salary': 50000.00
})
assert not form_bad_email.is_valid(), "Form should be invalid for malformed email"
assert 'email' in form_bad_email.errors, "Expected error on email field"
print("Passed: Invalid email format correctly rejected with error:", form_bad_email.errors['email'])

# Test 3: Duplicate Email Validation
# Sarah Connor email already exists in seeded database
form_duplicate_email = EmployeeForm(data={
    'name': 'Sarah Fake',
    'email': 'sarah.connor@cyberdyne.io',
    'phone': '1234567890',
    'department': 'Testing',
    'designation': 'QA Engineer',
    'salary': 50000.00
})
assert not form_duplicate_email.is_valid(), "Form should be invalid for duplicate email"
assert 'email' in form_duplicate_email.errors, "Expected error on duplicate email"
print("Passed: Duplicate email correctly rejected with error:", form_duplicate_email.errors['email'])


print("\n--- 2. Testing Function-Based Views & URLs ---")

# Test 4: List View
response_list = client.get('/')
assert response_list.status_code == 200, f"List view failed with code {response_list.status_code}"
print("Passed: employee_list view returned 200 OK")

# Test 5: Create View (GET & POST)
response_add_get = client.get('/add/')
assert response_add_get.status_code == 200, "Add view GET request failed"

response_add_post = client.post('/add/', data={
    'name': 'New Hire',
    'email': 'new.hire@company.com',
    'phone': '+1 555 999 1111',
    'department': 'Engineering',
    'designation': 'Junior Dev',
    'salary': '72000.00'
})
assert response_add_post.status_code == 302, f"Add view POST should redirect, got {response_add_post.status_code}"
created_emp = Employee.objects.get(email='new.hire@company.com')
print(f"Passed: Created new employee ID {created_emp.pk}: {created_emp.name}")

# Test 6: Detail View
response_detail = client.get(f'/{created_emp.pk}/')
assert response_detail.status_code == 200, "Detail view failed"
print("Passed: employee_detail view returned 200 OK")

# Test 7: Edit View (GET & POST)
response_edit_post = client.post(f'/{created_emp.pk}/edit/', data={
    'name': 'New Hire Updated',
    'email': 'new.hire@company.com',
    'phone': '+1 555 999 1111',
    'department': 'Engineering',
    'designation': 'Mid-level Dev',
    'salary': '85000.00'
})
assert response_edit_post.status_code == 302, "Edit view POST should redirect"
created_emp.refresh_from_db()
assert created_emp.designation == 'Mid-level Dev', "Update failed"
print(f"Passed: Updated employee designation to: {created_emp.designation}")

# Test 8: Delete View (GET & POST)
response_delete_post = client.post(f'/{created_emp.pk}/delete/')
assert response_delete_post.status_code == 302, "Delete view POST should redirect"
assert not Employee.objects.filter(pk=created_emp.pk).exists(), "Delete failed"
print("Passed: employee_delete view removed employee record successfully")

print("\n--- ALL FUNCTION-BASED VIEWS & FORM VALIDATION TESTS PASSED! ---")
