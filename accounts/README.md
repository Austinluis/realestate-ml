# Accounts App

This Django app owns authentication and dashboard-related user flows.

## Responsibilities

- Defines the custom `User` model in `models.py`.
- Uses email as the login identifier through `USERNAME_FIELD = 'email'`.
- Provides registration, login, logout, and dashboard views in `views.py`.
- Provides API endpoints for register, login, logout, and profile in `api_views.py`.
- Stores form definitions in `forms.py`.
- Serializes users for API responses in `serializers.py`.
- Registers the custom user model in Django admin through `admin.py`.
- Contains auth/dashboard tests in `tests.py`.

## URL Files

- `urls.py`: account pages and account API routes.
- `urls_dashboard.py`: dashboard route mounted at `/dashboard/`.
