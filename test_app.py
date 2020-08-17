from unittest import TestCase
from app import app
from flask import session

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class RedirectTestCase(TestCase):

    def test_redirect_selected(self): # will not need SET
        with app.test_client() as client:
            resp = client.get("/selected")

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "http://localhost/survey")

    def test_redirection_followed_selected(self):
        with app.test_client() as client:
            data = {'selected': 'personality'}
            resp = client.post('/selected', data = data, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)

    def test_redirection_responses(self):
        with app.test_client() as client:
            resp = client.get('/responses')

            self.assertEqual(resp.status_code, 302)

    def test_redirection_followed_responses(self):
        with app.test_client() as client:
            data = {'selected': 'personality'}
            client.post('/selected', data = data, follow_redirects=True)
            resp = client.get('/responses', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)

    def test_redirect_complete(self):
        with app.test_client() as client:
            resp = client.get('/complete')

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "http://localhost/")


class SurveySubmitCase(TestCase):

    def test_survey_submit(self):
        with app.test_client() as client:
            data = {'selected': 'personality'}
            resp = client.post('/selected', data = data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertIn('personality', html)

    def test_answer_submit(self):
        with app.test_client() as client:
            data = {'selected': 'personality'}
            client.post('/selected', data = data)
            data = {'answer': 'Yes'}
            client.post('/responses')
            client.post('/answer', data = data)
            self.assertEqual(session['responses'], ['Yes'])

class SessionTestCase(TestCase):

    def test_survey_select_session(self):
        with app.test_client() as client:
            data = {'selected': 'personality'}
            client.post('/selected', data = data)
            self.assertEqual(session['selected'], 'personality')

    def test_clear_session(self):
        with app.test_client() as client:
            data = {'selected': 'personality'}
            client.post('/selected', data = data)
            client.post('/responses')
            data = {'answer': 'Yes'}
            client.post('/answer', data = data)
            client.get('/complete')
            self.assertEqual(session['selected'], "")
            self.assertEqual(session['responses'], [])
