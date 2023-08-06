#!/usr/bin/env python


class Resource:
    value = None

    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value

    def __hash__(self):
        return hash(repr(self))

class Entity(Resource):
    def __init__(self, value):
        super().__init__(value)

class Literal(Resource):
    datatype = None
    language = None

    def __init__(self, value, datatype=None, language=None):
        super().__init__(value)

        if datatype is not None and language is not None:
            raise Warning("Accepts either datatype or language, not both")

        self.datatype = IRIRef(datatype) if datatype is not None else None
        self.language = language

    def __eq__(self, other):
        return self.value == other.value\
                and self.datatype == other.datatype\
                and self.language == other.language

    def __hash__(self):
        value = str()
        if self.datatype is not None:
            value = self.datatype
        if self.language is not None:
            value = self.language

        return hash(repr(self)+repr(value))

class BNode(Entity):
    def __init__(self, value):
        super().__init__(value)

class IRIRef(Entity):
    def __init__(self, value):
        super().__init__(value)
