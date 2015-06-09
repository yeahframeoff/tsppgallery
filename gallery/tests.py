from PIL import Image
from django.core.files.uploadedfile import TemporaryUploadedFile, SimpleUploadedFile
from django.test import TestCase
from django.contrib.auth.forms import AuthenticationForm
from .gauth import UserCreationForm, Role
from gallery.models import Artist
from collections import namedtuple


class LoginTest(TestCase):
    def test_wrong_credentials_shall_not_pass(self):
        """
        If user inputs wrong data, auth form is invalid
        """
        username, pwd, wrong_pwd = 'test1', '1234', '1235'
        user = Artist.objects.create_user(
            username=username,
            password=pwd
        )
        form = AuthenticationForm({
            'username':username,
            'password':wrong_pwd
        })
        self.assertFalse(form.is_valid() )

    def test_wrong_data_shall_not_register(self):
        """
        username must match regex: r'^[A-Za-z0-9._]{4,20}$'
        first_name and last_name can be empty or must satisfy
        regex: r'^([А-Я][а-я]+)|([A-Z][a-z]+)$'
        email must be valid email
        uploaded photo is obligatory
        role must be either Artist or Organizer
        password1 must equal password2 (for confirmation)
        """
        DataType = namedtuple('DataType', ('data', 'files', 'preferred_result'))
        TheForm = UserCreationForm
        filename = 'gallery/testdata/test_image_1.jpg'
        data_list = [
            DataType(
                {
                    'username': 'valera',
                    'password1': '123456',
                    'password2': '123456',
                    'first_name': 'Valera',
                    'last_name': 'Kavalera',
                    'email': 'vale@gmail.com',
                    'role': Role.ARTIST
                },
                {
                    'photo': SimpleUploadedFile(filename, open(filename, 'rb').read())
                },
                True
            ),
            DataType(
                {
                    'username': 'asdf#$%',
                    'password1': '123456',
                    'password2': '123456',
                    'first_name': 'Valera',
                    'last_name': 'Kavalera',
                    'email': 'vale@gmail.com',
                    'role': Role.ARTIST
                },
                {
                    'photo': SimpleUploadedFile(filename, open(filename, 'rb').read())
                },
                False
            ),
            DataType(
                {
                    'username': 'michail',
                    'password1': '123457',
                    'password2': '123457',
                    'first_name': 'VLASDsdf',
                    'last_name': 'KavaДрцу',
                    'email': 'vale@gmail.com',
                    'role': Role.ORGANIZER
                },
                {
                    'photo': SimpleUploadedFile(filename, open(filename, 'rb').read())
                },
                False
            ),
            DataType(
                {
                    'username': 'bombaleillo',
                    'password1': '2375#$HT*890',
                    'password2': '2375#$HT*890',
                    'first_name': 'Petro',
                    'last_name': 'Poroshenko',
                    'email': 'pet$ro#gmail.lom',
                    'role': Role.ARTIST
                },
                {
                    'photo': SimpleUploadedFile(filename, open(filename, 'rb').read())
                },
                False
            ),
            DataType(
                {
                    'username': 'panamero',
                    'password1': '123459',
                    'password2': '123459',
                    'first_name': 'Carerra',
                    'last_name': 'Sambrera',
                    'email': 'vale@gmail.com',
                    'role': Role.ARTIST
                },
                {
                    # empty
                },
                False
            ),
            DataType(
                {
                    'username': 'puerterikanec',
                    'password1': '1234567',
                    'password2': '1234586',
                    'first_name': 'Puerte',
                    'last_name': 'Rikanets',
                    'email': 'vale@gmail.com',
                    'role': Role.ORGANIZER
                },
                {
                    'photo': SimpleUploadedFile(filename, open(filename, 'rb').read())
                },
                False
            ),
            DataType(
                {
                    'username': 'fujitsu',
                    'password1': 'asdfghj',
                    'password2': 'asdfghj',
                    'first_name': 'Fujitsu',
                    'last_name': 'Yaponets',
                    'email': 'yaponets@gmail.com',
                    'role': Role.ADMIN
                },
                {
                    'photo': SimpleUploadedFile(filename, open(filename, 'rb').read())
                },
                False
            ),
        ]
        for data_item in data_list:
            form = TheForm(data_item.data, data_item.files)
            print(form.is_valid())
            print(form.errors)
            print(data_item.preferred_result)
            self.assertFalse(form.is_valid() ^ data_item.preferred_result )
