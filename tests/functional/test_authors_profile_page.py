import pytest
from data import authors


@pytest.mark.parametrize(
    "label",
    [
        b"Amount of publications",
        b"Number of citations",
        b"H-index",
        b"Research beginning year",
    ],
)
def test_author_info(test_client, label):
    response = test_client.get("/author_id=57186538600")
    assert response.status_code == 200
    assert label in response.data


@pytest.mark.parametrize(
    "parameter",
    [
        "papers_number",
        "overall_citation",
        "hirsch_ind",
    ],
)
def test_author_data_error(test_client, parameter):
    with pytest.raises(AssertionError):
        response = test_client.get("/author_id=57186538600")
        author = authors.set_index("id")
        author = author.loc[57186538600]
        assert response.status_code == 200
        assert bytes(author[parameter]) in response.data
