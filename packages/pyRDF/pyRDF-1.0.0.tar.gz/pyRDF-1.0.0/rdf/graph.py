#!/usr/bin/env python


class Statement(tuple):
    """Statement"""

    subject = None
    predicate = None
    object = None

    def __new__(cls, subject, predicate, object):
        return super().__new__(cls, (subject, predicate, object))

    def __init__(self, subject, predicate, object):
        self.subject = subject
        self.predicate = predicate
        self.object = object

    def __getnewargs__(self):
        return (self.subject, self.predicate, self.object)

    def __eq__(self, other):
        for resourceA, resourceB in ((self.subject, other.subject),
                                     (self.predicate, other.predicate),
                                     (self.object, other.object)):
            if resourceA != resourceB:
                return False

        return True

    def __lt__(self, other):
        # ordering following predicate logic: (s, p, o) := p(s, o)
        for resourceA, resourceB in ((self.predicate, other.predicate),
                                     (self.subject, other.subject),
                                     (self.object, other.object)):
            if resourceA < resourceB:
                return True

        return False

    def __str__(self):
        return "(%s, %s, %s)" % (str(self.subject),
                                 str(self.predicate),
                                 str(self.object))

    def __hash__(self):
        return hash(repr(self))
