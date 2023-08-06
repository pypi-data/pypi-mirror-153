import typer
from .initer import initer
from .builder import builder
from .flasher import flasher
from .installer import installer

def start():
    app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]}, add_help_option=True, no_args_is_help=True)
    app_project = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]}, add_help_option=True, no_args_is_help=True)
    app_tools = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]}, add_help_option=True, no_args_is_help=True)
    
    app.add_typer(app_project, name='project', help='Manage project dependencies.')
    app.add_typer(app_tools, name='tools', help='Manage platform tools.')

    @app_project.command()
    def init():
        """
        Initialize project directory tree.
        """
        try: 
            initer()
            typer.echo('Project directory tree initialized.')
        except: 
            typer.echo('Project directory tree already initialized.')

    @app_tools.command()
    def install():
        """
        Install plaftorm tools.
        """
        installer()

    @app.command()
    def build():
        """
        Build binaries according to manifest file.
        """
        builder()
        typer.echo('Building finished.')

    @app.command()
    def flash(sensor_name : str = typer.Argument(None), sensor_spiffs_version : str = typer.Argument(None), sensor_sketch_version : str = typer.Argument(None)):
        """
        Flash binaries according to availability.
        """
        flasher(sensor_name, sensor_spiffs_version, sensor_sketch_version)
        typer.echo('Flashing finished.')


    app()