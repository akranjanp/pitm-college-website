from django.test import TestCase
from django.urls import reverse
from website.models import ContactMessage, Course, Notice, GalleryImage, FacultyMember

class WebsitePagesTestCase(TestCase):
    def setUp(self):
        # Create some dummy objects for page queries
        Course.objects.create(
            title="Test Course",
            code="TC",
            description="Testing description",
            duration_years=3,
            eligibility="10+2",
            seats=60
        )
        Notice.objects.create(
            title="Test Notice",
            content="Testing notice content",
            is_active=True
        )
        FacultyMember.objects.create(
            name="Dr. Test",
            designation="Tester",
            department="Testing Department",
            qualification="Ph.D"
        )
        GalleryImage.objects.create(
            title="Test Campus Image",
            category="campus"
        )

    def test_pages_status_code(self):
        """Verify that all main website pages load successfully"""
        pages = ['home', 'about', 'courses', 'gallery', 'contact']
        for page in pages:
            url = reverse(page)
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, f"Page '{page}' failed to load (status {response.status_code})")

    def test_contact_form_submission(self):
        """Verify that submitting the contact form saves data to database"""
        contact_url = reverse('contact')
        data = {
            'name': 'Test User',
            'email': 'testuser@example.com',
            'phone': '9876543210',
            'subject': 'Admission Enquiry',
            'message': 'This is a test message to verify form submission'
        }
        # Simulate standard POST request
        response = self.client.post(contact_url, data)
        self.assertEqual(response.status_code, 302) # Redirects on success
        
        # Verify saved object
        self.assertEqual(ContactMessage.objects.count(), 1)
        msg = ContactMessage.objects.first()
        self.assertEqual(msg.name, 'Test User')
        self.assertEqual(msg.subject, 'Admission Enquiry')

    def test_contact_form_ajax_submission(self):
        """Verify that AJAX contact form submission works and returns JSON response"""
        contact_url = reverse('contact')
        data = {
            'name': 'Ajax User',
            'email': 'ajax@example.com',
            'phone': '9123456789',
            'subject': 'AJAX Test',
            'message': 'Testing AJAX contact submission'
        }
        # Simulate AJAX post
        import json
        response = self.client.post(
            contact_url,
            data=json.dumps(data),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        
        # Verify JSON response
        json_data = response.json()
        self.assertEqual(json_data['status'], 'success')
        self.assertIn('sent successfully', json_data['message'])
        
        # Verify saved object in DB
        self.assertEqual(ContactMessage.objects.count(), 1)
        msg = ContactMessage.objects.first()
        self.assertEqual(msg.name, 'Ajax User')

    def test_contact_form_validation_fail(self):
        """Verify that invalid submissions return error state"""
        contact_url = reverse('contact')
        # Missing fields (no email and phone)
        data = {
            'name': 'Invalid User',
            'subject': 'Failed Test',
            'message': 'Testing invalid fields'
        }
        
        # Non-AJAX POST
        response = self.client.post(contact_url, data)
        self.assertEqual(response.status_code, 302) # Redirects back with flash messages
        self.assertEqual(ContactMessage.objects.count(), 0) # No message saved
        
        # AJAX POST
        import json
        response = self.client.post(
            contact_url,
            data=json.dumps(data),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 400) # Bad Request
        self.assertEqual(response.json()['status'], 'error')
