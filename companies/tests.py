from django.test import TestCase, Client
from django.urls import reverse

from welcome_pages.models import User

from .models import Company, Job
from .forms import IdentityForm


class IdentityTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="testpass",
        )
        self.user.is_active = True
        self.user.save()
        company = Company.objects.create(user=self.user)
        company.save()
        job = Job.objects.create(company=self.user.company)
        job.save()

    def test_identity_view(self):
        url = reverse("companies:identity")
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "companies/identity.html")
        self.assertIsInstance(response.context["form"], IdentityForm)

    def test_identity_view_post_valid_form(self):
        url = reverse("companies:identity")
        self.client.force_login(self.user)
        response = self.client.post(
            url,
            {
                "name": "Test Company",
                "phone_number": "+33612345678",
                "adress": "Test address",
                "postal_code": "75001",
                "photo": "",
                "city": "Paris",
            },
        )
        self.assertRedirects(response, reverse("companies:company"))
        self.assertEqual(response.status_code, 302)

    def test_identity_view_post_invalid_form(self):
        url = reverse("companies:identity")
        self.client.force_login(self.user)
        response = self.client.post(
            url,
            {
                "name": "",
                "description": "",
                "phone_number": "",
                "adress": "",
                "postal_code": "",
                "photo": "",
                "city": "",
            },
        )
        self.assertEqual(response.status_code, 400)
