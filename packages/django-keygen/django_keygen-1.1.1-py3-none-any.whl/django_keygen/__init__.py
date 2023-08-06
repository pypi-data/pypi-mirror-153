"""The ``django-keygen`` package provides an easy and convenient way to generate
secure secret keys for use with ``django`` driven web applications.

The ``SECRET_KEY`` setting in Django is used to provide
`cryptographic signing <https://docs.djangoproject.com/en/2.2/topics/signing/>`_
and is an important part of building secure Django applications.
While it is mostly used to sign session cookies, other common uses
include generating secure URL's, protecting form content in hidden fields,
and restricting access to private resources.

Installation
------------

The ``django-keygen`` package is pip installable:

.. code-block:: bash

   $ pip install django-keygen

To integrate the package with an existing django application, add it to
the ``installed_apps`` list in the application settings:

.. code-block:: python

   >>> INSTALLED_APPS = [
   ...    'django-keygen',
   ...    ...
   ... ]

Python Usage
------------

Key generation is available using the ``KeyGen`` class:

.. doctest:: python

   >>> from django_keygen import KeyGen
   >>> key_generator = KeyGen()
   >>> secret_key = key_generator.gen_secret_key()

By default, keys are generated using the full range of ascii charaters and
are 50 characters long. This can be overwritted using key word arguments:

.. doctest:: python

   >>> from string import ascii_lowercase
   >>> key_generator = KeyGen(length=55, chars=ascii_lowercase)
   >>> secret_key = key_generator.gen_secret_key()

To use the package in your django application, you will want to persist your
secret key to disk. In your ``settings.py`` file, add the code snippet below.
The ``secret_key.txt`` file wil be created automatically if it does not already
exist.

.. doctest:: python

   >>> from django_keygen import KeyGen
   >>> key_generator = KeyGen()
   >>> SECRET_KEY = key_generator.from_plaintext('secret_key.txt', create_if_not_exist=True)

Command Line Usage
------------------

The command line interface is accessible via the django management tool:

.. code-block:: bash

   $ python manage.py keygen

Just like the Python interface, you can specify the key length and charecter set used to generate the key:

.. code-block:: bash

   $ python manage.py keygen 50 some_character_set

You can also write a new secret key to disk.

.. important:: The following command will overwrite an existing key file

.. code-block:: bash

   $ python manage.py keygen >> secret_key.txt

Security Notices
----------------

It is considered bad security practice to use short security keys generating
using few unique characters. To safeguard against this, a ``SecurityError``
is raised when ``django-keygen`` is asked to generate an insecure key.

.. doctest:: python

   >>> key_generator = KeyGen(length=5, chars='abc')
   Traceback (most recent call last):
   ...
   django_keygen.exceptions.SecurityException: Secret key length is short. Consider increasing the key length.
   ...

The error can be ignored by specifying ``force=True``, in which case a warning
is issued instead:

.. doctest:: python

   >>> key_generator = KeyGen(length=5, chars='abc', force=True)
"""

import string
from pathlib import Path
from typing import Union
from warnings import warn

from django.utils.crypto import get_random_string

from django_keygen.exceptions import SecurityWarning, SecurityException

__version__ = '1.1.1'
__author__ = 'Daniel Perrefort'

DEFAULT_CHARS = string.ascii_letters + string.digits + string.punctuation


class KeyGen:
    """Generates and prints a new secret key"""

    def __init__(self, length: int = 50, chars: str = DEFAULT_CHARS, force: bool = False) -> None:
        if length <= 0:
            raise ValueError('Key length must be greater than zero.')

        msg = None
        if length < 30:
            msg = 'Secret key length is short. Consider increasing the key length.'

        elif len(set(chars)) < 20:
            msg = 'Secret key generated with few unique characters. Try increasing the character set size.'

        if msg and force:
            warn(msg, SecurityWarning)

        elif msg:
            raise SecurityException(msg)

        self.length = length
        self.chars = chars

    def gen_secret_key(self) -> str:
        """Generate a secret key for Django"""

        return get_random_string(self.length, self.chars)

    def from_plaintext(self, path: Union[Path, str], create_if_not_exist: bool = False) -> str:
        """Load a secret key from a plain text file on disk

        Args:
            path: The path to load the secret key from
            create_if_not_exist: Create a secret key and write it to the given path if the path does not exist

        Returns:
            The secret key
        """

        path = Path(path)
        if path.exists():
            with path.open('r') as outfile:
                key = outfile.readline()

        elif create_if_not_exist:
            key = self.gen_secret_key()
            with path.open('w') as outfile:
                outfile.write(key)

        else:
            raise FileNotFoundError('The given path does not exist. Create it or set `create_if_not_exist=True`.')

        key_length = len(key)
        if key_length != self.length:
            warn(f'Length of security key on disk (key_length) does not match the value passed to KeyGen ({self.length})', SecurityWarning)

        return key
