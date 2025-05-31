# 🎬 commonactors

Find common movies between two actors using [TMDb](https://www.themoviedb.org/) — CLI-first, testable, and fun.

## 🚀 Features

- Get all movies for an actor
- Find shared movies between two actors
- Filtered, sorted, and deduplicated results
- CLI powered by [Typer](https://typer.tiangolo.com/)
- Fully tested and type-checked (using `pytest`, `pytest-cov`, `ty`, `poethepoet`)

## 📦 Installation

```bash
git clone git@github.com:bbelderbos/commonactors.git
cd commonactors
uv sync
```

TODO: push to PyPI so people can use it with `uvx`.

## 🔧 Setup

Get a free TMDb API key at https://www.themoviedb.org/.

Then add it to your environment:

```bash
export TMDB_API_KEY=your_key_here
```

Or for local development, create a `.env` file in the project root:

```bash
$ cp .env-template .env
# add your TMDB API key in there
```

## 🖥️ CLI Usage

```bash
# List movies for an actor
commonactors movies "Brad Pitt"

# Find common movies between two actors
commonactors common "Tom Hanks" "Meg Ryan"
```

## 📈 Examples

```bash
$ uv run commonactors common "Brad Pitt" " Leonardo DiCaprio"
🎞️  Brad Pitt: 71 movies
🎞️   Leonardo DiCaprio: 35 movies


🎬 Common movies between Brad Pitt and  Leonardo DiCaprio:

- Once Upon a Time... in Hollywood (2019-07-24)

$ uv run commonactors common "Al Pacino" "Robert De Niro"
🎞️  Al Pacino: 63 movies
🎞️  Robert De Niro: 116 movies


🎬 Common movies between Al Pacino and Robert De Niro:

- The Irishman (2019-11-01)
- Righteous Kill (2008-09-11)
- Heat (1995-12-15)
- The Godfather Part II (1974-12-20)
```

## 🧪 Running Tests and Linting

```bash
uvx poe cov             # pytest with coverage
uvx poe tc              # run ty for static type checking

uvx pre-commit install  # install pre-commit hooks
```
