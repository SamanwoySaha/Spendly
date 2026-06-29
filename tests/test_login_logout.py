def _login(client, email, password):
    return client.post("/login", data={"email": email, "password": password})


# ---------------------------------------------------------------------------
# POST /login — success
# ---------------------------------------------------------------------------

def test_login_valid_credentials_sets_session(client, registered_user):
    _login(client, registered_user["email"], registered_user["password"])
    with client.session_transaction() as sess:
        assert sess["user_id"] == registered_user["id"]
        assert sess["user_name"] == registered_user["name"]


def test_login_valid_credentials_redirects_to_landing(client, registered_user):
    resp = _login(client, registered_user["email"], registered_user["password"])
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/")


# ---------------------------------------------------------------------------
# POST /login — failure paths
# ---------------------------------------------------------------------------

def test_login_unknown_email_shows_error(client):
    resp = _login(client, "nobody@example.com", "password123")
    assert resp.status_code == 200
    assert b"Invalid email or password." in resp.data


def test_login_wrong_password_shows_error(client, registered_user):
    resp = _login(client, registered_user["email"], "wrongpassword")
    assert resp.status_code == 200
    assert b"Invalid email or password." in resp.data


def test_login_missing_email_shows_error(client):
    resp = client.post("/login", data={"email": "", "password": "password123"})
    assert b"Email and password are required." in resp.data


def test_login_missing_password_shows_error(client):
    resp = client.post("/login", data={"email": "test@example.com", "password": ""})
    assert b"Email and password are required." in resp.data


def test_login_missing_both_fields_shows_error(client):
    resp = client.post("/login", data={"email": "", "password": ""})
    assert b"Email and password are required." in resp.data


# ---------------------------------------------------------------------------
# User enumeration prevention
# ---------------------------------------------------------------------------

def test_login_error_message_same_for_bad_email_and_bad_password(client, registered_user):
    resp_bad_email = _login(client, "nobody@example.com", "password123")
    resp_bad_password = _login(client, registered_user["email"], "wrongpassword")
    assert b"Invalid email or password." in resp_bad_email.data
    assert b"Invalid email or password." in resp_bad_password.data
    # Neither response should reveal which field was wrong
    assert b"email" not in resp_bad_email.data.lower().split(b"invalid email or password.")[1][:50]


# ---------------------------------------------------------------------------
# GET /logout
# ---------------------------------------------------------------------------

def test_logout_clears_session(client, registered_user):
    _login(client, registered_user["email"], registered_user["password"])
    client.get("/logout")
    with client.session_transaction() as sess:
        assert "user_id" not in sess


def test_logout_redirects_to_landing(client, registered_user):
    _login(client, registered_user["email"], registered_user["password"])
    resp = client.get("/logout")
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/")


def test_logout_when_already_logged_out_is_safe(client):
    resp = client.get("/logout")
    assert resp.status_code == 302


# ---------------------------------------------------------------------------
# GET /login — unchanged behaviour
# ---------------------------------------------------------------------------

def test_login_get_renders_form(client):
    resp = client.get("/login")
    assert resp.status_code == 200
    assert b"<form" in resp.data
    assert b"auth-error" not in resp.data


def test_login_form_action_uses_url_for(client):
    resp = client.get("/login")
    assert b'action="/login"' in resp.data


# ---------------------------------------------------------------------------
# Navbar session awareness
# ---------------------------------------------------------------------------

def test_navbar_shows_signin_when_logged_out(client):
    resp = client.get("/")
    assert b"Sign in" in resp.data
    assert b"Get started" in resp.data
    assert b"Sign out" not in resp.data


def test_navbar_shows_username_when_logged_in(client, registered_user):
    _login(client, registered_user["email"], registered_user["password"])
    resp = client.get("/")
    assert b"Sign out" in resp.data
    assert registered_user["name"].encode() in resp.data
    assert b'class="nav-user-name"' in resp.data
