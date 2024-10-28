import typer
from click import Choice

from smsh.config import cfg
from smsh.handler import Handler
from smsh.role import SystemRole, DefaultRoles
from smsh.utils import run_command, get_smsh_version


def main(
        prompt: str = typer.Argument(
            "",
            show_default=False,
            help="The prompt to generate completions for.",
        ),
        model: str = typer.Option(
            cfg.get("DEFAULT_MODEL"),
            help="Large language model to use.",
        ),
        temperature: float = typer.Option(
            0.0,
            min=0.0,
            max=2.0,
            help="Randomness of generated output.",
        ),
        top_p: float = typer.Option(
            1.0,
            min=0.0,
            max=1.0,
            help="Limits highest probable tokens (words).",
        ),
        md: bool = typer.Option(
            cfg.get("PRETTIFY_MARKDOWN") == "true",
            help="Prettify markdown output.",
        ),
        shell: bool = typer.Option(
            True,
            "--shell",
            "-s",
            help="Generate and execute shell commands.",
            rich_help_panel="Assistance Options",
        ),
        interaction: bool = typer.Option(
            False,
            "--interaction",
            "-i",
            help="Interactive mode for --shell option.",
            rich_help_panel="Assistance Options",
        ),
        describe_shell: bool = typer.Option(
            False,
            "--describe-shell",
            "-d",
            help="Describe a shell command.",
            rich_help_panel="Assistance Options",
        ),
        role: str = typer.Option(
            None,
            help="System role for GPT model.",
            rich_help_panel="Role Options",
        ),
        create_role: str = typer.Option(
            None,
            help="Create role.",
            callback=SystemRole.create,
            rich_help_panel="Role Options",
        ),
        show_role: str = typer.Option(
            None,
            help="Show role.",
            callback=SystemRole.show,
            rich_help_panel="Role Options",
        ),
        list_roles: bool = typer.Option(
            False,
            "--list-roles",
            "-lr",
            help="List roles.",
            callback=SystemRole.list,
            rich_help_panel="Role Options",
        ),
        version: bool = typer.Option(
            False,
            "--version",
            help="Show version.",
            callback=get_smsh_version,
        ),
        config_mode: bool = typer.Option(
            False,
            "-c",
            "--config",
            help="Enter configuration edit mode.",
            rich_help_panel="Assistance Options",
        ),
) -> None:

    if prompt == "" or config_mode:
        typer.echo("Entering configuration mode.")
        typer.echo("Current configuration:")
        for key, value in cfg.items():
            typer.echo(f"{key} = {value}")
        key = typer.prompt("Enter the config key you want to edit, or press 'q' to exit.")
        if key == "q":
            raise typer.Exit()
        value = typer.prompt(f"Enter the new value for {key}")
        cfg.edit(key, value)
        typer.echo(f"Configuration for {key} has been updated to {value}")
        raise typer.Exit()

    role_class = (
        DefaultRoles.check_get(shell, describe_shell)
        if not role
        else SystemRole.get(role)
    )

    if describe_shell:
        Handler(DefaultRoles.DESCRIBE_SHELL.get_role(), md).handle(
            prompt=prompt,
            model=model,
            temperature=temperature,
            top_p=top_p
        )
        raise typer.Exit()

    full_completion = Handler(role_class, md).handle(
        prompt=prompt,
        model=model,
        temperature=temperature,
        top_p=top_p
    )

    while shell:
        option = typer.prompt(
            text="[E]xecute, [D]escribe, [C]ancel, [Q]uit",
            type=Choice(("e", "d", "c", "q"), case_sensitive=False),
            default="e" if cfg.get("DEFAULT_EXECUTE_SHELL_CMD") == "true" else "c",
            show_choices=False,
            show_default=False,
        )
        if option == "e":
            run_command(full_completion)
        elif option == "d":
            Handler(DefaultRoles.DESCRIBE_SHELL.get_role(), md).handle(
                full_completion,
                model=model,
                temperature=temperature,
                top_p=top_p
            )
            continue
        elif option == "q":
            break
        if interaction:
            option = typer.prompt(
                text="Enter a new prompt or [Q]uit",
                show_choices=False,
                default="q",
                show_default=False,
            )
            if option == "q":
                break
            full_completion = Handler(role_class, md).handle(
                option,
                model=model,
                temperature=temperature,
                top_p=top_p
            )
        else:
            break


def entry() -> None:
    typer.run(main)


if __name__ == '__main__':
    entry()

