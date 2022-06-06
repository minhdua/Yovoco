import typer

def emphasize(text: str):
    index = text.find(":")
    if index > -1:
        label = text[:index+1]
        value = text[index+1:] 
        label = typer.style(label, fg=typer.colors.MAGENTA, bold=True)
    typer.echo(label + value)
    