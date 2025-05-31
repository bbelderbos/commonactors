from commonactors.actors import ActorService


class FakeAPI:
    def get_movies(self, actor_name: str) -> list[str]:
        return ["Forrest Gump", "Cast Away", "Saving Private Ryan"]


def test_get_movies_for_actor():
    service = ActorService(api=FakeAPI())
    movies = service.get_movies_for_actor("Tom Hanks")
    assert "Forrest Gump" in movies


def test_common_movies():
    class StubAPI:
        def get_movies(self, actor_name: str) -> list[str]:
            return {
                "Actor A": ["Movie 1", "Movie 2"],
                "Actor B": ["Movie 2", "Movie 3"],
            }[actor_name]

    service = ActorService(api=StubAPI())
    commons = service.common_movies("Actor A", "Actor B")
    assert commons == ["Movie 2"]
