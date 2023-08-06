import typing

from .common import CAPI
from ._ffi import ffi;

class GraphANNISException(Exception):
    def __init__(self, msg : str, cause: Exception = None):
        self.message = msg
        self.__cause__ = cause

    def __str__(self):
        return self.message

class SetLoggerError(GraphANNISException):
    def __init__(self, msg : str, cause : GraphANNISException = None):
        GraphANNISException.__init__(self, msg, cause)

class AQLSemanticError(GraphANNISException):
    def __init__(self, msg : str,  cause : GraphANNISException = None):
        GraphANNISException.__init__(self, msg, cause)

class AQLSyntaxError(GraphANNISException):
    def __init__(self, msg : str,  cause : GraphANNISException = None):
        GraphANNISException.__init__(self, msg, cause)

class NoSuchCorpus(GraphANNISException):
    def __init__(self, msg : str,  cause : GraphANNISException = None):
        GraphANNISException.__init__(self, msg, cause)



def consume_errors(err):
    """ Processes the error list from the C-API and raises an exception if they contain an error.
    It also deletes the memory if the vector has been filled.
    """ 
    if err != ffi.NULL and err[0] != ffi.NULL:
        num_of_errors = CAPI.annis_error_size(err[0])

        cause : GraphANNISException = None        
        if num_of_errors > 0:

            # iterate of the list of all causes, rewinding the causes and
            # getting to the first exception that
            # is the main exception

            for i in reversed(range(0, num_of_errors)):
                msg = ffi.string(CAPI.annis_error_get_msg(err[0], i)).decode('utf-8')
                kind = ffi.string(CAPI.annis_error_get_kind(err[0], i)).decode('utf-8')

                if kind == "SetLoggerError":
                    cause = SetLoggerError(msg, cause)
                elif kind == "AQLSemanticError":
                    cause = AQLSemanticError(msg, cause)
                elif kind == "AQLSyntaxError":
                    cause = AQLSyntaxError(msg, cause)
                elif kind == "NoSuchCorpus":
                    cause = NoSuchCorpus(msg, cause)
                else:
                    cause = GraphANNISException(msg, cause)
        CAPI.annis_free(err[0])

        if cause != None:
            # finally raise the root cause    
            raise cause # pylint: disable-msg=E0702
    
