from commonactors.actors import ActorService, Movie, MovieAPI


class FakeAPI(MovieAPI):
    def get_movies(self, actor_name: str) -> list[Movie]:
        match actor_name:
            case "Tom Hanks":
                return [
                    Movie("Forrest Gump", "1994-07-06"),
                    Movie("Cast Away", "2000-12-22"),
                    Movie("Saving Private Ryan", "1998-07-24"),
                ]
            case "Meg Ryan":
                return [
                    Movie("Sleepless in Seattle", "1993-06-25"),
                    Movie("You've Got Mail", "1998-12-18"),
                    Movie("Joe Versus the Volcano", "1990-03-09"),
                    Movie("Forrest Gump", "1994-07-06"),  # intentionally shared
                ]
            case _:
                return []


def test_get_movies_for_actor():
    service = ActorService(api=FakeAPI())
    movies = service.get_movies_for_actor("Tom Hanks")
    assert Movie("Forrest Gump", "1994-07-06") in movies


def test_common_movies():
    service = ActorService(api=FakeAPI())
    commons = service.common_movies("Tom Hanks", "Meg Ryan")
    assert commons == [Movie("Forrest Gump", "1994-07-06")]
