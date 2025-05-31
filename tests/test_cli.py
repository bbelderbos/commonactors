from typer.testing import CliRunner

from commonactors.actors import Movie
from commonactors.cli import app

runner = CliRunner()


def test_movies_cmd_found(monkeypatch):
    def fake_get_movies(self, actor_name):
        return [Movie("Test Movie", "2020-01-01")]

    monkeypatch.setattr("commonactors.actors.TMDbAPI.get_movies", fake_get_movies)

    result = runner.invoke(app, ["movies", "Tom Hanks"])
    assert result.exit_code == 0
    assert "Movies featuring Tom Hanks" in result.output
    assert "- Test Movie (2020-01-01)" in result.output


def test_movies_cmd_not_found(monkeypatch):
    monkeypatch.setattr("commonactors.actors.TMDbAPI.get_movies", lambda self, _: [])

    result = runner.invoke(app, ["movies", "Unknown Actor"])
    assert result.exit_code == 1
    assert "No movies found" in result.output


def test_common_cmd(monkeypatch):
    def fake_get_movies(self, actor_name):
        return {
            "A": [Movie("Shared", "2020-01-01"), Movie("UniqueA", "2019-01-01")],
            "B": [Movie("Shared", "2020-01-01"), Movie("UniqueB", "2018-01-01")],
        }[actor_name]

    monkeypatch.setattr("commonactors.actors.TMDbAPI.get_movies", fake_get_movies)

    result = runner.invoke(app, ["common", "A", "B"])
    assert result.exit_code == 0
    assert "🎬 Common movies between A and B" in result.output
    assert "- Shared (2020-01-01)" in result.output


def test_common_cmd_actor_missing(monkeypatch):
    monkeypatch.setattr("commonactors.actors.TMDbAPI.get_movies", lambda self, _: [])

    result = runner.invoke(app, ["common", "A", "B"])
    assert result.exit_code == 1
    assert "One or both actors not found" in result.output


def test_common_cmd_no_overlap(monkeypatch):
    def fake_get_movies(self, actor_name):
        return {
            "A": [
                Movie("OnlyA", "2020-01-01"),
            ],
            "B": [
                Movie("OnlyB", "2020-01-01"),
            ],
        }[actor_name]

    monkeypatch.setattr("commonactors.actors.TMDbAPI.get_movies", fake_get_movies)

    result = runner.invoke(app, ["common", "A", "B"])
    assert result.exit_code == 0
    assert "😕 No common movies found between A and B." in result.output
