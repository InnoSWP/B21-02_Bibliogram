import pytest
from data import uni


@pytest.mark.parametrize(
    "label",
    [
        b"Amount of publications",
        b"Number of researchers",
        b"Publications per person",
        b"Citations per person",
        b"Innopolis University",
    ]
)
def test_main_page_gen_stat(test_client, label):
    response = test_client.get("/")
    assert response.status_code == 200
    assert label in response.data


@pytest.mark.parametrize(
    "uni_parameter",
    [
        b"1457",
        b"800000",
        b"1000000",
        b"7005003",
    ]
)
def test_main_page_gen_stat_content(test_client, uni_parameter):
    uni.num_researchers = 1457
    uni.num_publications = 800000
    uni.public_per_person = 1000000
    uni.cit_per_person = 7005003

    response = test_client.get("/")
    assert response.status_code == 200
    assert uni_parameter in response.data


@pytest.mark.parametrize(
    "label",
    [
        b"Explore the statistics of the Innopolis University",
        b"Monitor the progress of the IU in the research activities",
        b"What to see here?",
        b"Explore the statistics of a particular researcher",
        b"Explore the information about publications",
    ]
)
def test_main_page_info(test_client, label):
    response = test_client.get("/")
    assert response.status_code == 200
    assert label in response.data


@pytest.mark.parametrize(
    "label",
    [
        b"Explore the statistics of the Innopolis University",
        b"Monitor the progress of the IU in the research activities",
        b"What to see here?",
        b"Explore the statistics of a particular researcher",
        b"Explore the information about publications",
    ]
)
def test_main_page_error(test_client, label):
    response = test_client.post("/")
    assert response.status_code == 405
    assert label not in response.data
