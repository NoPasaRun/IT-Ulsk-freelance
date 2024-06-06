import django
django.setup()


from django.test import TestCase
from admin_panel.models import Company, CompanyUser


class TestModels(TestCase):
    def test_company_has_user(self):
        company = Company(
            name='Test Company', image_link='http://test.com',
            business_number='Test Business', address='Test Address',
            leader_info='Leader', contact_info='Contact Info', web_site_link='www.test.com'
        )
        company.save()

        company_user = CompanyUser.objects.create(
            company=company, username="test",
            password="password", email="email@damn.com"
        )
        company_user.save()

        self.assertEqual(company.users.count(), 1)

    def test_model_str(self):
        company = Company(
            name='Test Company', image_link='http://test.com',
            business_number='Test Business', address='Test Address',
            leader_info='Leader', contact_info='Contact Info', web_site_link='www.test.com'
        )
        company.save()
        self.assertEqual(str(company), "Test Company")
