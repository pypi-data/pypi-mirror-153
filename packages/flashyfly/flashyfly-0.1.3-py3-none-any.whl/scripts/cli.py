import typer
import flashyfly

app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]}, add_help_option=True, no_args_is_help=True)
app_project = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]}, add_help_option=True, no_args_is_help=True)
app.add_typer(app_project, name='project', help='Manage project dependencies.')

@app_project.command()
def init():
    """
    Initialize project directory tree.
    """
    try: 
        flashyfly.init()
        typer.echo('Project directory tree initialized.')
    except: 
        typer.echo('Project directory tree already initialized.')

@app.command()
def build():
    """
    Build binaries according to manifest file.
    """
    flashyfly.builder()
    typer.echo('Building finished.')

@app.command()
def flash():
    """
    Flash binaries according to availability.
    """
    flashyfly.flasher()
    typer.echo('Flashing finished.')

def main(): #if __name__ == "__main__":
    app()