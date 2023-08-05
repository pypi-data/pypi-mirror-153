"""Console script for ubuntu_ppa_package_version_report."""
import os
import sys
import click

import launchpadagent
from ubuntu_ppa_package_version_report import (
    get_ppa_published_binaries,
    get_ppa_sources,
)


@click.command()
@click.option(
    "--lp-credentials-store",
    envvar="LP_CREDENTIALS_STORE",
    required=False,
    help="An optional path to an already configured launchpad "
         "credentials store.",
    default=None,
    type=click.STRING,
)
@click.option(
    "--ppa",
    "ppas",
    help="PPA (Personal Package Archive) to use as the final "
         "source of the diff",
    required=True,
    multiple=True,
    type=click.STRING,
)
@click.option(
    "--series",
    help='the Ubuntu series eg. "20.04" or "focal"',
    required=True,
    type=click.STRING,
)
@click.option(
    "--binary-architecture",
    help="The architecture of the binary packages you are querying. "
    "The default is amd64",
    default="amd64",
    show_default=True,
    type=click.STRING,
)
@click.option(
    "--binary-versions",
    is_flag=True,
    default=False,
    help="Report on the binary versions as well as source package "
         "versions",
)
def main(lp_credentials_store, ppas, series, binary_architecture,
         binary_versions):
    """Console script for ubuntu_ppa_package_version_report."""
    cachedir_prefix = os.environ.get("SNAP_USER_COMMON", "/tmp")
    launchpad_cachedir = os.path.join(
        f"{cachedir_prefix}/ubuntu_ppa_package_version_report/.launchpadlib"
    )
    launchpad = launchpadagent.get_launchpad(
        launchpadlib_dir=launchpad_cachedir,
        lp_credentials_store=lp_credentials_store
    )
    ubuntu = launchpad.distributions["ubuntu"]
    lp_series = ubuntu.getSeries(name_or_version=series)
    lp_arch_series = lp_series.getDistroArchSeries(archtag=binary_architecture)
    for _ppa in ppas:
        _ppa_name = _ppa.split("/")[1]
        click.echo(_ppa_name)
        _sources = get_ppa_sources(launchpad, lp_series, _ppa)

        for _source in _sources:
            _source_package_name = _source.source_package_name
            _source_package_version = _source.source_package_version
            click.echo(f"\t{_source_package_name} - {_source_package_version}")

        if binary_versions:
            click.echo("\tPublished binaries:")
            _binaries = get_ppa_published_binaries(launchpad, lp_arch_series,
                                                   _ppa)
            # get current version for  package in the PPA
            for _binary in _binaries:
                _binary_package_name = _binary.binary_package_name
                _binary_package_version = _binary.binary_package_version
                click.echo(f"\t\t{_binary_package_name} - "
                           f"{_binary_package_version}")


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
