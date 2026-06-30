from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from accounts.models import User
from properties.models import Property
from predictions.models import Prediction


def make_user(username='preduser', email='pred@example.com', password='TestPass123!'):
    return User.objects.create_user(username=username, email=email, password=password)


def make_property(owner):
    return Property.objects.create(
        owner=owner, title='Test House', location='Lagos',
        area=2000, bedrooms=3, bathrooms=2, stories=1,
        mainroad='yes', guestroom='no', basement='no',
        hotwaterheating='no', airconditioning='yes',
        parking=1, prefarea='no', furnishingstatus='furnished',
    )


VALID_PAYLOAD = {
    'area': '2000', 'bedrooms': '3', 'bathrooms': '2',
    'stories': '1', 'mainroad': 'yes', 'guestroom': 'no',
    'basement': 'no', 'hotwaterheating': 'no', 'airconditioning': 'yes',
    'parking': '1', 'prefarea': 'no', 'furnishingstatus': 'furnished',
}


class PredictViewTest(TestCase):

    def setUp(self):
        self.user = make_user()
        self.client.login(username='pred@example.com', password='TestPass123!')

    def test_predict_page_loads(self):
        """Prediction form page returns 200 for authenticated users."""
        response = self.client.get(reverse('predict'))
        self.assertEqual(response.status_code, 200)

    def test_predict_requires_login(self):
        """Unauthenticated users are redirected to login."""
        self.client.logout()
        response = self.client.get(reverse('predict'))
        self.assertEqual(response.status_code, 302)

    @patch('predictions.views.predict_price', return_value=4500000.0)
    def test_predict_valid_input_returns_json(self, mock_predict):
        """Valid POST returns JSON with predicted_price key."""
        import json
        response = self.client.post(
            reverse('predict'),
            data=json.dumps(VALID_PAYLOAD),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('predicted_price', data)
        self.assertEqual(data['predicted_price'], 4500000.0)

    @patch('predictions.views.predict_price', return_value=4500000.0)
    def test_predict_saves_to_db(self, mock_predict):
        """A valid prediction call creates a Prediction record in the database."""
        import json
        self.client.post(
            reverse('predict'),
            data=json.dumps(VALID_PAYLOAD),
            content_type='application/json'
        )
        self.assertEqual(Prediction.objects.filter(user=self.user).count(), 1)
        pred = Prediction.objects.get(user=self.user)
        self.assertEqual(pred.predicted_price, 4500000.0)

    @patch('predictions.views.predict_price', return_value=3200000.0)
    def test_predict_with_linked_property(self, mock_predict):
        """Prediction linked to a property stores the property FK correctly."""
        import json
        prop = make_property(self.user)
        payload = {**VALID_PAYLOAD, 'property_id': str(prop.pk)}
        self.client.post(
            reverse('predict'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        pred = Prediction.objects.get(user=self.user)
        self.assertEqual(pred.property, prop)

    def test_prediction_history_requires_login(self):
        """Unauthenticated users cannot access prediction history."""
        self.client.logout()
        response = self.client.get(reverse('prediction_history'))
        self.assertEqual(response.status_code, 302)

    @patch('predictions.views.predict_price', return_value=5000000.0)
    def test_prediction_history_shows_only_user_predictions(self, mock_predict):
        """A user only sees their own prediction history."""
        import json
        # Create a second user and their prediction
        other_user = make_user('other', 'other@example.com')
        Prediction.objects.create(
            user=other_user, predicted_price=9999999.0,
            area=5000, bedrooms=5, bathrooms=3, stories=2,
            mainroad='yes', guestroom='yes', basement='no',
            hotwaterheating='no', airconditioning='yes',
            parking=2, prefarea='yes', furnishingstatus='furnished',
        )
        # Make a prediction as the logged-in user
        self.client.post(
            reverse('predict'),
            data=json.dumps(VALID_PAYLOAD),
            content_type='application/json'
        )
        response = self.client.get(reverse('prediction_history'))
        self.assertEqual(response.status_code, 200)
        # Should not see the other user's prediction price
        self.assertNotContains(response, '9999999')


class PredictInvalidInputTest(TestCase):

    def setUp(self):
        self.user = make_user()
        self.client.login(username='pred@example.com', password='TestPass123!')

    @patch('predictions.views.predict_price', side_effect=ValueError('Invalid input'))
    def test_predict_invalid_type_returns_error(self, mock_predict):
        """When predict_price raises, the view returns a 500 JSON error."""
        import json
        payload = {**VALID_PAYLOAD, 'area': 'not-a-number'}
        response = self.client.post(
            reverse('predict'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', response.json())
