
def test_user_signup(client, user_in, user_out, user_access_token):
    response = client.post(url="/admin/user/signup", json=user_in, headers={'Authorization': f'Bearer {user_access_token}'})
    assert response.status_code == 201
    res = response.json()
    res["password"] = "string"
    res["id"] = user_out["id"]
    assert res == user_out
    

def test_read_all_users(client, user_access_token):
    response = client.get(url="/users/get_users", headers={'Authorization': f'Bearer {user_access_token}'})
    assert response.status_code == 200


def test_get_user_by_email(client, user_in, user_access_token):
    email = user_in['email']
    response = client.get(url=f'/users/{email}/get_user/', headers={'Authorization': f'Bearer {user_access_token}'} )
    assert response.status_code == 200
    assert response.json()['email'] == email


def test_create_entry_for_user(client, entry_in, entry_out, user_access_token):
    response = client.post(url="/users/me/new_entry/", json=entry_in, headers={'Authorization': f'Bearer {user_access_token}'})
    assert response.status_code == 201
    res = response.json()
    entry_out["id"] = res["id"]
    entry_out["entry_date"] = res["entry_date"]
    entry_out['period_id'] = res['period_id']
    entry_out['owner_id'] = res['owner_id']
    assert res == entry_out


def test_get_entries_me(client, user_access_token):
    response = client.get(url="/entries/show_entries_me", headers={'Authorization': f'Bearer {user_access_token}'})
    assert response.status_code == 200


def test_set_user_active_level(client, user_in, user_access_token):
    email = user_in['email']
    id = client.get(url=f'/users/{email}/get_user/', headers={'Authorization': f'Bearer {user_access_token}'}).json()['id']
    response = client.patch(url=f'/admin/user/{id}/set_user_active_level',headers={'Authorization': f'Bearer {user_access_token}'})
    assert response.status_code == 201


def test_create_entry_for_in_active_user(client, entry_in, user_access_token):
    response = client.post(url="/users/me/new_entry/", json=entry_in, headers={'Authorization': f'Bearer {user_access_token}'})
    assert response.status_code == 400


def test_set_super_user(client, user_in, user_access_token):
    email = user_in['email']
    id = client.get(url=f'/users/{email}/get_user/', headers={'Authorization': f'Bearer {user_access_token}'}).json()['id']
    response = client.patch(url=f'/admin/users/{id}/set_super_user', headers={'Authorization': f'Bearer {user_access_token}'})   
    assert response.status_code == 200
    assert response.json()['super_user'] is True 


def test_create_period(client, user_access_token):
    stub = {
        'nr': 1000,
        'start_date': '1971-07-19',
        'end_date': '1971-07-20'
    }
    response = client.post(url="/admin/period/create_periods", json=stub, headers={'Authorization': f'Bearer {user_access_token}'})
    assert response.status_code == 201


def test_update_period(client, user_access_token):
    stub = {
        'nr': 1000,
        'start_date': '1971-07-19',
        'end_date': '2023-11-15'
    }
    response = client.put(url="/admin/period/update_period", json=stub, headers={'Authorization': f'Bearer {user_access_token}'})
    assert response.status_code == 201
    assert response.json()['nr'] == stub['nr']
    

def test_delete_period(client, user_access_token):
    nr = 1000
    response = client.delete(url=f"/admin/period/{nr}/delete_period", headers={'Authorization': f'Bearer {user_access_token}'})
    assert response.status_code == 200


def test_create_fixed_entry(client, user_access_token):
    stub = {
        "amount": 216.67,
        "description": "test",
        "interval": "Monthly",
        "supplier": "pytest",
        "title": "test",
        "url": "pytest.org"
    }
    response = client.post(
        url='/admin/fixed_entries/create_fixed_entry', 
        headers={'Authorization': f'Bearer {user_access_token}'}, 
        json=stub 
        )
    assert response.status_code == 201
    with open("fixed_entries.jsonl", 'r+') as fp:
    # read an store all lines into list
        lines = fp.readlines()
        fp.seek(0)
        fp.truncate()
        fp.writelines(lines[:-1])


def test_load_fixeds_for_period(client, user_access_token): 
    ...

def test_remove_entry(client, user_access_token):
    id = client.get(url="/entries/get_last_entry", headers={'Authorization': f'Bearer {user_access_token}'}).json()["id"]
    response = client.delete(url=f"/admin/entries/{id}/delete_entry", headers={'Authorization': f'Bearer {user_access_token}'})
    assert response.status_code == 200

def test_remove_user(client, user_in, user_access_token):
    email = user_in['email']
    id = client.get(url=f'/users/{email}/get_user/', headers={'Authorization': f'Bearer {user_access_token}'}).json()['id']
    response = client.delete(url=f'/admin/user/{id}/delete_user/', headers={'Authorization': f'Bearer {user_access_token}'})
    assert response.status_code == 200
