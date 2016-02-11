# -*- coding:utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from itertools import chain
import random
import string

import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

browsers = {
    'firefox': webdriver.Firefox,
    # 'chrome': webdriver.Chrome,
    # 'phantomjs': webdriver.PhantomJS,
}


def random_string(n):
    return ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(n)
    )


@pytest.fixture(scope='session',
                params=browsers.keys())
def driver(request):
    # if 'DISPLAY' not in os.environ:
    #     pytest.skip('Test requires display server (export DISPLAY)')

    try:
        b = browsers[request.param]()
    except WebDriverException as e:
        pytest.skip(e)
    else:
        b.set_window_size(1200, 800)
        request.addfinalizer(lambda *args: b.quit())
        return b


@pytest.fixture
def companies(db):
    from .testapp.models import Company

    return Company.objects.bulk_create(
        [Company(pk=pk, name=random_string(30)) for pk in range(100)]
    )


@pytest.fixture
def employees(companies):
    from .testapp.models import Employee
    return Employee.objects.bulk_create(list(chain.from_iterable(
        chain(
            (Employee(company=company, social_security_number=random_string(30)) for _ in range(10)),
            (Employee(company=company) for _ in range(3))
        ) for company in companies
    )))
