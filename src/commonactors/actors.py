from typing import NamedTuple, Protocol

import httpx
from decouple import config

TMDB_API_KEY = config("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"


class Movie(NamedTuple):
    title: str
    released: str


class MovieAPI(Protocol):
    def get_movies(self, actor_name: str) -> list[Movie]: ...


class TMDbAPI(MovieAPI):
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or TMDB_API_KEY

    def _is_valid_movie(self, m: dict) -> bool:
        return bool(
            m.get("title")
            and m.get("release_date")
            and not m.get("video", False)
            and m.get("media_type", "movie") == "movie"
            and m.get("character") not in {"Self", "Himself", "Herself"}
            and 99 not in m.get("genre_ids", [])  # genre 99 = Documentary
            and "making" not in m["title"].lower()
            and "conversation" not in m["title"].lower()
            and "look inside" not in m["title"].lower()
            and "in concert" not in m["title"].lower()
            and "final cut" not in m["title"].lower()
        )

    def get_movies(self, actor_name: str) -> list[Movie]:
        person = self._search_person(actor_name)
        if not person:
            return []

        credits = self._get_movie_credits(person["id"])
        movies = [
            Movie(m["title"], m["release_date"])
            for m in credits
            if self._is_valid_movie(m)
        ]
        return sorted(movies, key=lambda m: m.released, reverse=True)

    def _search_person(self, name: str) -> dict | None:
        resp = httpx.get(
            f"{BASE_URL}/search/person",
            params={"api_key": self.api_key, "query": name},
        )
        data = resp.json()
        return data["results"][0] if data["results"] else None

    def _get_movie_credits(self, person_id: int) -> list[dict]:
        resp = httpx.get(
            f"{BASE_URL}/person/{person_id}/movie_credits",
            params={"api_key": self.api_key},
        )
        return resp.json().get("cast", [])


class ActorService:
    def __init__(self, api: MovieAPI | None = None):
        self.api = api or TMDbAPI()

    def get_movies_for_actor(self, name: str) -> list[Movie]:
        return self.api.get_movies(name)

    def common_movies(self, actor1: str, actor2: str) -> list[Movie]:
        movies1 = {m.title: m for m in self.get_movies_for_actor(actor1)}
        movies2 = {m.title: m for m in self.get_movies_for_actor(actor2)}
        common_titles = movies1.keys() & movies2.keys()
        return sorted(
            [movies1[t] for t in common_titles], key=lambda m: m.released, reverse=True
        )
