import pytest


@pytest.mark.parametrize(
    "label",
    [
        b"Author",
        b"Quantity of publications",
        b"Affiliation",
        b"Vladimir Ivanov",
        b"Peter Johnson",
        b"Caleb Blackgate",
        b"Alexey Petrov",
    ],
)
def test_coauthors_info(test_client, label):
    response = test_client.get("/co-author=57186538600")
    assert response.status_code == 200
    assert label in response.data
