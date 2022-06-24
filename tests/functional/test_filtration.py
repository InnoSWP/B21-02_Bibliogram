def test_filtration(test_client):
    test_client().post("/publications", data={"sort": "Publication Date"})
    response = test_client.get("/publications")
    assert  b"Publication Date" in response
