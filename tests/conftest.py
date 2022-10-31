import pytest


from app import bibliometrics




@pytest.fixture(scope="module")


def test_client():


    with bibliometrics.test_client() as testing_client:


        with bibliometrics.app_context():


            yield testing_client


