def test_filtration(test_client):
    test_client().post("/publications", data={"sort": "Publication Date"})
