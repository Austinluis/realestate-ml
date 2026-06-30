# Properties App

This Django app manages real estate listings owned by users.

## Responsibilities

- Defines the `Property` model in `models.py`.
- Stores property details such as location, area, bedrooms, bathrooms, stories, amenities, furnishing status, listed price, and uploaded photo.
- Provides HTML CRUD views in `views.py`.
- Provides REST API endpoints in `api_views.py`.
- Serializes properties in `serializers.py`.
- Registers properties in Django admin through `admin.py`.
- Contains property ownership and CRUD tests in `tests.py`.

## Important Behavior

All property views and APIs are scoped to the logged-in user. Users should only see, edit, or delete their own property records.
