import unittest
from app import app

class CreatureTypeGeneratorTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_main_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Creature Type Generator', response.data)

    def test_generate_creature(self):
        response = self.client.get('/api/generate')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('creature_type', data)
        self.assertIn('history', data)
        self.assertIn(data['creature_type'], data['history'])

    def test_reset_history(self):
        # Generate a creature to add to history
        self.client.get('/api/generate')
        # Reset history
        response = self.client.post('/api/reset')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        # Check that history is empty
        response = self.client.get('/api/generate')
        data = response.get_json()
        self.assertEqual(len(data['history']), 1)  # Only the new one

    def test_error_handler(self):
        # Simulate a 500 error by patching an endpoint if needed
        pass  # Implement if you have custom error triggers

if __name__ == '__main__':
    unittest.main()