import grpc
from concurrent import futures
import movie_pb2
import movie_pb2_grpc
import json


class MovieServicer(movie_pb2_grpc.MovieServicer):

    def __init__(self):
        with open('{}/data/movies.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["movies"]

    def GetMovieByID(self, request, context):
        for movie in self.db:
            if movie['id'] == request.id:
                print("Movie found! Returning")
                return movie_pb2.MovieData(title=movie['title'], rating=movie['rating'], director=movie['director'],
                                           id=movie['id'])
        return movie_pb2.MovieData(title="", rating=0, director="", id="")

    def GetListMovies(self, request, context):
        for movie in self.db:
            yield movie_pb2.MovieData(title=movie['title'], rating=movie['rating'], director=movie['director'],
                                      id=movie['id'])

    def CreateMovie(self, request, context):
        movie = {
            "title": request.title,
            "rating": request.rating,
            "director": request.director,
            "id": request.id
        }
        self.db.append(movie)
        return movie_pb2.MovieData(title=request.title, rating=request.rating, director=request.director, id=request.id)

    def UpdateMovie(self,request,context):
        newMovie = {
            "title":request.title,
            "rating":request.rating,
            "director": request.director,
            "id": request.id
        }
        for movie in self.db:
            if movie['id'] == newMovie["id"]:
                movie['title']= newMovie['title']
                movie['rating']= newMovie['rating']
                movie['director']= newMovie['director']
                print("Movie found! Updated")
                return movie_pb2.MovieData(title=request.title, rating=request.rating, director=request.director, id=request.id);

    def DeleteMovie(self,request,context):
        for movie in self.db:
            if movie['id'] == request.id:
                self.db.remove(movie)
                print("Movie found! Deleted")
                return movie_pb2.MovieID(id=request.id);
        return movie_pb2.MovieID(id="")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    movie_pb2_grpc.add_MovieServicer_to_server(MovieServicer(), server)
    server.add_insecure_port('[::]:3001')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()