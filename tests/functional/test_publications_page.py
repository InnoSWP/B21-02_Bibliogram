import pytest


from app import bibliometrics




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
    bibliometrics.test_client().post("/publications/page=1", data={"sort": sort_type})


    response = bibliometrics.test_client().get("/publications/page=1")


    assert bytes(sort_type, "utf-8") in response.data




@pytest.mark.parametrize(


    "filtration",


    [


        ["Publication Date", "Quartile", "Citations", "Work Type", "Source Type"],


        ["Publication Date", "Quartile", "Citations", "Work Type", "Source Type"],


    ],
)


def test_publications_filtration(test_client, filtration):
    bibliometrics.test_client().post("/publications/page=2", data={"show": filtration})


    response = bibliometrics.test_client().get("/publications/page=2")


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
    bibliometrics.test_client().post("/publications/page=3", data={"show": filtration})


    response = bibliometrics.test_client().get("/publications/page=3")


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
    bibliometrics.test_client().post("/publications/page=4", data={"download": file_type})


    response = bibliometrics.test_client().get("/publications/page=4")


    assert bytes(file_type.lower(), "utf-8") in response.data


