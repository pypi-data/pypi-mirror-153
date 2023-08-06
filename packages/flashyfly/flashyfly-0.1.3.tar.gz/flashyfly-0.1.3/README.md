# Flashyfly

Flashyfly package to build and flash firmware in production environment working as a CLI wrapper for Platformio objecting ease of use and speed to deploy firmware in a hardware platform.

<p align="center">
    <img src="img/flashyfly.png" alt="drawing" style="width:300px;" />
</p>

---

## Usage

The package can be installed with `pip`:

```
$ pip install flashyfly
```

Also can be built from source with the `setup.py` file:

```
$ python setup.py install
```

After the installation the CLI script can be invoked using the command:

```
$ flashyfly -h
Usage: flashyfly [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  -h, --help                      Show this message and exit.

Commands:
  build    Build binaries according to manifest file.
  flash    Flash binaries according to availability.
  project  Manage project dependencies.
```

