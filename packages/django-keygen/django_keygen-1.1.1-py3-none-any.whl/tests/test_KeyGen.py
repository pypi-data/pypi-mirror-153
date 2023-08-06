import string
from pathlib import Path
from unittest import TestCase

from django_keygen import KeyGen, SecurityWarning, SecurityException, DEFAULT_CHARS


class KeyGeneration(TestCase):
    """Tests for the generation of secret keys"""

    def test_returned_length(self) -> None:
        """Test the returned key length matches the ``length`` argument"""

        for i in range(10, 25, 50):
            generator = KeyGen(length=i, force=True)
            self.assertEqual(i, len(generator.gen_secret_key()))

    def test_sequential_not_equal(self) -> None:
        """Test sequential keys do not match"""

        # This isn't really a true test for randomness - those are very involved
        # However, it will protect a developer who left behind a seed while debugging
        self.assertNotEqual(
            KeyGen().gen_secret_key(),
            KeyGen().gen_secret_key()
        )


class SecurityErrorsAndWarnings(TestCase):
    """Tests for security warnings and errors"""

    def test_error_on_non_positive_length(self) -> None:
        """Test for a ``ValueError`` on a non-positive key length"""

        with self.assertRaises(ValueError):
            KeyGen(length=0)

        with self.assertRaises(ValueError):
            KeyGen(length=-1)

    def test_warn_on_short_length(self) -> None:
        """Test a warning is issued for a short key length"""

        with self.assertRaises(SecurityException):
            KeyGen(length=29)

        with self.assertWarns(SecurityWarning):
            KeyGen(length=29, force=True)

    def test_warn_on_small_char_set(self) -> None:
        """Test a warning is issued for a small character set"""

        with self.assertRaises(SecurityException):
            KeyGen(chars='abcd')

        with self.assertWarns(SecurityWarning):
            KeyGen(chars='abcd', force=True)


class DefaultCharacterSet(TestCase):
    """Tests for the default character set used in key generation"""

    def assertSubsetChars(self, expected: str, actual: str) -> None:
        """Test if characters of the ``expected`` string are a subset of the ``actual`` string"""

        expected_set = set(expected)
        actual_set = set(actual)
        self.assertTrue(expected_set.issubset(actual_set))

    def test_contains_ascii_lower(self) -> None:
        """Test keys pull from lowercase letters"""

        self.assertSubsetChars(string.ascii_lowercase, DEFAULT_CHARS)

    def test_contains_ascii_upper(self) -> None:
        """Test keys pull from uppercase letters"""

        self.assertSubsetChars(string.ascii_uppercase, DEFAULT_CHARS)

    def test_contains_punctuation(self) -> None:
        """Test keys pull from punctuation"""

        self.assertSubsetChars(string.punctuation, DEFAULT_CHARS)


class FromPlainText(TestCase):
    """Tests for the reading/writing of secret keys from a file"""

    def setUp(self) -> None:
        """Define a test file path and ensure it does not exist"""

        self.test_path = Path('test_key.txt').resolve()
        self.tearDown()

    def tearDown(self) -> None:
        """Delete the test key file"""

        try:
            self.test_path.unlink()

        except FileNotFoundError:
            pass

    def test_error_if_file_not_found(self) -> None:
        """Check for a ``FileNotFoundError`` if the file does not exist"""

        with self.assertRaises(FileNotFoundError):
            KeyGen().from_plaintext(self.test_path)

    def test_file_is_created(self) -> None:
        """Tet the file is created when ``create_if_not_exist=True``"""

        returned_key = KeyGen().from_plaintext(self.test_path, create_if_not_exist=True)
        self.assertTrue(self.test_path.exists())
        with self.test_path.open('r') as infile:
            key_on_disk = infile.readline()

        self.assertEqual(returned_key, key_on_disk, 'Returned key does not match key on disk')

    def test_returned_key_has_no_newline(self):
        """Test the key returned from file has no newline"""

        # Run test once when the file does not exist
        returned_key = KeyGen().from_plaintext(self.test_path, create_if_not_exist=True)
        self.assertEqual(returned_key.strip(), returned_key)

        # Run the test again now that the file does exist
        returned_key = KeyGen().from_plaintext(self.test_path, create_if_not_exist=True)
        self.assertEqual(returned_key.strip(), returned_key)
