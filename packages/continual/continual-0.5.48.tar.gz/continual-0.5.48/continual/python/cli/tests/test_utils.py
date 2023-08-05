import unittest
import mock

from continual.python.sdk.changes import Change

from continual.python.cli import utils


class AStringHaving(str):
    def __eq__(self, other):
        return self in other


class print_change(unittest.TestCase):
    def test_should_handle_non_default_environments(self):
        with mock.patch("typer.secho") as sut:
            utils.print_change(
                Change(), "some_project", "some_non_default_env", "message"
            )
            print(sut.call_args_list)
            sut.assert_any_call(
                "Updating some_project@some_non_default_env:", fg=mock.ANY
            )
            sut.assert_any_call(
                "Operations for  in project 'some_project', environment 'some_non_default_env':",
                fg=mock.ANY,
            )
            sut.assert_any_call(
                AStringHaving("/projects/some_project@some_non_default_env/changes/"),
                fg=mock.ANY,
            )

    def test_should_handle_default_environment(self):
        with mock.patch("typer.secho") as sut:
            utils.print_change(Change(), "some_project", "prod", "message")
            print(sut.call_args_list)
            sut.assert_any_call("Updating some_project@production:", fg=mock.ANY)
            sut.assert_any_call(
                "Operations for  in project 'some_project', environment 'production':",
                fg=mock.ANY,
            )
            sut.assert_any_call(
                AStringHaving("/projects/some_project/changes/"),
                fg=mock.ANY,
            )

    def test_should_handle_default_environment_name(self):
        with mock.patch("typer.secho") as sut:
            utils.print_change(
                Change(), "some_project", "projects/some_project", "message"
            )
            print(sut.call_args_list)
            sut.assert_any_call("Updating some_project@production:", fg=mock.ANY)
            sut.assert_any_call(
                "Operations for  in project 'some_project', environment 'production':",
                fg=mock.ANY,
            )
            sut.assert_any_call(
                AStringHaving("/projects/some_project/changes/"),
                fg=mock.ANY,
            )
