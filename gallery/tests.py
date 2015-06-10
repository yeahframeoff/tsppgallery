from unittest import skip
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.contrib.auth.forms import AuthenticationForm
from .gauth import UserCreationForm, Role
from gallery.models import Artist, Admin, Genre, GenreForm, Drawing
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
        print(form.errors)
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


    def test_admin_can_delete_user(self):
        """
        Admin can delete users of all roles
        """
        admin = Admin.objects.create_superuser(
            username='adminst',
            password='1234',
            email='admin@example.com'
        )
        user = Artist.objects.create_user(
            username='artistst',
            password='1234'
        )
        user_pk = user.pk
        admin.delete_user(user)
        with self.assertRaises(Artist.DoesNotExist):
            Artist.objects.get(pk=user_pk)


    def test_admin_can_create_and_delete_genres(self):
        """
        Admin can create and delete genres
        """
        admin = Admin.objects.create_superuser(
            username='adminst',
            password='1234',
            email='admin@example.com'
        )
        genre_text = 'VeryLongGenreTextItMustBeUnique'
        admin.add_genre(genre_text)
        self.assertTrue(Genre.objects.filter(name__icontains=genre_text).exists())
        admin.delete_genre(genre_text)
        with self.assertRaises(Genre.DoesNotExist):
            Genre.objects.get(name__icontains=genre_text)


    def test_genres_must_be_valid(self):
        """
        Genres must contain valid characters
        and satisfy regex r'^[А-Яа-яA-Za-z\w\s\.\,]+$'
        """
        form = GenreForm({'name': '#$%GD'})
        self.assertFalse(form.is_valid())
        form = GenreForm({'name': 'Valid text'})
        self.assertTrue(form.is_valid())


class CreateDrawingTest(TestCase):
    def test_create_drawing_with_bad_name(self):
        """
        If name is not string, AssertionError shoould be raised
        """
        artist = Artist.objects.create_user(
            username='artistka',
            password='1234'
        )
        not_string_obj = 10
        with self.assertRaises(AssertionError):
            artist.create_drawing(not_string_obj, None, None)

    def test_create_drawing_with_bad_descripton(self):
        """
        If description is not string, AssertionError shoould be raised
        """
        artist = Artist.objects.create_user(
            username='artistka',
            password='1234'
        )
        name = 'Good name'
        not_string_obj = []
        with self.assertRaises(AssertionError):
            artist.create_drawing(name, not_string_obj, None)

    def test_create_drawing_with_bad_image(self):
        """
        If image is not UploadedFile, AssertionError shoould be raised
        """
        artist = Artist.objects.create_user(
            username='artistka',
            password='1234'
        )
        name = 'Good name'
        description = 'Good description'
        image = 'image.jpg'
        with self.assertRaises(AssertionError):
            artist.create_drawing(name, description, image)

    def test_create_drawing_with_bad_genres(self):
        """
        If genres list is provided, it must be either
             QuerySet of Genre model
             or
             list of genre objects
             or
             list of integers
        if any of these fail, AssertionError is raised
        """
        artist = Artist.objects.create_user(
            username='artistka',
            password='1234'
        )
        name = 'Good name'
        description = 'Good description'
        filename = 'gallery/testdata/test_image_1.jpg'
        make_image = lambda: SimpleUploadedFile(filename,
                                                open(filename, 'rb').read())
        bad_genres1 = Drawing.objects.all()  # returns queryset with model Drawing
        bad_genres2 = [Drawing(), Genre()]   # there are non-Genre objects in list
        bad_genres3 = [1, 2, 3, 'string']    # there are non-integers in list
        for bad_genres in (bad_genres1, bad_genres2, bad_genres3):
            with self.assertRaises(AssertionError):
                artist.create_drawing(name,
                                      description,
                                      make_image(),
                                      bad_genres)
        good_genres = Genre.objects.all()    # returns queryset with model Genre
        drawing = artist.create_drawing(name, description, make_image(), good_genres)
        self.assertIsInstance(drawing, Drawing)

