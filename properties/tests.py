from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from properties.models import Property


def make_user(username='user1', email='user1@example.com', password='TestPass123!'):
    return User.objects.create_user(username=username, email=email, password=password)


def make_property(owner, title='Test House', location='Lagos'):
    return Property.objects.create(
        owner=owner,
        title=title,
        location=location,
        area=2000,
        bedrooms=3,
        bathrooms=2,
        stories=1,
        mainroad='yes',
        guestroom='no',
        basement='no',
        hotwaterheating='no',
        airconditioning='yes',
        parking=1,
        prefarea='no',
        furnishingstatus='furnished',
    )


class PropertyAddTest(TestCase):

    def setUp(self):
        self.user = make_user()
        self.client.login(username='user1@example.com', password='TestPass123!')

    def test_add_property_valid(self):
        """Valid property data saves a record to the database."""
        response = self.client.post(reverse('property_add'), {
            'title': 'New Property',
            'location': 'Abuja',
            'area': 1500,
            'bedrooms': 2,
            'bathrooms': 1,
            'stories': 1,
            'mainroad': 'no',
            'guestroom': 'no',
            'basement': 'no',
            'hotwaterheating': 'no',
            'airconditioning': 'no',
            'parking': 0,
            'prefarea': 'no',
            'furnishingstatus': 'unfurnished',
        })
        self.assertEqual(Property.objects.filter(owner=self.user).count(), 1)
        self.assertRedirects(response, reverse('property_list'))

    def test_add_property_missing_area(self):
        """Missing area field returns a form error."""
        response = self.client.post(reverse('property_add'), {
            'title': 'No Area Property',
            'location': 'Lagos',
            # area intentionally omitted
            'bedrooms': 2,
            'bathrooms': 1,
            'stories': 1,
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Property.objects.count(), 0)

    def test_property_list_requires_login(self):
        """Unauthenticated request to property list redirects to login."""
        self.client.logout()
        response = self.client.get(reverse('property_list'))
        self.assertEqual(response.status_code, 302)


class PropertyOwnershipTest(TestCase):

    def setUp(self):
        self.user_a = make_user('userA', 'a@example.com')
        self.user_b = make_user('userB', 'b@example.com')
        self.prop_a = make_property(self.user_a, title='A House')

    def test_property_list_only_shows_user_properties(self):
        """User B cannot see User A's properties in the list."""
        self.client.login(username='b@example.com', password='TestPass123!')
        response = self.client.get(reverse('property_list'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'A House')

    def test_delete_requires_ownership(self):
        """User B cannot delete User A's property (returns 404)."""
        self.client.login(username='b@example.com', password='TestPass123!')
        response = self.client.post(reverse('property_delete', args=[self.prop_a.pk]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Property.objects.filter(pk=self.prop_a.pk).exists())

    def test_edit_requires_ownership(self):
        """User B cannot edit User A's property (returns 404)."""
        self.client.login(username='b@example.com', password='TestPass123!')
        response = self.client.get(reverse('property_edit', args=[self.prop_a.pk]))
        self.assertEqual(response.status_code, 404)
