import typing
from enum import IntEnum
from collections import namedtuple
import networkx as nx

from .common import CAPI
from ._ffi import ffi
from .graph import _map_graph as map_graph
from .errors import consume_errors


class ResultOrder(IntEnum):
    """ Defines the ordering of results"""
    Normal = 0
    Inverted = 1
    Randomized = 2
    NotSorted = 3


class QueryLanguage(IntEnum):
    """ Defines which query language is used """
    AQL = 0
    """ Default ANNIS Query Language (AQL)"""
    AQLQuirksV3 = 1
    """ AQL in quirks mode that emulates some of the behavior of ANNIS3 """


class ImportFormat(IntEnum):
    """An enum of all supported input formats of graphANNIS."""
    RelANNIS = 0
    """Legacy relANNIS import file format: http://korpling.github.io/ANNIS/4.0/developer-guide/annisimportformat.html"""
    GraphML = 1
    """GraphML (http://graphml.graphdrawing.org/) based export-format, suitable to be imported from other graph databases.
    This format follows the extensions/conventions of the Neo4j GraphML module (https://neo4j.com/docs/labs/apoc/current/import/graphml/)."""


class ExportFormat(IntEnum):
    """An enum of all supported output formats of graphANNIS."""
    GraphML = 0
    """ GraphML (http://graphml.graphdrawing.org/) based export-format, suitable to be imported into other graph databases.
    This format follows the extensions/conventions of the Neo4j GraphML module (https://neo4j.com/docs/labs/apoc/current/import/graphml/)."""
    GraphMLZip = 1
    """Like **GraphML**, but compressed as ZIP file. Linked files are also copied into the ZIP file."""
    GraphMLDirectory = 2
    """Like **GraphML**, but using a directory with multiple GraphML files, each for one corpus."""


FrequencyTableEntry = namedtuple("FrequencyTableEntry", "values count")

CountExtra = namedtuple("CountExtra", "match_count document_count")


