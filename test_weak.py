from weak import make_request


def test_data():
    response = make_request()
    assert response.a == 1
    assert response.b == 2
    assert response.customer.name == "Erik"
    assert response.customer.email == "erik@example.com"

def test_accessed():
    response = make_request()
    assert response._accessed['a'] == False
    response.a
    assert response._accessed['a'] == True

    assert response._accessed['customer'] == False
    response.customer.name
    assert response._accessed['customer'] == True
    assert response.customer._accessed['name'] == True
