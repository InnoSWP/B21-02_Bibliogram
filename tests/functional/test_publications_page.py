import pytest
from app import app


@pytest.mark.parametrize(
    "sort_type",
    [
        "Publication Date",
        "Quartile",
        "Title",
        "Citations",
        "Work Type",
        "Source Type",
    ],
)
def test_publications_sorting(test_client, sort_type):
    app.test_client().post(
        "/publications/page=1", data={"sort": sort_type}
    )
    response = app.test_client().get("/publications/page=1")
    assert bytes(sort_type, "utf-8") in response.data


@pytest.mark.parametrize(
    "filtration",
    [
        ["Publication Date", "Quartile", "Citations", "Work Type", "Source Type"],
        ["Publication Date", "Quartile", "Citations", "Work Type", "Source Type"],
    ],
)
def test_publications_filtration(test_client, filtration):
    app.test_client().post("/publications/page=1", data={"show": filtration})
    response = app.test_client().get("/publications/page=1")
    assert b"Quartile" in response.data
    assert b"Citations" in response.data


@pytest.mark.parametrize(
    "filtration",
    [
        ["Publication Date", "Quartile", "Citations", "Work Type", "Source Type"],
        ["Publication Date", "Quartile", "Citations", "Work Type", "Source Type"],
    ],
)
def test_publications_filtration_error(test_client, filtration):
    app.test_client().post("/publications/page=1", data={"show": filtration})
    response = app.test_client().get("/publications/page=1")
    with pytest.raises(AssertionError):
        assert b"Affiliation" not in response.data
        assert b"DOI" not in response.data


@pytest.mark.parametrize(
    "file_type",
    [
        "CSV",
        "TSV",
        "JSON",
        "XLSX",
    ],
)
def test_publications_downloading(test_client, file_type):
    app.test_client().post(
        "/publications/page=1", data={"download": file_type}
    )
    response = app.test_client().get("/publications/page=1")
    assert bytes(file_type.lower(), "utf-8") in response.data