class CorpusStorageManager:
    def __init__(self, db_dir='data/', use_parallel=True):
        err = ffi.new("AnnisErrorList **")
        self.__cs = CAPI.annis_cs_with_auto_cache_size(
            db_dir.encode('utf-8'), use_parallel, err)
        consume_errors(err)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        CAPI.annis_cs_free(self.__cs)
        self.__cs = ffi.NULL

    def list(self):
        """ List all available corpora in the corpus storage. """
        if self.__cs is None or self.__cs == ffi.NULL:
            return None

        err = ffi.new("AnnisErrorList **")
        orig = CAPI.annis_cs_list(self.__cs, err)
        consume_errors(err)

        orig_size = int(CAPI.annis_vec_str_size(orig))

        copy = []
        for idx, _ in enumerate(range(orig_size)):
            corpus_name = ffi.string(CAPI.annis_vec_str_get(orig, idx))
            copy.append(corpus_name.decode('utf-8'))
        return copy

    def count(self, corpus_name, query: str, query_language=QueryLanguage.AQL) -> int:
        """ Count the number of results for a query.

        :param corpus_name: The name of the corpus to execute the query on. This can be a string or a list of strings.
        :param query:  The query as string.
        :param query_language: The query language of the query (e.g. AQL).
        :return: The count of matches as number.
        """
        if self.__cs is None or self.__cs == ffi.NULL:
            return None

        result = int(0)

        c_corpus_list = CAPI.annis_vec_str_new()
        if isinstance(corpus_name, str):
            CAPI.annis_vec_str_push(c_corpus_list, corpus_name.encode('utf-8'))
        else:
            for c in corpus_name:
                CAPI.annis_vec_str_push(c_corpus_list, c.encode('utf-8'))

        err = ffi.new("AnnisErrorList **")
        result = result + CAPI.annis_cs_count(self.__cs, c_corpus_list,
                                              query.encode('utf-8'), int(query_language), err)

        CAPI.annis_free(c_corpus_list)

        consume_errors(err)

        return result

    def count_extra(self, corpus_name, query: str, query_language=QueryLanguage.AQL) -> CountExtra:
        """ Count the number of results for a `query` and return both the total number of matches and also the number of documents in the result set.

        :param corpus_name: The name of the corpus to execute the query on. This can be a string or a list of strings
        :param query:  The query as string.
        :param query_language: The query language of the query (e.g. AQL).
        :return: The count of matches and documents.
        """
        if self.__cs is None or self.__cs == ffi.NULL:
            return None

        c_corpus_list = CAPI.annis_vec_str_new()
        if isinstance(corpus_name, str):
            CAPI.annis_vec_str_push(c_corpus_list, corpus_name.encode('utf-8'))
        else:
            for c in corpus_name:
                CAPI.annis_vec_str_push(c_corpus_list, c.encode('utf-8'))

        err = ffi.new("AnnisErrorList **")
        result = CAPI.annis_cs_count_extra(self.__cs, c_corpus_list,
                                           query.encode('utf-8'), int(query_language), err)

        CAPI.annis_free(c_corpus_list)

        consume_errors(err)

        return CountExtra(match_count=result.match_count, document_count=result.document_count)

    def find(self, corpus_name, query: str, query_language=QueryLanguage.AQL, offset=0, limit=10, order: ResultOrder = ResultOrder.Normal):
        """Find all results for a `query` and return the match ID for each result.

        :param corpus_name: The name of the corpus to execute the query on. This can be a string or a list of strings.
        :param query: The query as string.
        :param query_language: The query language of the query (e.g. AQL).
        :param offset: Skip the `n` first results, where `n` is the offset.
        :param limit: Return at most `n` matches, where `n` is the limit.
        :param order: Specify the order of the matches.
        :return: A list of match IDs, where each match ID consists of the matched node annotation identifiers separated by spaces.
                You can use the :py:meth:`subgraph` method to get the subgraph for a single match described by the node annnotation identifiers.
        """
        if self.__cs is None or self.__cs == ffi.NULL:
            return None

        result = []
        err = ffi.new("AnnisErrorList **")

        c_corpus_list = CAPI.annis_vec_str_new()
        if isinstance(corpus_name, str):
            CAPI.annis_vec_str_push(c_corpus_list, corpus_name.encode('utf-8'))
        else:
            for c in corpus_name:
                CAPI.annis_vec_str_push(c_corpus_list, c.encode('utf-8'))

        limit_ptr = ffi.NULL
        if limit is not None:
            limit_ptr = ffi.new("size_t *")
            limit_ptr[0] = limit

        vec = CAPI.annis_cs_find(self.__cs, c_corpus_list,
                                 query.encode(
                                     'utf-8'), int(query_language),
                                 offset, limit_ptr, int(order), err)

        CAPI.annis_free(c_corpus_list)

        consume_errors(err)

        vec_size = CAPI.annis_vec_str_size(vec)
        for i in range(vec_size):
            result_str = ffi.string(
                CAPI.annis_vec_str_get(vec, i)).decode('utf-8')
            result.append(result_str.split())
        return result

    def frequency(self, corpus_name, query, definition, query_language=QueryLanguage.AQL):
        """ Execute a frequency query.

        :param corpus_name: The name of the corpus. This can be a string or a list of strings.
        :param query:       Query in the specified query language (per default AQL)
        :param definition:  A comma seperated list of single frequency definition items as string.
                            Each frequency definition must consist of two parts: the name of referenced node and the (possible qualified) annotation name or "tok" separated by ":".
                            E.g. a frequency definition like::

                                1:tok,3:pos,4:tiger::pos

                            #1, the pos annotation for node #3 and the
                            would extract the token value for the node
                            pos annotation in the tiger namespace for node #4.
        :param query_language: Optional query language (AQL per default)
        :return: A frequency table which is a list of named tuples. The named tuples have the field **values** which is a list
                 with the actual values for this entry and **count** with the number of occurences for these value combination.
        """
        if self.__cs is None or self.__cs == ffi.NULL:
            return None

        err = ffi.new("AnnisErrorList **")

        c_corpus_list = CAPI.annis_vec_str_new()
        if isinstance(corpus_name, str):
            CAPI.annis_vec_str_push(c_corpus_list, corpus_name.encode('utf-8'))
        else:
            for c in corpus_name:
                CAPI.annis_vec_str_push(c_corpus_list, c.encode('utf-8'))

        ft = CAPI.annis_cs_frequency(self.__cs, c_corpus_list,
                                     query.encode('utf-8'), int(query_language), definition.encode('utf-8'), err)

        CAPI.annis_free(c_corpus_list)
        consume_errors(err)

        # return a list containing a tuple (the different values) and their count
        result = []
        ncols = CAPI.annis_freqtable_str_ncols(ft)
        for i in range(0, CAPI.annis_freqtable_str_nrows(ft)):
            values = []
            for j in range(0, ncols):
                v = ffi.string(CAPI.annis_freqtable_str_get(ft, i, j))
                values.append(v.decode('utf-8'))
            entry = FrequencyTableEntry(
                values=values, count=CAPI.annis_freqtable_str_count(ft, i))
            result.append(entry)

        return result

    def subgraph(self, corpus_name: str, node_ids, ctx_left=0, ctx_right=0, segmentation=None) -> nx.MultiDiGraph:
        """ Return the copy of a subgraph which includes the given list of node annotation identifiers,
        the nodes that cover the same token as the given nodes and all nodes that cover the token
        which are part of the defined context.

        :param corpus_name: The name of the corpus for which the subgraph should be generated from.
        :param node_ids: A list of node annotation identifiers describing the subgraph.
        :param ctx_left: Left context in token distance to be included in the subgraph.
        :param ctx_right: Right context in token distance to be included in the subgraph.
        :param segmentation: The name of the segmentation which should be used to as base for the context.
         * 					   Use `None` to define the context in the default token layer.

        """
        if self.__cs is None or self.__cs == ffi.NULL:
            return None

        c_node_ids = CAPI.annis_vec_str_new()
        for nid in node_ids:
            CAPI.annis_vec_str_push(c_node_ids, nid.encode('utf-8'))

        err = ffi.new("AnnisErrorList **")
        db = CAPI.annis_cs_subgraph(self.__cs, corpus_name.encode('utf-8'),
                                    c_node_ids, ctx_left, ctx_right,
                                    ffi.NULL if segmentation == None else segmentation.encode(
                                        'utf-8'),
                                    err)
        consume_errors(err)

        G = map_graph(db)

        CAPI.annis_free(db)
        CAPI.annis_free(c_node_ids)

        return G

    def subcorpus_graph(self, corpus_name: str, document_ids) -> nx.MultiDiGraph:
        """ Return the copy of a subgraph which includes all nodes that belong to any of the given list of sub-corpus/document identifiers.
        :param corpus_name:  The name of the corpus for which the subgraph should be generated from.
        :param document_ids: A list of sub-corpus/document identifiers describing the subgraph.
        """
        if self.__cs is None or self.__cs == ffi.NULL:
            return None

        c_document_ids = CAPI.annis_vec_str_new()
        for id in document_ids:
            CAPI.annis_vec_str_push(c_document_ids, id.encode('utf-8'))

        err = ffi.new("AnnisErrorList **")
        db = CAPI.annis_cs_subcorpus_graph(self.__cs, corpus_name.encode('utf-8'),
                                           c_document_ids, err)
        consume_errors(err)

        G = map_graph(db)

        CAPI.annis_free(db)
        CAPI.annis_free(c_document_ids)

        return G

    def apply_update(self, corpus_name: str, update):
        """ Apply a sequence of updates (`update` parameter) to this graph for a corpus given by the `corpus_name` parameter.

        It is ensured that the update process is atomic and that the changes are persisted to disk if the no exceptions are thrown.

        :param corpus_name: The name of the corpus to apply the update on.
        :param update: List with elements of the type :py:class:`graphannis.graph.GraphUpdate`.

        >>> from graphannis.cs import CorpusStorageManager
        >>> from graphannis.graph import GraphUpdate
        >>> with CorpusStorageManager() as cs:
        ...     with GraphUpdate() as g:
        ...         g.add_node('n1')
        ...         cs.apply_update('test', g)
        """

        err = ffi.new("AnnisErrorList **")
        CAPI.annis_cs_apply_update(self.__cs,
                                   corpus_name.encode('utf-8'), update._get_instance(), err)
        consume_errors(err)

    def delete_corpus(self, corpus_name: str):
        """ Delete a corpus from the database

        >>> from graphannis.cs import CorpusStorageManager
        >>> from graphannis.graph import GraphUpdate
        >>> with CorpusStorageManager() as cs:
        ...     # create a corpus named "test"
        ...     with GraphUpdate() as g:
        ...         g.add_node('anynode')
        ...         cs.apply_update('test', g)
        ...     # delete it
        ...     cs.delete_corpus('test')
        True
        """
        if self.__cs is None or self.__cs == ffi.NULL:
            return None

        err = ffi.new("AnnisErrorList **")
        result = CAPI.annis_cs_delete(
            self.__cs, corpus_name.encode('utf-8'), err)
        consume_errors(err)
        return result

    def import_from_fs(self, path, fmt: ImportFormat = ImportFormat.RelANNIS, corpus_name: str = None, disk_based: bool = False, overwrite_existing: bool = False):
        """ Import corpus from the file system into the database

        >>> from graphannis.cs import CorpusStorageManager
        >>> from graphannis.graph import GraphUpdate
        >>> with CorpusStorageManager() as cs:
        ...     # import relANNIS corpus with automatic name
        ...     corpus_name = cs.import_from_fs("relannis/GUM")
        ...     print(corpus_name)
        ...     # import a GraphML corpus with a different name
        ...     corpus_name = cs.import_from_fs("examples/tutorial.graphml", ImportFormat.GraphML, "example")
        ...     print(corpus_name)
        GUM
        example
        """
        if self.__cs is None or self.__cs == ffi.NULL:
            return None

        err = ffi.new("AnnisErrorList **")
        if corpus_name is None:
            corpus_name = ffi.NULL
        else:
            corpus_name = corpus_name.encode('utf-8')
        imported_corpus_name = CAPI.annis_cs_import_from_fs(self.__cs,
                                                            path.encode('utf-8'), fmt, corpus_name, disk_based, overwrite_existing, err)

        consume_errors(err)
        return ffi.string(imported_corpus_name).decode('utf-8')

    def export_to_fs(self, corpus_name, path, fmt: ExportFormat = ExportFormat.GraphMLZip):
        """ Export a corpus to an external location on the file system using the given format.
            :param corpus_name: The name of the corpus to export. This can be a string or a list of strings.
            :param path: The location on the file system where the corpus data should be written to.
            :param fmt: The format in which this corpus data will be stored stored.

        >>> from graphannis.cs import CorpusStorageManager
        >>> from graphannis.graph import GraphUpdate
        >>> with CorpusStorageManager() as cs:
        ...     # import the same corpus under different names
        ...     c1 = cs.import_from_fs("examples/tutorial.graphml", ImportFormat.GraphML, corpus_name="example1")
        ...     c2 = cs.import_from_fs("examples/tutorial.graphml", ImportFormat.GraphML, corpus_name="example2")
        ...
        ...     # export them to different formats
        ...     cs.export_to_fs(["example1", "example2"], "all.zip", ExportFormat.GraphMLZip)
        ...     cs.export_to_fs("example2", "example2.graphml", ExportFormat.GraphML)
        """
        if self.__cs is None or self.__cs == ffi.NULL:
            return None

        err = ffi.new("AnnisErrorList **")
        c_corpus_list = CAPI.annis_vec_str_new()
        if isinstance(corpus_name, str):
            CAPI.annis_vec_str_push(c_corpus_list, corpus_name.encode('utf-8'))
        else:
            for c in corpus_name:
                CAPI.annis_vec_str_push(c_corpus_list, c.encode('utf-8'))

        CAPI.annis_cs_export_to_fs(self.__cs, c_corpus_list,
                                   path.encode('utf-8'), fmt, err)

        consume_errors(err)
