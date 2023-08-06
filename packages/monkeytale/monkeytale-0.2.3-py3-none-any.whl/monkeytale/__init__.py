import click

__version__ = "0.2.3"


@click.command()
@click.version_option(version=__version__)
def cli():
    click.echo(f"{__file__}!")


if __name__ == "__main__":
    cli()
