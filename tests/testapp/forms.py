from django import forms

from .fields import (
    CompanySelect2Field, EmployeeSelect2Field,
    RequestSpecificCompanySelect2Field
)


class RequestSpecificForm(forms.Form):
    company = RequestSpecificCompanySelect2Field(required=True)
    company2 = RequestSpecificCompanySelect2Field(required=False)


class ChainedForm(forms.Form):
    company = CompanySelect2Field(
        required=False,
        allow_empty=True,
        label=u"Filter by company",
    )
    employee = EmployeeSelect2Field(
        allow_empty=True,
        chain_field='customer_company',
        model_field='companies',
        label=u"Select an employee"
    )
