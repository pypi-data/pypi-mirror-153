from argparse import ArgumentParser
from unittest import TestCase

from django_keygen import KeyGen, DEFAULT_CHARS
from django_keygen.management.commands.keygen import Command


class CliDocumentation(TestCase):
    """Tests for the command line help text"""

    def test_help_text_is_set(self) -> None:
        """Test the command line parser help text matches the ``KeyGen`` class documentation"""

        self.assertEqual(KeyGen.__doc__, Command.help)


class CliParsing(TestCase):
    """Test for the parsing of command line arguments"""

    def test_for_default_cli_arguments(self) -> None:
        """Test arguments are added to the command line parser"""

        command = Command()
        test_parser = ArgumentParser()
        command.add_arguments(test_parser)

        # Compare parser defaults against package defaults
        parsed_args = test_parser.parse_args([])
        self.assertEqual(50, parsed_args.length)
        self.assertEqual(DEFAULT_CHARS, parsed_args.chars)
        self.assertEqual(False, parsed_args.force)
