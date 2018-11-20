from .client import client


def add_post(client, endpoint, data):
    client.post(endpoint, json=data)


def add_multiple_posts(client, count=10, endpoint='/chosnale/', key="chosnale"):
    import os
    for _ in list(range(count)):
        add_post(client=client,
                 endpoint=endpoint,
                 data={key: str(os.urandom(30))})


def test_index(client):
    res = client.get("/")
    assert res.status == "200 OK"
    res = client.get("/chosnale/")
    assert res.status == "200 OK"
    res = client.get("/chosnale/")
    assert res.status == "200 OK"


def test_empty_db(client):
    res = client.get('/')
    res = res.get_json()
    assert res['result']['data'] == []


def test_add_chosnale(client):
    res = client.post('/chosnale/', json={"chosnale": "test string with atleast"\
                                          "15 charachters in it's body"})
    assert res.status == "201 CREATED"
    res = res.get_json()
    assert "chosnale saved successfully" in res['result']


def test_add_short_chosnale(client):
    import os
    res = client.post('/chosnale/', json={"chosnale": "short text"})
    assert res.status == "400 BAD REQUEST"
    res = res.get_json()
    assert "your chosnale should be atleast 15 chars long" in res['result']


def test_add_long_chosnale(client):
    import os
    res = client.post('/chosnale/', json={"chosnale": str(os.urandom(241))})
    assert res.status == "400 BAD REQUEST"
    res = res.get_json()
    assert "your chosnale should be 240 chars long" in res['result']


def test_add_missing_chosnale(client):
    res = client.post('/chosnale/', json={})
    assert res.status == "400 BAD REQUEST"
    res = res.get_json()
    assert "you should provide a `chosnale` field." in res['result']


def test_pagination(client):
    add_multiple_posts(client=client, count=15)
    res = client.get('/chosnale/?page=2')
    res = res.get_json()
    assert res['result']['page'] == '2'
