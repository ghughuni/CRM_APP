from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Record
from .views import export_to_excel

class RecordModelTestCase(TestCase):
    def setUp(self):
        self.record = Record.objects.create(
            passport_no='ABCD1234',
            first_name='John',
            last_name='Doe',
            email='johndoe@example.com',
            phone='1234567890',
            city='New York',
            address='123 Main St',
            zipcode='12345'
        )
    def test_model_str_representation(self):
        expected_result = "John Doe"
        self.assertEqual(str(self.record), expected_result)

    def test_model_fields(self):
        self.assertEqual(self.record.passport_no, 'ABCD1234')
        self.assertEqual(self.record.first_name, 'John')
        self.assertEqual(self.record.last_name, 'Doe')
        self.assertEqual(self.record.email, 'johndoe@example.com')
        self.assertEqual(self.record.phone, '1234567890')
        self.assertEqual(self.record.city, 'New York')
        self.assertEqual(self.record.address, '123 Main St')
        self.assertEqual(self.record.zipcode, '12345')

class ViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.factory = RequestFactory()

    def test_export_to_excel_view(self):
        record1 = Record.objects.create(
            passport_no='12345',
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            phone='1234567890',
            city='New York',
            address='123 Main St',
            zipcode='10001'
        )
        record2 = Record.objects.create(
            passport_no='67890',
            first_name='Jane',
            last_name='Smith',
            email='jane@example.com',
            phone='9876543210',
            city='Los Angeles',
            address='456 Elm St',
            zipcode='90001'
        )

        request = self.factory.get(reverse('export_to_excel'))
        request.user = self.user
        response = export_to_excel(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response['Content-Disposition'],
            'attachment; filename="Customers_data.xlsx"'
        )
        self.assertEqual(
            response['Content-Type'],
            'application/vnd.ms-excel'
        )


        from openpyxl import load_workbook
        from io import BytesIO

        excel_buffer = BytesIO(response.content)
        workbook = load_workbook(excel_buffer)
        sheet = workbook.active

        header_row = sheet[1]
        self.assertEqual(header_row[0].value, 'Passport No')
        self.assertEqual(header_row[1].value, 'First Name')
        self.assertEqual(header_row[2].value, 'Last Name')
        self.assertEqual(header_row[3].value, 'Email')
        self.assertEqual(header_row[4].value, 'Phone')
        self.assertEqual(header_row[5].value, 'City')
        self.assertEqual(header_row[6].value, 'Address')
        self.assertEqual(header_row[7].value, 'Zipcode')

        data_row1 = sheet[2]
        self.assertEqual(data_row1[0].value, '12345')
        self.assertEqual(data_row1[1].value, 'John')
        self.assertEqual(data_row1[2].value, 'Doe')
        self.assertEqual(data_row1[3].value, 'john@example.com')
        self.assertEqual(data_row1[4].value, '1234567890')
        self.assertEqual(data_row1[5].value, 'New York')
        self.assertEqual(data_row1[6].value, '123 Main St')
        self.assertEqual(data_row1[7].value, '10001')

        data_row2 = sheet[3]
        self.assertEqual(data_row2[0].value, '67890')
        self.assertEqual(data_row2[1].value, 'Jane')
        self.assertEqual(data_row2[2].value, 'Smith')
        self.assertEqual(data_row2[3].value, 'jane@example.com')
        self.assertEqual(data_row2[4].value, '9876543210')
        self.assertEqual(data_row2[5].value, 'Los Angeles')
        self.assertEqual(data_row2[6].value, '456 Elm St')
        self.assertEqual(data_row2[7].value, '90001')

