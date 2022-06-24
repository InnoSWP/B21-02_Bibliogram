from app.data import uni


def test_main_page_info(test_client):
    """
    :param test_client:
    :return:
    """
    response = test_client.get("/")
    assert response.status_code == 200
    assert b"Amount of publications" in response.data
    assert b"Number of researchers" in response.data
    assert b"Publications per person" in response.data
    assert b"Citations per person" in response.data


def test_main_page_gen_stat(test_client):
    """
    :param test_client:
    :return:
    """

    uni.num_researchers = 1457
    uni.num_publications = 800000
    uni.cit_per_person = 1000000
    uni.public_per_person = 7005003

    response = test_client.get("/")
    assert response.status_code == 200
    assert b"1457" in response.data
    assert b"800000" in response.data
    assert b"1000000" in response.data
    assert b"7005003" in response.data
