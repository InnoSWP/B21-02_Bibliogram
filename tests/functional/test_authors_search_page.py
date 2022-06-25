import pytest


@pytest.mark.parametrize(
    "label",
    [
        b"Find author",
        b"Search results",
    ]
)
def test_coauthors_info(test_client, label):
    response = test_client.get("/search")
    assert response.status_code == 200
    assert label in response.data


@pytest.mark.parametrize(
    "name",
    [
        "Marat Mingazov",
        "Maksim Rassabin",
        "Mohamad Kassab",
        "Adil Mehood Khan",
    ]
)
def test_coauthors_data(test_client, name):
    response = test_client.post("/search", data={"author": name})
    assert response.status_code == 200
    assert bytes(name, "utf-8") in response.data
