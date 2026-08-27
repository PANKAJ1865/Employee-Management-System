from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q, Avg, Sum, Count
from .models import Employee
from .forms import EmployeeForm

def employee_list(request):
    search_query = request.GET.get('q', '').strip()
    dept_filter = request.GET.get('department', '').strip()

    employees = Employee.objects.all()

    if search_query:
        employees = employees.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(designation__icontains=search_query) |
            Q(phone__icontains=search_query)
        )

    if dept_filter:
        employees = employees.filter(department__iexact=dept_filter)

    # Statistics calculation
    total_employees = Employee.objects.count()
    dept_list = Employee.objects.values_list('department', flat=True).distinct()
    stats = Employee.objects.aggregate(
        total_payroll=Sum('salary'),
        avg_salary=Avg('salary')
    )

    context = {
        'employees': employees,
        'search_query': search_query,
        'dept_filter': dept_filter,
        'departments': dept_list,
        'total_employees': total_employees,
        'total_payroll': stats['total_payroll'] or 0,
        'avg_salary': round(stats['avg_salary'] or 0, 2),
    }
    return render(request, 'employee_list.html', context)

def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employee_detail.html', {'employee': employee})

def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save()
            messages.success(request, f"Employee '{employee.name}' was successfully added!")
            return redirect('employee_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = EmployeeForm()
    return render(request, 'employee_form.html', {'form': form, 'title': 'Add New Employee'})

def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, f"Employee '{employee.name}' profile updated successfully!")
            return redirect('employee_detail', pk=employee.pk)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employee_form.html', {'form': form, 'employee': employee, 'title': f'Edit {employee.name}'})

def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        name = employee.name
        employee.delete()
        messages.warning(request, f"Employee '{name}' has been permanently deleted.")
    return redirect('employee_list')
