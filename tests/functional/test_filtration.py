from app import app


def test_filtration(test_client):
    app.test_client().post("/publications", data={"sort": "Publication Date"})
    response = test_client.get("/publications")
    assert b"Publication Date" in response.data
