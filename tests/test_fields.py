# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json

import pytest
from django.core.urlresolvers import reverse
from django.utils.encoding import smart_text
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import ui

from tests.testapp import forms


class TestRequestSpecificAutoModelSelect2Field(object):
    url = reverse('request_specific')
    auto_field_url = reverse('django_select2_central_json')
    form = forms.RequestSpecificForm()
    company_field_id = form.fields['company'].field_id

    def test_form_exists(self):
        assert self.form.as_p()

    def test_company_exists(self, client, companies):
        company = companies[1]
        response = client.get(
            self.auto_field_url,
            {
                'field_id': self.company_field_id,
                'term': company.name,
                'page': 1
            }
        )
        assert response.status_code == 200
        data = json.loads(response.content.decode('utf-8'))
        assert data['results']
        assert {'id': company.pk, 'text': smart_text(company)} in data['results']

    def test_company_filter_list_exists(self, client, companies):
        company = companies[1]
        response = client.get(
            self.auto_field_url,
            {
                'field_id': self.company_field_id,
                'term': company.name,
                'page': 1,
                'companies': [1, 3, 5]
            }
        )
        assert response.status_code == 200
        data = json.loads(response.content.decode('utf-8'))
        assert data['results']
        assert {'id': company.pk, 'text': smart_text(company)} in data['results']

    def test_company_not_in_list(self, client, companies):
        company = companies[0]
        response = client.get(
            self.auto_field_url,
            {
                'field_id': self.company_field_id,
                'term': company.name,
                'page': 1,
                'companies': [1, 3, 5]
            }
        )
        assert response.status_code == 200
        data = json.loads(response.content.decode('utf-8'))
        assert data == {"results": [], "err": "nil", "more": False}

    def test_company_no_such_name(self, client, companies):
        response = client.get(
            self.auto_field_url,
            {
                'field_id': self.company_field_id,
                'term': "a" * 50,  # Max company name length == 30.
                'page': 1
            }
        )
        assert response.status_code == 200
        data = json.loads(response.content.decode('utf-8'))
        assert data == {"results": [], "err": "nil", "more": False}

    def test_initial_data(self, companies):
        company = companies[0]
        form = self.form.__class__(initial={'company': company.pk})
        assert unicode(company) not in form.as_p()

    def test_allow_clear(self, db):
        required_field = self.form.fields['company']
        assert required_field.required is True

        not_required_field = self.form.fields['company2']
        assert not_required_field.required is False

    def test_no_js_error(self, db, live_server, driver):
        driver.get(live_server + self.url)
        with pytest.raises(NoSuchElementException):
            error = driver.find_element_by_xpath('//body[@JSError]')
            pytest.fail(error.get_attribute('JSError'))

    def test_selecting(self, live_server, driver, companies, employees):
        driver.get(live_server + self.url)
        wait = ui.WebDriverWait(driver, 10)
        results = driver.find_element_by_css_selector('.select2-results')
        assert results.is_displayed() is False
        elem = driver.find_element_by_css_selector('.select2-container')
        elem.click()
        wait.until(lambda driver: driver.find_element_by_css_selector('.select2-result'))
        result = driver.find_element_by_css_selector('.select2-result')
        assert result.is_displayed()
        drop_mask = driver.find_element_by_css_selector('.select2-drop-mask')
        drop_mask.click()
        with pytest.raises(NoSuchElementException):
            result = driver.find_element_by_css_selector('.select2-result')

        with pytest.raises(NoSuchElementException):
            error = driver.find_element_by_xpath('//body[@JSError]')
            pytest.fail(error.get_attribute('JSError'))
