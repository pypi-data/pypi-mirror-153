from typing import Optional, List
import typer
import os
import yaml

from continual.python.cli import utils
from continual.python.sdk.client import Client
from continual.rpc.management.v1.types import Extension
from rich.console import Console

app = typer.Typer(help="Manage extensions.", hidden=True)


def format_extension_data(extension: Extension, zipped=False, all_projects=False):
    create_time = extension.create_time.replace(microsecond=0)
    update_time = extension.update_time.replace(microsecond=0)

    environment = extension.parent.split("/")[-1]
    data = [
        extension.extension_id,
        extension.name,
        environment,
        extension.extension_type,
        create_time,
        update_time,
        extension.class_name,
        extension.module_name,
        extension.package_url,
        extension.package_hash,
    ]
    headers = [
        "ID",
        "Name",
        "Environment",
        "Extension Type",
        "Created",
        "Updated",
        "Class Name",
        "Module Name",
        "Package URL",
        "Package Hash",
    ]
    if zipped:
        return tuple([x[0], x[1]] for x in (zip(headers, data)))
    if all_projects:
        data.insert(0, extension.parent.split("/")[1])
        headers.insert(0, "Project")
    return (data, headers)


# use callback to run  list command if nothing is passed in
@app.callback(invoke_without_command=True)
def default(ctx: typer.Context):
    if ctx.invoked_subcommand is not None:
        return
    else:
        extension_list(
            project=None,
            environment=None,
            n=30,
            all_projects=False,
            style=None,
        )


@app.command("new")
@utils.exit_on_error
def extension_new(
    project: str = typer.Option(None, help="Project ID."),
    environment: str = typer.Option(None, "--env", help="Environment ID."),
    id: str = typer.Option(..., "--id", help="Unique ID/label for the extension."),
    path: str = typer.Option(
        os.getcwd(), "--path", help="Directory in which to create the extension."
    ),
    model: bool = typer.Option(
        True, "--model", help="Set the extension type to a custom model."
    ),
    class_name: str = typer.Option(
        "MyCustomModel", "--class", help="Name of the implementation class"
    ),
    source_path: str = typer.Option(
        None,
        "--source",
        help="Implementation source code to be copied into extension directory.",
    ),
    dependencies: Optional[List[str]] = typer.Option(
        None, "--dependency", help="Add a pip package dependency to this extension"
    ),
):
    """Create a new extension template."""

    project, environment = utils.get_project_and_environment(project, environment)
    c = Client(project=utils.get_environment_name(project, environment))

    # Set extension type
    if model:
        e_type = "model"
    else:
        e_type = "model"

    # Call to ExtensionManager
    c.extensions.new(
        root=path,
        id=id,
        extension_type=e_type,
        class_name=class_name,
        source_path=source_path,
        dependencies=list(dependencies),
    )

    typer.secho(
        "\nCreated extension '%s' of type %s at %s"
        % (id, e_type, os.path.join(path, id)),
        fg="blue",
    )


@app.command("list")
@utils.exit_on_error
def extension_list(
    project: str = typer.Option(None, help="Project ID."),
    environment: str = typer.Option(None, "--env", help="Environment ID."),
    n: int = typer.Option(30, "--num", "-n", help="Number of records to show."),
    all_projects: bool = typer.Option(False, "--all", "-a", help="Show all projects."),
    style: utils.ContinualStyle = typer.Option(None, help="Color to use for list."),
):
    """List Extensions."""

    project, environment = utils.get_project_and_environment(project, environment)
    c = Client(project=utils.get_environment_name(project, environment))

    project_snippet = "project %s, environment %s" % (project, environment)
    if all_projects:
        project_snippet = "all accessible projects"
    data = []
    headers = []
    for e in c.extensions.list(n, all_projects=all_projects):
        (e_data, headers) = format_extension_data(e, all_projects=all_projects)
        data.append(e_data)
    typer.secho(
        "\nFound %s extensions in %s:" % (len(data), project_snippet),
        fg="blue",
    )
    utils.print_table(data, headers, style=utils.get_style(style))


@app.command("get")
@utils.exit_on_error
def get(
    extension: str = typer.Argument(..., help="Extension ID."),
    project: str = typer.Option(None, help="Project ID."),
    environment: str = typer.Option(None, "--env", help="Environment ID."),
    to_json: bool = typer.Option(
        False, "--json", help="Show full JSON representation."
    ),
):
    """Get extension details."""
    project, environment = utils.get_project_and_environment(project, environment)
    c = Client(project=utils.get_environment_name(project, environment))

    e = c.extensions.get(id=extension)

    console = Console()
    if to_json:
        console.print(e.to_dict())
    else:
        data = format_extension_data(e, zipped=True)
        typer.secho("\nRetrieving extension %s: \n" % (extension), fg="blue")
        utils.print_info(data)
        typer.secho("\nExtension schema:\n", fg="blue")
        console.print(yaml.safe_load(e.schema_text))


@app.command("delete")
@utils.exit_on_error
def delete(
    extension: str = typer.Argument(..., help="Extension ID."),
    project: str = typer.Option(None, help="Project ID."),
    environment: str = typer.Option(None, "--env", help="Environment ID."),
    force: bool = typer.Option(
        False, "--force", help="Force deletion. Skips confirmation."
    ),
):
    """Delete extension."""
    project, environment = utils.get_project_and_environment(project, environment)
    c = Client(project=utils.get_environment_name(project, environment))

    if not force:
        force = typer.confirm(
            "Are you sure you want to delete extension %s in project %s, environment %s?"
            % (extension, project, environment),
        )
    if force:
        c.projects.get(project).extensions.delete(id=extension)
        typer.secho("Successfully deleted extension %s." % extension, fg="green")
    else:
        typer.secho("Cancelled extension deletion!", fg="blue")
