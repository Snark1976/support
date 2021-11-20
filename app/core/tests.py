from rest_framework import status
from rest_framework.test import APITestCase


class SupportTestCase(APITestCase):

    def setUp(self):
        self.user = self.client.post('/auth/users/', data={'username': 'user', 'password': 'user_password'})
        response = self.client.post('/auth/jwt/create/', data={'username': 'user', 'password': 'user_password'})
        self.token = response.data['access']
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_get_tickets_list(self):
        response = self.client.get('/api/tickets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_tickets_list_anonymous(self):
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/tickets/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_tickets(self):
        response = self.client.post('/api/tickets/', format='json', data={
            "new_ticket": {
                "title_ticket": "New ticket",
                "text": "Message"
            }
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_message(self):
        self.client.post('/api/tickets/', format='json', data={
            "new_ticket": {
                "title_ticket": "New ticket",
                "text": "Message"
            }
        })
        response = self.client.post('/api/tickets/1/', format='json', data={
            "new_message": {
                "text": "clarification"
            }
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
