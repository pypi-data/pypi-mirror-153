import os
import sys
import subprocess
import questionary
from rich.console import Console
from .. import get_home_dir
from .. import Config

console = Console()
config = Config()
home = get_home_dir()


def npm(repository: str, name: str):
    bundler = questionary.select("Bundler", choices=["Vite", "create-react-app"]).ask()
    if os.path.exists(os.path.join(home, repository, name)):
        console.print(f"[red]Project already exists![/]")
        sys.exit(1)
    if bundler == "Vite":
        os.chdir(os.path.join(get_home_dir(), repository))
        console.print("[green]Creating project with Vite, JavaScript and NPM[/]")
        if config.config["cli"]["display_output"]:
            subprocess.run(
                ["npm", "create", "vite@latest", name, "--", "--template", "react"],
                shell=True,
            )
        else:
            subprocess.run(
                ["npm", "create", "vite@latest", name, "--", "--template", "react"],
                shell=True,
                capture_output=True,
            )
        return
    else:
        os.chdir(os.path.join(home, repository))
        console.print(
            f"[green]Creating project with create-react-app, JavaScript and NPM[/]"
        )
        if config.config["cli"]["display_output"]:
            subprocess.run(
                ["npx", "create-react-app@latest", name],
                shell=True,
            )
        else:
            subprocess.run(
                ["npx", "create-react-app@latest", name],
                shell=True,
                capture_output=True,
            )
        return


def yarn(repository: str, name: str):
    bundler = questionary.select("Bundler", choices=["Vite", "create-react-app"]).ask()
    if os.path.exists(os.path.join(home, repository, name)):
        console.print(f"[red]Project already exists![/]")
        sys.exit(1)
    if bundler == "Vite":
        os.chdir(os.path.join(home, repository))
        console.print("[green]Creating project with Vite, JavaScript and Yarn[/]")
        if config.config["cli"]["display_output"]:
            subprocess.run(
                ["yarn", "create", "vite", name, "--template", "react"], shell=True
            )
        else:
            subprocess.run(
                ["yarn", "create", "vite", name, "--template", "react"],
                shell=True,
                capture_output=True,
            )
        return
    else:
        os.chdir(os.path.join(home, repository))
        console.print(
            f"[green]Creating project with create-react-app, JavaScript and Yarn[/]"
        )
        if config.config["cli"]["display_output"]:
            subprocess.run(
                ["yarn", "create", "react-app", name],
                shell=True,
            )
        else:
            subprocess.run(
                ["yarn", "create", "react-app", name],
                shell=True,
                capture_output=True,
            )
        return


def pnpm(repository: str, name: str):
    bundler = questionary.select("Bundler", choices=["Vite"]).ask()
    if os.path.exists(os.path.join(home, repository, name)):
        console.print(f"[red]Project already exists![/]")
        sys.exit(1)
    if bundler == "Vite":
        os.chdir(os.path.join(home, repository))
        console.print("[green]Creating project with Vite, JavaScript and Pnpm[/]")
        if config.config["cli"]["display_output"]:
            subprocess.run(
                ["pnpm", "create", "vite", name, "--", "--template", "react"],
                shell=True,
            )
        else:
            subprocess.run(
                ["pnpm", "create", "vite", name, "--", "--template", "react"],
                shell=True,
                capture_output=True,
            )
        return
