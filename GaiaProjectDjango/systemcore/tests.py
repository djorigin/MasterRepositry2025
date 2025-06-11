from django.test import TestCase
# GaiaProjectDjango
# systemcore/tests.py
# This file contains tests for the systemcore app in the GaiaProjectDjango project.
# Django imports
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import SystemCoreColourCode    

# Create your tests here.
class SystemCoreColourCodeTests(TestCase):
    def setUp(self):
        # Define test user credentials
        self.TEST_USERNAME = 'testuser'
        self.TEST_PASSWORD = 'testpassword'
        # Create a test user
        self.user = User.objects.create_user(username=self.TEST_USERNAME, password=self.TEST_PASSWORD)

    def test_colour_code_creation(self):
        # Test creating a new colour code
        colour_code = SystemCoreColourCode.objects.create(
            name='Test colour',
            rgb_value='255,0,0',
            hex_code='#FF0000'
        )
        self.assertEqual(colour_code.name, 'Test colour')
        self.assertEqual(colour_code.rgb_value, '255,0,0')
        self.assertEqual(colour_code.hex_code, '#FF0000')
        self.assertEqual(str(colour_code), 'Test colour (#FF0000, RGB: 255,0,0)')
        
    def test_colour_code_str_method(self):
        # Test the __str__ method of the SystemCoreColourCode model
        colour_code = SystemCoreColourCode.objects.create(
            name='Test colour',
            rgb_value='0,255,0',
            hex_code='#00FF00'
        )
        self.assertEqual(str(colour_code), 'Test colour (#00FF00, RGB: 0,255,0)')

    def test_colour_code_name_capitalization(self):
        # Test that the name is capitalized when saved
        colour_code = SystemCoreColourCode.objects.create(
            name='test colour',
            rgb_value='0,0,255',
            hex_code='#0000FF'
        )
        self.assertEqual(colour_code.name, 'Test colour')

    def test_colour_code_rgb_validation(self):
        # Test that invalid RGB values raise a validation error
        with self.assertRaises(ValidationError):
            SystemCoreColourCode.objects.create(
                name='Invalid RGB',
                rgb_value='256,0,0',  # Invalid RGB value
                hex_code='#FF0000'
            )

    def test_colour_code_hex_validation(self):
        # Test that invalid hex codes raise a validation error
        with self.assertRaises(ValidationError):
            SystemCoreColourCode.objects.create(
                name='Invalid Hex',
                rgb_value='0,0,0',
                hex_code='FF0000'  # Invalid hex code (missing '#')
            )

    def test_colour_code_unique_constraints(self):
        # Test that unique constraints are enforced
        SystemCoreColourCode.objects.create(
            name='Unique colour',
            rgb_value='255,255,0',
            hex_code='#FFFF00'
        )
        with self.assertRaises(ValidationError):
            SystemCoreColourCode.objects.create(
                name='Unique colour',
                rgb_value='255,255,0',
                hex_code='#FFFF00'  # Duplicate entry
            )

    def test_colour_code_url_reverse(self):
        # Test that the URL name 'systemcore:colorcode_list')' is correctly defined
        url = reverse('systemcore:colorcode_list')
    def test_colour_code_view_access(self):
        """
        Test that the colour code view is accessible.

        This test ensures that:
        - The view is accessible to authenticated users.
        - The correct URL name 'systemcore:colorcode_list')' is defined in urls.py.
        - The view renders the expected template 'systemcore/colorcode_list').html'.
        """
        self.client.login(username='testuser', password='testpassword')
        # Ensure the URL name 'systemcore:colorcode_list')' is correctly defined in urls.py
        response = self.client.get(reverse('systemcore:colorcode_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'systemcore/colorcode_list.html')
        url = reverse('systemcore:colorcode_list')
        self.assertEqual(url, '/systemcore/colorcode_list/')
    
    def test_colorcode_new_url_reverse(self):
        # Test that the URL name 'systemcore:colorcode_create' is correctly defined
        url = reverse('systemcore:colorcode_create')
        self.assertEqual(url, '/systemcore/colorcode_create/')
        
        # Ensure the resolved URL is functional
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Test that the URL name 'systemcore:colorcode_create' is correctly defined
        url = reverse('systemcore:colorcode_create')
        self.assertEqual(url, '/systemcore/colorcode_create/')

    def test_colorcode_new_view_access(self):
        """
        Test that the ColorCodeNew view is accessible and uses the correct template.
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('systemcore:colorcode_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'systemcore/colorcode_form.html')

    def test_colorcode_new_post(self):
        """
        Test creating a new color code via POST to the ColorCodeNew view.
        """
        self.client.login(username='testuser', password='testpassword')
        data = {
            'name': 'Posted Colour',
            'rgb_value': '123,123,123',
            'hex_code': '#7B7B7B'
        }
        response = self.client.post(reverse('systemcore:colorcode_create'), data)
        # Should redirect to the colorcode_list page after successful creation
    


    