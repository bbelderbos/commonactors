import typer

from commonactors.actors import ActorService, TMDbAPI

app = typer.Typer()
api = TMDbAPI()
service = ActorService(api)


@app.command()
def movies(
    actor: str = typer.Argument(..., help="Actor name (e.g. 'Arnold Schwarzenegger')"),
):
    movies = service.get_movies_for_actor(actor)
    if movies:
        typer.echo(f"Movies featuring {actor}:")
        for movie in movies:
            typer.echo(f"- {movie.title} ({movie.released})")
    else:
        typer.secho(
            f"😕 No movies found for {actor}. Please check the name and try again.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)


@app.command()
def common(
    actor1: str = typer.Argument(
        ..., help="First actor name (e.g. 'Arnold Schwarzenegger')"
    ),
    actor2: str = typer.Argument(
        ..., help="Second actor name (e.g. 'Sylvester Stallone')"
    ),
):
    movies1 = service.get_movies_for_actor(actor1)
    movies2 = service.get_movies_for_actor(actor2)
    if not movies1 or not movies2:
        typer.secho(
            "😕 One or both actors not found. Please check the names and try again.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)

    typer.echo(f"🎞️  {actor1}: {len(movies1)} movies")
    typer.echo(f"🎞️  {actor2}: {len(movies2)} movies\n")

    common = service.common_movies(actor1, actor2)
    if common:
        typer.echo(f"\n🎬 Common movies between {actor1} and {actor2}:\n")
        for movie in common:
            typer.echo(f"- {movie.title} ({movie.released})")
    else:
        typer.echo(f"\n😕 No common movies found between {actor1} and {actor2}.")
