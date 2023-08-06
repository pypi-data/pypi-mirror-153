# STDLIB
import sys
from typing import Optional

# EXT
import click

# OWN
import cli_exit_tools

# PROJ
try:
    from . import __init__conf__
    from . import lib_cicd_github
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    # imports for doctest
    import __init__conf__  # type: ignore  # pragma: no cover
    import lib_cicd_github  # type: ignore  # pragma: no cover

# CONSTANTS
CLICK_CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])
# CLICK_CONTEXT_SETTINGS_RUN = dict(help_option_names=['-h', '--help'], ignore_unknown_options=True)


def info() -> None:
    """
    >>> info()
    Info for ...

    """
    __init__conf__.print_info()


@click.group(help=__init__conf__.title, context_settings=CLICK_CONTEXT_SETTINGS)
@click.version_option(
    version=__init__conf__.version,
    prog_name=__init__conf__.shell_command,
    message=f"{__init__conf__.shell_command} version {__init__conf__.version}",
)
@click.option(
    "--traceback/--no-traceback",
    is_flag=True,
    type=bool,
    default=None,
    help="return traceback information on cli",
)
def cli_main(traceback: Optional[bool] = None) -> None:
    if traceback is not None:
        cli_exit_tools.config.traceback = traceback


@cli_main.command("info", context_settings=CLICK_CONTEXT_SETTINGS)  # type: ignore
def cli_info() -> None:
    """get program informations"""
    info()


@cli_main.command("get_branch", context_settings=CLICK_CONTEXT_SETTINGS)  # type: ignore
def cli_get_branch() -> None:
    """get the branch to work on"""
    response = lib_cicd_github.get_branch()
    print(response)


@cli_main.command("run", context_settings=CLICK_CONTEXT_SETTINGS)  # type: ignore
@click.option("-r", "--retry", type=int, default=3, help="retry in case of failure, default=3")
@click.option("-s", "--sleep", type=int, default=30, help="seconds to sleep on repeat, default=30")
@click.option("--banner/--no-banner", default=True, help="use Banners, default=True")
@click.argument("description")
@click.argument("command")
def cli_run(description: str, command: str, retry: int, sleep: int, banner: bool) -> None:
    """run string command wrapped in run/success/error banners"""
    lib_cicd_github.run(description, command, retry=retry, sleep=sleep, banner=banner)


@cli_main.command("install", context_settings=CLICK_CONTEXT_SETTINGS)  # type: ignore
@click.option("--dry-run", is_flag=True, default=False, help="dry run")
def cli_install(dry_run: bool) -> None:
    """updates pip, setuptools, wheel, pytest-pycodestyle"""
    lib_cicd_github.install(dry_run)


@cli_main.command("script", context_settings=CLICK_CONTEXT_SETTINGS)  # type: ignore
@click.option("--dry-run", is_flag=True, default=False, help="dry run")
def cli_script(dry_run: bool) -> None:
    """updates pip, setuptools, wheel, pytest-pycodestyle"""
    lib_cicd_github.script(dry_run)


@cli_main.command("after_success", context_settings=CLICK_CONTEXT_SETTINGS)  # type: ignore
@click.option("--dry-run", is_flag=True, default=False, help="dry run")
def cli_after_success(dry_run: bool) -> None:
    """coverage reports"""
    lib_cicd_github.after_success(dry_run)


@cli_main.command("deploy", context_settings=CLICK_CONTEXT_SETTINGS)  # type: ignore
@click.option("--dry-run", is_flag=True, default=False, help="dry run")
def cli_deploy(dry_run: bool) -> None:
    """deploy on pypi"""
    lib_cicd_github.deploy(dry_run)


# entry point if main
if __name__ == "__main__":
    try:
        cli_main()
    except Exception as exc:
        cli_exit_tools.print_exception_message()
        sys.exit(cli_exit_tools.get_system_exit_code(exc))
    finally:
        cli_exit_tools.flush_streams()
