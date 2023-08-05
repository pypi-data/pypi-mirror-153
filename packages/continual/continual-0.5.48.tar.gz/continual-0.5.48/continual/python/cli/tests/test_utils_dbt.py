import unittest
import tempfile
import os
import mock

from continual.python.cli import utils_dbt


class AStringHaving(str):
    def __eq__(self, other):
        return self in other


class process_dbt_project_file(unittest.TestCase):
    def test_should_parse_dbt_project_config(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dbt_project_file_path = os.path.join(tmpdir, "dbt_project.yml")
            with open(dbt_project_file_path, "w+") as dbt_project_file:
                dbt_project_file.writelines(
                    """
name: 'my_new_project'
version: '1.0.0'
config-version: 2

profile: 'default'

model-paths: ["models"]
analysis-paths: ["analysis"]
test-paths: ["tests"]
seed-paths: ["data"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

target-path: "target"
clean-targets:
  - "target"
  - "dbt_modules"

models:
  my_new_project:                
                """
                )

            (
                dbt_project_config_file_path,
                dbt_project_name,
                dbt_default_profile_name,
                dbt_target_dir,
                dbt_manifest_file_path,
            ) = utils_dbt.process_dbt_project_file(tmpdir)

            assert dbt_project_config_file_path == os.path.join(
                tmpdir, "dbt_project.yml"
            )
            assert dbt_project_name == "my_new_project"
            assert dbt_default_profile_name == "default"
            assert dbt_target_dir == "target"
            assert dbt_manifest_file_path == os.path.join(
                tmpdir, "target/manifest.json"
            )


class get_default_target(unittest.TestCase):
    def test_should_get_profile_target_name(self):
        dbt_profiles_file_path = ""
        with tempfile.TemporaryDirectory() as tmpdir:
            dbt_profiles_file_path = os.path.join(tmpdir, "profiles.yml")
            with open(dbt_profiles_file_path, "w+") as dbt_profiles_file:
                dbt_profiles_file.writelines(
                    """
a_profile_name:
  outputs:
    a_target_name:
      type: snowflake
      account: a_snowflake_account
      user: a_snowflake_user
      password: a_snowflake_password
      role: a_snowflake_role
      database: a_snowflake_database
      warehouse: a_snowflake_warehouse
      schema: a_snowflake_schema_name

  target: a_target_name            
                """
                )

            result = utils_dbt.get_default_target(
                dbt_profiles_file_path, "a_profile_name"
            )
            assert result == "a_target_name"

    def test_should_handle_case_sensitive_profile_names(self):
        dbt_profiles_file_path = ""
        with tempfile.TemporaryDirectory() as tmpdir:
            dbt_profiles_file_path = os.path.join(tmpdir, "profiles.yml")
            with open(dbt_profiles_file_path, "w+") as dbt_profiles_file:
                dbt_profiles_file.writelines(
                    """
A_Profile_Name_With_Capital_Letters:
  outputs:
    a_target_name:
      type: snowflake
      account: a_snowflake_account
      user: a_snowflake_user
      password: a_snowflake_password
      role: a_snowflake_role
      database: a_snowflake_database
      warehouse: a_snowflake_warehouse
      schema: a_snowflake_schema_name

  target: a_target_name
                """
                )

            result = utils_dbt.get_default_target(
                dbt_profiles_file_path, "A_Profile_Name_With_Capital_Letters"
            )
            assert result == "a_target_name"

    def test_should_handle_case_sensitive_keys(self):
        dbt_profiles_file_path = ""
        with tempfile.TemporaryDirectory() as tmpdir:
            dbt_profiles_file_path = os.path.join(tmpdir, "profiles.yml")
            with open(dbt_profiles_file_path, "w+") as dbt_profiles_file:
                dbt_profiles_file.writelines(
                    """
a_profile_name:
  outputs:
    a_target_name:
      type: snowflake
      account: a_snowflake_account
      user: a_snowflake_user
      password: a_snowflake_password
      role: a_snowflake_role
      database: a_snowflake_database
      warehouse: a_snowflake_warehouse
      schema: a_snowflake_schema_name

  TARGET: a_target_name     
                """
                )

            result = utils_dbt.get_default_target(
                dbt_profiles_file_path, "a_profile_name"
            )
            # dbt requires keys to be lowercase: https://linear.app/continual/issue/DEV-2805/dbt-profile-config-keys-are-case-sensitive
            assert result is None


class get_default_target(unittest.TestCase):
    def test_should_get_default_target_for_profile(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dbt_profiles_file_path = os.path.join(tmpdir, "dbt_profiles.yml")
            with open(dbt_profiles_file_path, "w+") as dbt_profiles_file:
                dbt_profiles_file.writelines(
                    """
a_profile_name:
  outputs:
    a_target:
      type: snowflake
      account: some_account
      user: some_user
      password: some_password
      role: some_role
      database: some_database
      warehouse: some_warehouse
      schema: some_schema

  target: a_target             
                """
                )

            dbt_target_result = utils_dbt.get_default_target(
                dbt_profiles_file_path, "a_profile_name"
            )

            assert dbt_target_result == "a_target"

    def test_should_fail_when_default_target_is_not_defined(self):
        # Note that this misconfiguration also causes `dbt debug` to fail
        with tempfile.TemporaryDirectory() as tmpdir:
            dbt_profiles_file_path = os.path.join(tmpdir, "dbt_profiles.yml")
            with open(dbt_profiles_file_path, "w+") as dbt_profiles_file:
                dbt_profiles_file.writelines(
                    """
a_profile_name:
  outputs:
    a_different_target:
      type: snowflake
    another_different_target:
      type: snowflake

  target: a_target_without_a_definition
                """
                )

            with mock.patch("typer.secho") as secho:
                with self.assertRaises(SystemExit) as e:
                    utils_dbt.get_default_target(
                        dbt_profiles_file_path, "a_profile_name"
                    )
                secho.assert_any_call(
                    AStringHaving("Default dbt target definition not found"),
                    fg=mock.ANY,
                )


class dbt_target_name_is_defined(unittest.TestCase):
    def test_should_return_true_when_target_is_defined(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dbt_profiles_file_path = os.path.join(tmpdir, "dbt_profiles.yml")
            with open(dbt_profiles_file_path, "w+") as dbt_profiles_file:
                dbt_profiles_file.writelines(
                    """
a_profile_name:
  outputs:
    a_target:
      type: snowflake
      account: some_account
      user: some_user
      password: some_password
      role: some_role
      database: some_database
      warehouse: some_warehouse
      schema: some_schema

  target: a_target             
                """
                )

            result = utils_dbt.dbt_target_name_is_defined(
                dbt_profiles_file_path, "a_profile_name", "a_target"
            )
            assert result == True

    def test_should_return_false_and_secho_when_target_is_not_defined(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dbt_profiles_file_path = os.path.join(tmpdir, "dbt_profiles.yml")
            with open(dbt_profiles_file_path, "w+") as dbt_profiles_file:
                dbt_profiles_file.writelines(
                    """
a_profile_name:
  outputs:
    a_target:
      type: snowflake
      account: some_account
      user: some_user
      password: some_password
      role: some_role
      database: some_database
      warehouse: some_warehouse
      schema: some_schema

  target: a_target
                """
                )

            with mock.patch("typer.secho") as secho:
                result = utils_dbt.dbt_target_name_is_defined(
                    dbt_profiles_file_path, "a_profile_name", "a_non_existent_target"
                )
                assert result == False
                secho.assert_any_call(
                    AStringHaving(
                        "dbt target definition not found for target 'a_non_existent_target'."
                    ),
                    fg=mock.ANY,
                )


class dbt_profile_name_is_defined(unittest.TestCase):
    def test_should_return_true_when_profile_is_defined(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dbt_profiles_file_path = os.path.join(tmpdir, "dbt_profiles.yml")
            with open(dbt_profiles_file_path, "w+") as dbt_profiles_file:
                dbt_profiles_file.writelines(
                    """
a_profile_name:
  outputs:
    a_target:
      type: snowflake
      account: some_account
      user: some_user
      password: some_password
      role: some_role
      database: some_database
      warehouse: some_warehouse
      schema: some_schema

  target: a_target             
                """
                )

            result = utils_dbt.dbt_profile_name_is_defined(
                dbt_profiles_file_path, "a_profile_name"
            )
            assert result == True

    def test_should_return_false_and_secho_when_profile_is_not_defined(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dbt_profiles_file_path = os.path.join(tmpdir, "dbt_profiles.yml")
            with open(dbt_profiles_file_path, "w+") as dbt_profiles_file:
                dbt_profiles_file.writelines(
                    """
a_profile_name:
  outputs:
    a_target:
      type: snowflake
      account: some_account
      user: some_user
      password: some_password
      role: some_role
      database: some_database
      warehouse: some_warehouse
      schema: some_schema

  target: a_target
                """
                )

            with mock.patch("typer.secho") as secho:
                result = utils_dbt.dbt_profile_name_is_defined(
                    dbt_profiles_file_path, "a_non_existent_profile_name"
                )
                assert result == False
                secho.assert_any_call(
                    AStringHaving(
                        "dbt profile definition not found for profile 'a_non_existent_profile_name'."
                    ),
                    fg=mock.ANY,
                )


class dbt_target_name_as_environment_id(unittest.TestCase):
    def test_should_replace_dashes_with_underscores(self):
        assert (
            utils_dbt.dbt_target_name_as_environment_id("target-name-with-dashes")
            == "target_name_with_dashes"
        )


class is_dbt_project_dir(unittest.TestCase):
    def test_should_return_true_when_dbt_config_file_exists(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dbt_profiles_file_path = os.path.join(tmpdir, "dbt_project.yml")
            with open(dbt_profiles_file_path, "w+") as dbt_profiles_file:
                dbt_profiles_file.writelines(
                    """
name: 'my_dbt_project'
                    """
                )

            result = utils_dbt.is_dbt_project_dir(tmpdir)
            assert result == True

    def test_should_return_false_when_dbt_config_file_does_not_exist(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            result = utils_dbt.is_dbt_project_dir(tmpdir)
            assert result == False
