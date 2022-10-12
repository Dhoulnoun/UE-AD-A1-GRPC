# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import showtime_pb2 as showtime__pb2


class ShowtimeStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetListSchedule = channel.unary_stream(
                '/Showtime/GetListSchedule',
                request_serializer=showtime__pb2.EmptyS.SerializeToString,
                response_deserializer=showtime__pb2.ScheduleData.FromString,
                )
        self.GetMovieByDate = channel.unary_unary(
                '/Showtime/GetMovieByDate',
                request_serializer=showtime__pb2.Date.SerializeToString,
                response_deserializer=showtime__pb2.ScheduleData.FromString,
                )


class ShowtimeServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetListSchedule(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetMovieByDate(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ShowtimeServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetListSchedule': grpc.unary_stream_rpc_method_handler(
                    servicer.GetListSchedule,
                    request_deserializer=showtime__pb2.EmptyS.FromString,
                    response_serializer=showtime__pb2.ScheduleData.SerializeToString,
            ),
            'GetMovieByDate': grpc.unary_unary_rpc_method_handler(
                    servicer.GetMovieByDate,
                    request_deserializer=showtime__pb2.Date.FromString,
                    response_serializer=showtime__pb2.ScheduleData.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Showtime', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Showtime(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetListSchedule(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/Showtime/GetListSchedule',
            showtime__pb2.EmptyS.SerializeToString,
            showtime__pb2.ScheduleData.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetMovieByDate(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Showtime/GetMovieByDate',
            showtime__pb2.Date.SerializeToString,
            showtime__pb2.ScheduleData.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)