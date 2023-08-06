from argparse import ArgumentParser
from pathlib import Path

from django.core.management.base import BaseCommand

from django_keygen import KeyGen, DEFAULT_CHARS


class Command(BaseCommand):
    """Secret key generator"""

    help = KeyGen.__doc__

    def add_arguments(self, parser: ArgumentParser) -> None:
        """Add arguments to a command line parser

        Adds ``len`` and ``chars`` arguments to CLI.

        Args:
            parser: The parser to add arguments to
        """

        parser.add_argument(
            'length', type=int, nargs='?', default=50,
            help='Length of the key to generate')

        parser.add_argument(
            'chars', type=str, nargs='?', default=DEFAULT_CHARS,
            help='Characters to include in the secret key')

        parser.add_argument(
            'force', type=bool, nargs='?', default=False,
            help='Issue warnings instead of exceptions for unsafe security options')

    def handle(self, *args, **options) -> str:
        """Handle a command line call for the parent class"""

        generator = KeyGen(length=options['length'], chars=options['chars'], force=options['force'])
        return generator.gen_secret_key()
