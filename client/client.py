import grpc

import movie_pb2
import movie_pb2_grpc
import showtime_pb2_grpc
import showtime_pb2


def get_movie_by_id(stub, id):
    movie = stub.GetMovieByID(id)
    print(movie)
    return movie


def get_list_movies(stub):
    allmovies = stub.GetListMovies(movie_pb2.Empty())
    for movie in allmovies:
        print("Movie called %s" % (movie.title))


def create_movie(stub, title, rating, director, id):
    movie = stub.CreateMovie(movie_pb2.MovieData(title=title, rating=rating, director=director, id=id))
    print(movie)


def update_movie(stub, title, rating, director, id):
    movie = stub.UpdateMovie(movie_pb2.MovieData(title=title, rating=rating, director=director, id=id))
    print(movie)


def delete_movie(stub, id):
    print("hello")
    movie = stub.DeleteMovie(id)
    print(movie)


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:3001') as channel:
        stub = movie_pb2_grpc.MovieStub(channel)

        print("-------------- GetMovieByID --------------")
        movieid = movie_pb2.MovieID(id="a8034f44-aee4-44cf-b32c-74cf452aaaae")
        get_movie_by_id(stub, movieid)

        print("-------------- GetListMovies --------------")
        get_list_movies(stub)

        print("-------------- CreateMovie --------------")
        create_movie(stub, "The Matrix", 5, "Wachowski", "a8034f44-aee4-44cf-b32c-74cf452aaaae")

        print("-------------- UpdateMovie --------------")
        update_movie(stub, "The Matrix", 5, "Wachowsk", "a8034f44-aee4-44cf-b32c-74cf452aaaae")

        print("-------------- DeleteMovie --------------")
        movieid=movie_pb2.MovieID(id="a8034f44-aee4-44cf-b32c-74cf452aaaae")
        delete_movie(stub, movieid)

    channel.close()

    with grpc.insecure_channel('localhost:3002') as channel:
        stub = showtime_pb2_grpc.ShowtimeStub(channel)

        print("-------------- GetMovieByDate --------------")
        date = showtime_pb2.Date(date="20151130")
        movie = stub.GetMovieByDate(date)
        print(movie)

        print("-------------- GetListSchedule --------------")
        allSchedule = stub.GetListSchedule(showtime_pb2.EmptyS())
        print(allSchedule)
        for schedule in allSchedule:
            print(schedule.date)
            print(schedule.movies)
    channel.close()


if __name__ == '__main__':
    run()
