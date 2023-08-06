# pylint: disable=dangerous-default-value
import logging
from typing import List, Optional

from django.db.models import Model
from nwon_baseline.typings import AnyDict

from nwon_django_toolbox.settings import NWON_DJANGO_SETTINGS
from nwon_django_toolbox.tests.api_client import ApiTest
from nwon_django_toolbox.typings.permission_test_expectation import (
    LoginFunction,
    PermissionTestExpectation,
)
from nwon_django_toolbox.url_helper import detail_url_for_model, list_url_for_model

LOGGER = logging.getLogger(NWON_DJANGO_SETTINGS.logger_name)


def check_permissions(
    model: Model,
    expectations: List[PermissionTestExpectation],
    login_function: LoginFunction,
    post_parameter: AnyDict = {},
    put_parameter: AnyDict = {},
    patch_parameter: AnyDict = {},
):
    for expectation in expectations:
        check_permission(
            model,
            expectation,
            login_function,
            post_parameter,
            put_parameter,
            patch_parameter,
        )


def check_permission(
    model: Model,
    expectation: PermissionTestExpectation,
    login_function: LoginFunction,
    post_parameter: AnyDict = {},
    put_parameter: AnyDict = {},
    patch_parameter: AnyDict = {},
):
    token = login_function(expectation.user, expectation.password)
    api_test = ApiTest(token)

    check_get_list_permissions(
        api_test,
        model,
        expectation.get_list_status_code,
        expectation.get_list_return_number,
    )

    if expectation.get_detail_status_code:
        check_get_detail_permissions(
            api_test, model, expectation.get_detail_status_code
        )

    if expectation.create_status_code:
        check_post_permissions(
            api_test, model, expectation.create_status_code, post_parameter
        )

    if expectation.put_status_code:
        check_put_permissions(
            api_test, model, expectation.put_status_code, put_parameter
        )

    if expectation.patch_status_code:
        check_patch_permissions(
            api_test, model, expectation.patch_status_code, patch_parameter
        )

    if expectation.delete_status_code:
        check_delete_permissions(api_test, model, expectation.delete_status_code)


def check_get_list_permissions(
    api_test: ApiTest,
    model: Model,
    expected_status_code: Optional[int] = None,
    expected_number_of_returned_elements: Optional[int] = None,
):
    list_url = list_url_for_model(model)
    response = None

    if expected_status_code:
        response = api_test.get_returns_status_code(list_url, expected_status_code)
    elif expected_number_of_returned_elements:
        response = api_test.get_successful(list_url)

    if expected_number_of_returned_elements and response:
        if len(response["results"]) != expected_number_of_returned_elements:
            LOGGER.debug(
                f"Expected {expected_number_of_returned_elements} but got {len(response['results'])}"
            )

        assert len(response["results"]) == expected_number_of_returned_elements


def check_get_detail_permissions(
    api_test: ApiTest,
    model: Model,
    expected_status_code: int,
):
    detail_url = detail_url_for_model(model)
    api_test.get_returns_status_code(detail_url, expected_status_code)


def check_post_permissions(
    api_test: ApiTest,
    model: Model,
    expected_status_code: int,
    post_parameter: AnyDict = {},
):
    list_url = list_url_for_model(model)
    api_test.post_returns_status_code(list_url, expected_status_code, post_parameter)


def check_put_permissions(
    api_test: ApiTest,
    model: Model,
    expected_status_code: int,
    put_parameter: AnyDict = {},
):
    detail_url = detail_url_for_model(model)
    api_test.put_returns_status_code(detail_url, expected_status_code, put_parameter)


def check_patch_permissions(
    api_test: ApiTest,
    model: Model,
    expected_status_code: int,
    patch_parameter: AnyDict = {},
):
    detail_url = detail_url_for_model(model)
    api_test.patch_returns_status_code(
        detail_url, expected_status_code, patch_parameter
    )


def check_delete_permissions(
    api_test: ApiTest,
    model: Model,
    expected_status_code: int,
):
    detail_url = detail_url_for_model(model)
    api_test.delete_returns_status_code(detail_url, expected_status_code)
