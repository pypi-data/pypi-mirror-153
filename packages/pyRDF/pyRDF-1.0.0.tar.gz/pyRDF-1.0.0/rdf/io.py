#!/usr/bin/env python

from io import BytesIO, StringIO, TextIOWrapper
import os
from sys import stdout

from rdf.graph import Statement
from rdf.terms import Entity, Literal, BNode, IRIRef

class NTriple:
    """N-triple"""

    mode = None
    path = None
    _file = None

    def __init__(self, path=None, mode='r', data=None, encoding='utf-8'):
        # TODO: move this out of this class
        self.mode = mode
        self.path = path

        if self.path is None:
            if self.mode == 'r':
                if data is not None:
                    if isinstance(data, str):
                        self._file = StringIO(data)
                    else:  # bytes
                        self._file = TextIOWrapper(BytesIO(data), encoding=encoding)
                else:
                    raise Exception("No input source provided")
            elif self.mode == 'w':
                self._file = stdout
            else:
                raise Exception("Unsupported mode: {}".format(self.mode))
        else:
            root, ext = os.path.splitext(self.path)
            if ext != ".nt":
                raise Warning("File doesn't seem to be in N-Triple format")

            self._file = open(self.path, self.mode, encoding=encoding)

    def parse(self):
        for statement in self._file:
            statement = statement.strip()
            if len(statement) <= 0 or statement.startswith('#'):
                continue

            try:
                yield self._parse_statement(statement)
            except:
                raise Exception("Line does not conform to NTriple specifications: "
                                + statement)

        self._file.seek(0)

    def write(self, statement):
        self._file.write(self._serialize_statement(statement) + '\n')

    def close(self):
        self._file.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


    ## Parse functions #####################################

    def _parse_statement(self, statement):
        statement = statement.rstrip(' ')
        if not statement.endswith('.'):
            statement = self._strip_comment(statement)
        statement = statement.rstrip(' .')

        subject, remainder = self._parse_subject(statement)
        predicate, remainder = self._parse_predicate(remainder)
        object = self._parse_object(remainder)

        return Statement(subject, predicate, object)

    def _strip_comment(statement):
        for i in range(1, len(statement)):
            if statement[-i] == '#':
                break

        return statement[:-i]

    def _parse_subject(self, statement):
        if statement.startswith("_:"):
            return self._parse_bnode(statement)
        else:  # iriref
            return self._parse_iriref(statement)

    def _parse_predicate(self, statement):
        return self._parse_iriref(statement)

    def _parse_object(self, statement):
        if statement.startswith('<'):
            object, _ = self._parse_iriref(statement)
            return object
        if statement.startswith("_:"):
            object, _ = self._parse_bnode(statement)
            return object
        if not statement.startswith('\"'):
            raise Exception("Unsuspected format: " + statement)

        language = None
        datatype = None
        if statement.endswith('>'):
            # datatype declaration
            for i in range(len(statement)):
                if statement[-i] == '<':
                    break

            datatype = statement[-i+1:-1]
            statement = statement[:-i-2]  # omit ^^
        elif not statement.endswith('\"'):
            # language tag
            for i in range(len(statement)):
                if statement[-i] == '@':
                    break

            language = statement[-i+1:]  # omit @-part
            statement = statement[:-i]
        elif statement.startswith('\"') and statement.endswith('\"'):
            pass
        else:
            raise Exception("Unsuspected format: " + statement)

        return Literal(statement, language=language, datatype=datatype)

    def _parse_bnode(self, statement):
        entity, remainder = self._parse_entity(statement)
        bnode = entity.value
        if bnode.startswith('_:'):
            bnode = BNode(bnode[2:])
        else:
            raise Exception("Unsuspected format: " + bnode)

        return (bnode, remainder)

    def _parse_iriref(self, statement):
        entity, remainder = self._parse_entity(statement)
        iriref = entity.value
        if iriref.startswith('<'):
            iriref = IRIRef(iriref[1:-1])
        else:
            raise Exception("Unsuspected format: " + iriref)

        return (iriref, remainder)

    def _parse_entity(self, statement):
        i = 0
        while i < len(statement) and statement[i] not in [u'\u0009', u'\u0020']:
            i += 1

        return (Entity(statement[:i]), statement[i+1:].lstrip())

    ## Serialization functions #####################################

    def _serialize_statement(self, statement):
        subject = self._serialize_subject(statement.subject)
        predicate = self._serialize_predicate(statement.predicate)
        object = self._serialize_object(statement.object)

        return subject + u'\u0020' + predicate + u'\u0020' + object + " ."

    def _serialize_subject(self, subject):
        if isinstance(subject, IRIRef):
            return self._serialize_iriref(subject)
        elif isinstance(subject, BNode):
            return self._serialize_bnode(subject)
        else:
            raise Exception("Unrecognised resource: " + subject)

    def _serialize_predicate(self, predicate):
        return self._serialize_iriref(predicate)

    def _serialize_object(self, object):
        if isinstance(object, IRIRef):
            return self._serialize_iriref(object)
        elif isinstance(object, BNode):
            return self._serialize_bnode(object)
        elif isinstance(object, Literal):
            # literal
            literal = object.value
            if object.language is not None:
                literal += '@' + object.language
            elif object.datatype is not None:
                literal += "^^" + self._serialize_iriref(object.datatype)

            return literal
        else:
            raise Exception("Unrecognised resource: " + object)

    def _serialize_iriref(self, iriref):
        return '<' + iriref.value + '>'

    def _serialize_bnode(self, bnode):
        return '_:' + bnode.value
