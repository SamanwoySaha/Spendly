# Spec: Login and Logout

## Overview
Implement credential-based login and session-clearing logout so registered
users can authenticate and sign out of Spendly. This step wires up
`POST /login` (currently `GET`-only) and converts the `GET /logout` stub
into a real route. It also makes the navbar session-aware so the UI reflects
whether the user is signed in.

## Depends on
- Step 01 — Database Setup (`get_db()`, `users` table)
- Step 02 — Registration (`get_user_by_email()`, `create_user()`, session
  variables `user_id` and `user_name`)

## Routes
- `POST /login` — validate email + password, set session, redirect to `/` — public
- `GET /logout` — clear session, redirect to `/` — logged-in (no hard auth
  guard needed at this step; simply clearing the session is sufficient)

The existing `GET /login` route is upgraded to accept `POST` as well (same
function, same decorator with `methods=["GET", "POST"]`).

## Database changes
No new tables or columns. No new helper functions — `get_user_by_email()`
already exists in `database/db.py` and returns a `sqlite3.Row` with all
user columns including `password_hash`.

## Templates
- **Modify:** `templates/login.html`
  - Change `action="/login"` to `action="{{ url_for('login') }}"`
- **Modify:** `templates/base.html`
  - Make `nav-links` section conditional on `session.get('user_id')`:
    - **Logged-out:** show "Sign in" and "Get started" links (current state)
    - **Logged-in:** show the user's name and a "Sign out" link pointing to
      `url_for('logout')`

## Files to change
- `app.py` — upgrade `/login` to handle `POST`; implement `/logout`; import
  `check_password_hash` from `werkzeug.security`
- `templates/login.html` — fix hardcoded form `action`
- `templates/base.html` — add session-aware nav

## Files to create
None.

## New dependencies
No new dependencies. `werkzeug.security.check_password_hash` is already
available (werkzeug is installed).

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never f-strings in SQL
- Passwords verified with `werkzeug.security.check_password_hash` — never
  compare plaintext
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Use `abort()` for HTTP errors, not bare string returns
- On bad credentials (wrong email **or** wrong password), re-render
  `login.html` with `error="Invalid email or password."` — do **not**
  distinguish which field was wrong (prevents user enumeration)
- On missing fields, re-render `login.html` with
  `error="Email and password are required."`
- On success, store `session['user_id']` and `session['user_name']` then
  redirect to `url_for('landing')`
- Logout must call `session.clear()` (not `session.pop`) then redirect to
  `url_for('landing')`
- The navbar "Sign out" link must use `url_for('logout')`, not a hardcoded URL

## Definition of done
- [ ] `POST /login` with valid credentials sets `session['user_id']` and
  redirects to `/`
- [ ] `POST /login` with unknown email re-renders the form with error message
- [ ] `POST /login` with wrong password re-renders the form with error message
- [ ] `POST /login` with missing fields re-renders the form with error message
- [ ] Error message does not reveal whether the email exists
- [ ] `GET /logout` clears the session and redirects to `/`
- [ ] After logout, `session['user_id']` is no longer set
- [ ] Navbar shows "Sign in" / "Get started" when logged out
- [ ] Navbar shows user name and "Sign out" when logged in
- [ ] `login.html` form `action` uses `url_for('login')`, not a hardcoded URL
- [ ] `GET /login` still renders the form unchanged
