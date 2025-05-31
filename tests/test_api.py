from commonactors.actors import Movie, TMDbAPI


class MockResponse:
    def __init__(self, json_data):
        self._json = json_data

    def json(self):
        return self._json


def test_search_person_found(monkeypatch):
    def mock_get(url, params):
        return MockResponse({"results": [{"id": 123, "name": "Test Actor"}]})

    monkeypatch.setattr("httpx.get", mock_get)

    api = TMDbAPI("fake-key")
    result = api._search_person("Test Actor")
    assert result is not None
    assert result["id"] == 123


def test_search_person_not_found(monkeypatch):
    monkeypatch.setattr("httpx.get", lambda *a, **kw: MockResponse({"results": []}))

    api = TMDbAPI("fake-key")
    result = api._search_person("Ghost Actor")
    assert result is None


def test_get_movie_credits(monkeypatch):
    monkeypatch.setattr(
        "httpx.get",
        lambda *a, **kw: MockResponse(
            {"cast": [{"title": "X", "release_date": "2020-01-01"}]}
        ),
    )

    api = TMDbAPI("fake-key")
    result = api._get_movie_credits(123)
    assert result == [{"title": "X", "release_date": "2020-01-01"}]


def test_get_movies_filters_and_sorts(monkeypatch):
    # Chain both calls in one mock setup
    def mock_get(url, params):
        if "search" in url:
            return MockResponse({"results": [{"id": 1}]})
        elif "movie_credits" in url:
            return MockResponse(
                {
                    "cast": [
                        {"title": "B", "release_date": "2020-01-01"},
                        {"title": "A", "release_date": "2021-01-01"},
                        {"title": None, "release_date": "2022-01-01"},
                        {"title": "C", "release_date": None},
                    ]
                }
            )

    monkeypatch.setattr("httpx.get", mock_get)

    api = TMDbAPI("fake-key")
    movies = api.get_movies("Anyone")
    assert movies == [
        Movie("A", "2021-01-01"),
        Movie("B", "2020-01-01"),
    ]


def test_get_movies_returns_empty_if_no_person(monkeypatch):
    def mock_get(url, params):
        return MockResponse({"results": []})  # triggers early return

    monkeypatch.setattr("httpx.get", mock_get)

    api = TMDbAPI("fake-key")
    movies = api.get_movies("Nonexistent Person")
    assert movies == []
