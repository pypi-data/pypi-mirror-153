from typing import Optional

import click

from anyscale.cli_logger import BlockLogger
from anyscale.controllers.job_controller import JobController
from anyscale.util import validate_non_negative_arg


log = BlockLogger()  # CLI Logger


@click.group("job", help="Interact with production jobs running on Anyscale.")
def job_cli() -> None:
    pass


@job_cli.command(name="submit", help="Submit a job to run asynchronously.")
@click.argument("job-config-file", required=True)
@click.option("--name", "-n", required=False, default=None, help="Name of job.")
@click.option("--description", required=False, default=None, help="Description of job.")
@click.option(
    "--follow",
    "-f",
    required=False,
    default=False,
    type=bool,
    is_flag=True,
    help="Whether to follow the log of the created job",
)
def submit(
    job_config_file: str,
    name: Optional[str],
    description: Optional[str],
    follow: Optional[bool],
) -> None:
    job_controller = JobController()
    id = job_controller.submit(job_config_file, name=name, description=description,)
    if follow:
        job_controller.logs(id, should_follow=follow)


@job_cli.command(name="list", help="Display information about existing jobs.")
@click.option("--name", "-n", required=False, default=None, help="Filter by job name.")
@click.option(
    "--job-id", "--id", required=False, default=None, help="Filter by job id."
)
@click.option(
    "--project-id", required=False, default=None, help="Filter by project id."
)
@click.option(
    "--include-all-users",
    is_flag=True,
    default=False,
    help="Include jobs not created by current user.",
)
@click.option(
    "--max-items",
    required=False,
    default=10,
    type=int,
    help="Max items to show in list.",
    callback=validate_non_negative_arg,
)
def list(
    name: Optional[str],
    job_id: Optional[str],
    project_id: Optional[str],
    include_all_users: bool,
    max_items: int,
) -> None:
    job_controller = JobController()
    job_controller.list(
        name=name,
        job_id=job_id,
        project_id=project_id,
        include_all_users=include_all_users,
        max_items=max_items,
    )


@job_cli.command(name="terminate", help="Attempt to terminate a job asynchronously.")
@click.option("--job-id", "--id", required=False, help="Id of job.")
@click.option("--name", "-n", required=False, help="Name of job.")
def terminate(job_id: Optional[str], name: Optional[str]) -> None:
    job_controller = JobController()
    job_controller.terminate(job_id=job_id, job_name=name)


@job_cli.command(name="logs", help="Print the logs of a job.")
@click.option("--job-id", "--id", required=False, help="Id of job.")
@click.option("--name", "-n", required=False, help="Name of job.")
@click.option(
    "--follow",
    "-f",
    required=False,
    default=False,
    type=bool,
    is_flag=True,
    help="Whether to follow the log.",
)
def logs(job_id: Optional[str], name: Optional[str], follow: bool = False,) -> None:
    job_controller = JobController()
    job_controller.logs(
        job_id=job_id, job_name=name, should_follow=follow,
    )
