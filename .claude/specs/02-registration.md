# Spec: Registration

## Overview
Implement user registration so new visitors can create a Spendly account.
This step wires up the `POST /register` route, adds two DB helpers for
looking up and inserting users, and sets up Flask's session so the user is
automatically logged in after a successful sign-up.

## Depends on
- Step 01 — Database Setup (`get_db()`, `init_db()`, `users` table)

## Routes
- `POST /register` — validate form data, hash password, insert user, start
  session, redirect to `/` — public

The existing `GET /register` route remains unchanged (renders `register.html`).

## Database changes
No new tables or columns. Two new helper functions are added to
`database/db.py`:

- `get_user_by_email(email)` — returns a `sqlite3.Row` or `None`
- `create_user(name, email, password)` — hashes the password with
  `werkzeug.security.generate_password_hash`, inserts the row, returns the
  new `user_id`

## Templates
- **Modify:** `templates/register.html`
  - Change the form `action` from the hardcoded string `/register` to
    `{{ url_for('register') }}`

## Files to change
- `app.py` — add `POST` to the `register` route, import `session` from
  flask, set `app.secret_key`, implement registration logic
- `database/db.py` — add `get_user_by_email()` and `create_user()`
- `templates/register.html` — fix hardcoded form action URL

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never f-strings in SQL
- Passwords hashed with `werkzeug.security.generate_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Use `abort()` for HTTP errors, not bare string returns
- `secret_key` must be set on `app` before session can be used; use a
  hard-coded dev string for now (e.g. `"dev-secret-change-in-prod"`)
- After successful registration, store `user_id` and `user_name` in
  `flask.session` and redirect to `url_for('landing')`
- On duplicate email, re-render `register.html` with
  `error="An account with that email already exists."`
- On missing/short fields, re-render with a descriptive `error` string
- Password minimum length: 8 characters — validate server-side

## Definition of done
- [ ] Submitting the form with valid data creates a new row in `users`
- [ ] Password is stored as a hash, never plaintext
- [ ] Duplicate email submission re-renders the form with an error message
- [ ] Password shorter than 8 characters re-renders the form with an error
- [ ] Missing name or email re-renders the form with an error
- [ ] After successful registration, `session['user_id']` is set
- [ ] After successful registration, the browser is redirected to `/`
- [ ] `GET /register` still works and renders the form
- [ ] Form `action` uses `url_for('register')`, not a hardcoded URL
