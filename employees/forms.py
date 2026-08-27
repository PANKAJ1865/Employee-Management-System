from django import forms
from django.core.exceptions import ValidationError
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'email', 'phone', 'department', 'designation', 'salary']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Jane Doe', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'e.g. jane.doe@company.com', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. +1 (555) 234-5678', 'required': True}),
            'department': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Engineering', 'required': True}),
            'designation': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Senior Software Architect', 'required': True}),
            'salary': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'e.g. 95000.00', 'step': '0.01', 'required': True}),
        }

    def clean_salary(self):
        salary = self.cleaned_data.get('salary')
        if salary is not None and salary <= 0:
            raise ValidationError("Salary must be greater than zero.")
        return salary

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower().strip()
            qs = Employee.objects.filter(email__iexact=email)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError("An employee with this email address already exists.")
        return email
