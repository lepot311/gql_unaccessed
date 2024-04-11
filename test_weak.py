from weak import make_request


def test_data():
    '''
    Access to GQL data through nested namespaces.
    '''
    response = make_request()
    assert response.a == 1
    assert response.b == 2
    assert response.customer.name == "Erik"
    assert response.customer.email == "erik@example.com"

def test_accessed_first_level():
    '''
    Accessing first-level data results in access dict being updated.
    '''
    response = make_request()
    assert response._accessed['a'] == False

    response.a

    assert response._accessed['a'] == True

def test_accessed_first_level_decendants():
    '''
    Accessing a nested namespace causes it to be marked as accessed,
    but not its decendants.
    '''
    response = make_request()
    assert response._accessed['customer'] == False

    response.customer

    assert response._accessed['customer'] == True
    assert response.customer._accessed['name'] == False

def test_accessed_second_level():
    '''
    Accessing a nested namespace's decendant causes both it and its parent to be
    marked as accessed.
    '''
    response = make_request()
    assert response._accessed['customer'] == False
    assert response.customer._accessed['name'] == False

    response.customer.name

    assert response._accessed['customer'] == True
    assert response.customer._accessed['name'] == True
