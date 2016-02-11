from collections import Iterable

from django_select2 import AutoModelSelect2Field

from django_select2_chained import (
    ChainedAutoModelSelect2Field, ChainedRequestSpecificAutoModelSelect2Field,
    PrepopulatedSelect2Widget, RequestSpecificAutoModelSelect2Field
)

from .models import Company, Employee


class CompanySelect2Field(AutoModelSelect2Field):
    search_fields = ['name__icontains']
    widget = PrepopulatedSelect2Widget
    queryset = Company.objects.all()


class RequestSpecificCompanySelect2Field(RequestSpecificAutoModelSelect2Field):
    search_fields = ['name__icontains']
    widget = PrepopulatedSelect2Widget
    queryset = Company.objects.none()

    def get_queryset(self, request):
        companies = request.GET.getlist('companies')
        try:
            companies = map(int, companies)
        except ValueError:
            pass
        else:
            if companies and isinstance(companies, Iterable):
                company_objects = Company.objects.filter(id__in=companies)
                return company_objects
        return Company.objects.all()


class EmployeeSelect2Field(ChainedAutoModelSelect2Field):
    search_fields = ['name__icontains', 'social_security_number__icontains']
    Employee.objects.all()


class RequestSpecificEmployeeSelect2Field(ChainedRequestSpecificAutoModelSelect2Field):
    search_fields = ['name__icontains', 'social_security_number__icontains']
    Employee.objects.none()

    def get_queryset(self, request):
        employees = request.GET.getlist('employees')
        try:
            employees = map(int, employees)
        except ValueError:
            pass
        else:
            if employees and isinstance(employees, Iterable):
                employee_objects = Employee.objects.filter(id__in=employees)
                return employee_objects
        return Employee.objects.all()
