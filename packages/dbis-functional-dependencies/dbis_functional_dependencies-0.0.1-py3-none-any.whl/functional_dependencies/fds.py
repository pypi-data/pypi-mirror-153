#!/usr/bin/python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2000-2021 Jens Lechtenbörger

u"""Functional dependencies (FDs) are a major tool for database design.

Introduction
============
The module
[functional_dependencies](https://gitlab.com/oer/cs/functional-dependencies/-/blob/master/functional_dependencies/functional_dependencies.py)
defines the classes `FD`, `FDSet`, and `RelSchema` to represent
a single functional dependency (FD), a set of FDs, and a relation schema,
respectively.  Here, a relation schema
is defined by a set of attributes and a set of FDs.  In particular,
`RelSchema.synthesize()` *synthesizes* a given schema into a set of relation
schemata in 3rd normal form (3NF).  Thus, the given schema does not need to
satisfy any normal form, while the set of output schemata will be in 3NF.
While the synthesis algorithm goes back to Bernstein (1976),
https://doi.org/10.1145/320493.320489,
notation and algorithms in this module follow that book:
Vossen (1999): Datenbankmodelle, Datenbanksprachen und
Datenbankmanagementsysteme, 3. Aufl., Oldenbourg

*Relation schemata* define tabular structures (in a spirit similar to CREATE
TABLE statements of SQL) with attributes (column headers with data types) and
constraints (here, we just consider functional dependencies, which generalize
primary keys).  A *relation* is an *instance* of a schema, i.e., a set of rows
or *tuples* that obeys the rules (data types and constraints) laid out by the
schema.

Functional Dependencies
=======================
An FD is an integrity constraint, restricting the set of permissible
relations/instances of a relation schema.  Intuitively, FDs capture semantic
information which attributes belong together how.
FDs are written in the form X -> Y for sets X and Y of attributes.
(In this module, attributes are just strings.  In general, each attribute has
a *domain* of permissible values, potentially including a NULL value.)
X is called *left-hand side* (lhs), Y *right-hand side* (rhs).
An FD is called *r-minimal* or *simple* if |Y| == 1, i.e., if the rhs consists
of a single element.

Following general practice, in this documentation we may represent sets of
attributes as sequences, omitting braces and commas to simplify notation.

Formally, an FD X -> Y *holds* in a relation r if no two tuples exist in r
that share the same X-value but disagree on their Y-values.
(Intuitively, each X-value functionally determines exactly one Y-value.)
An FD is *trivial* if it is satisfied in every relation.  (E.g., if Y is a
subset of X, then X -> Y is trivial: clearly, if tuples agree on the "larger"
lhs, then they also agree on the rhs.)

Instances of `FD` are constructed from lhs and rhs, each of which is
either a single attribute or set of attributes.  E.g., `fd1` below
represents the FD CustomerID -> DateOfBirth.
>>> fd1 = FD("CustomerID", "DateOfBirth")
>>> fd1.isrminimal()
True
>>> fd1.attributes() == {"CustomerID", "DateOfBirth"}
True
>>> fd2 = FD({"CustomerID", "DateOfBirth"}, {"BirthYear", "Country"})
>>> fd2.isrminimal()
False
>>> fd2.attributes() == {"CustomerID", "DateOfBirth", "BirthYear", "Country"}
True

Keys
----
A *superkey* for a relation schema R with attributes Y is a set K of attributes
such that the FD K -> Y holds.  Intuitively, the values of superkeys are
unique per relation.

The notion of superkey is merely a technical one.  We are really interested in
keys.  ("Super" does not indicate "better" but "superset of"; see next
paragraph.)

A *key* is a superkey that is minimal with respect to set inclusion.  (I.e.,
if we remove any attribute from a key, then the remaining attributes do not
functionally determine all other attributes any more.)  Thus, every superset
of a key is a superkey.  In particular, the set of all attributes is a trivial
superkey (and method `RelSchema.key()`, which determines a key for a relation
schema with its FDs, starts from that superkey to find a key).

In SQL, one of the keys of a relation schema may be declared as *primary key*.
(I do not know what a "candidate" key is.  Let me expand on that.  In his
[seminal paper on the relational
model](https://dl.acm.org/doi/10.1145/362384.362685),
Codd talks about primary keys and nonredundant primary keys, while he defines
candidate keys in his [follow-up paper on
normalization](https://www.bibsonomy.org/bibtex/24b7b528f0502ff638c837f39a3ed3732).
In the decades since then, we have come to *define* keys as nonredundant sets
of attributes.  Thus, redundant keys do not exist any longer, and
"nonredundant" stopped being a meaningful qualifier.  Moreover, I
doubt that a reasonable definition for "noncandidate" key exists, which turns
"candidate" into a meaningless qualifier.  Please do not use it unless you can
say what it means.)

In general, multiple keys may exist; thus, we talk about "a key",
not "the key" (e.g., in a table with data about student assistants, the
matriculation number, the student number, the employee number, and the tax ID
could exist as four different keys).  Note that keys are *sets* of attributes
(e.g., the  primary key of a fact table in a data warehouse contains
attributes for each of the dimensions).

An attribute that occurs in *some* key is called *key attribute* or *prime
attribute*; otherwise it is a non-key attribute (non-prime).

*Warning!*  Please be careful if you read texts on normalization or FDs that
talk about "the key".  Quite likely, they are incorrect.


Sets of FDs
===========
The class `FDSet` represents a set of FDs.
A non-simple FD X -> A1, ..., An with n>1 is equivalent to a set of n simple
FDs X -> A1, ..., X -> An (this claim requires a proof).
Such a set can be computed with `FD.rminimize()` (which also removes
trivial FDs).  As fd1 is simple and non-trivial, `rminimize()` does not have
an effect:
>>> fdset1 = fd1.rminimize()
>>> logging.debug("fdset1: %s", fdset1)
>>> len(fdset1) == 1
True
>>> fd1b = next(iter(fdset1))
>>> fd1.lhs == fd1b.lhs and fd1.rhs == fd1b.rhs
True

Non-simple FD fd2 is split into two simple FDs:
>>> fdset2 = fd2.rminimize()
>>> len(fdset2) == 2
True
>>> len([nfd for nfd in fdset2 if not nfd.isrminimal()]) == 0
True
>>> print(fdset2)
{{CustomerID, DateOfBirth} -> {BirthYear}, {CustomerID, DateOfBirth} -> {Country}}

In the following FD, DateOfBirth occurs in lhs and rhs.  Thus, `rminimize()`
removes the trivial FD {CustomerID, DateOfBirth} -> DateOfBirth.
>>> fd3 = FD({"CustomerID", "DateOfBirth"}, {"DateOfBirth", "BirthYear"})
>>> fd3mset = fd3.rminimize()
>>> len(fd3mset) == 1
True
>>> fd3 == fd3mset
False
>>> fd3b = next(iter(fd3mset))
>>> fd3 == fd3b
False
>>> fd3 != fd3b
True
>>> print(fd3b)
{CustomerID, DateOfBirth} -> {BirthYear}

Implication of FDs
------------------
Given some FDs, other (non-trivial) FDs may be *implied*, e.g., if A -> B and
B -> C hold in some relation, then also A -> C holds (this claim requires
a proof).  In this case, the FD A -> C is called *transitive*, while A -> B
and B -> C are *direct*.
>>> fds = FDSet()
>>> fds.add(FD({"CustomerID"}, {"DateOfBirth"}))
>>> fds.add(FD({"DateOfBirth"}, {"BirthYear"}))
>>> fds.isimplied({"CustomerID"}, "BirthYear")
True

Given a set F of FDs, the *closure* of F, denoted F⁺, is the set of FDs
that are implied by F.

Implication of FDs is related to the *closure* of attributes.  Given sets F of
FDs and X of attributes, the closure of X with respect to F, denoted X⁺, is
the largest set of attributes Y such that X -> Y is implied by F.
>>> fds.closure({"CustomerID"}) == {"CustomerID", "DateOfBirth", "BirthYear"}
True

FD Basis
--------
Given a set F of FDs, we may wonder what its "core" looks like, i.e., a
"small" set G of FDs such that the FDs implied by F and G are the same (i.e.,
F⁺ = G⁺).
Formally, a *basis* is such a set (note "a" basis, not "the" basis):
>>> fds2 = FDSet(fds.copy())
>>> fds2.add(FD({"CustomerID"}, {"BirthYear"}))
>>> fds2.add(FD({"CustomerID", "DateOfBirth"}, {"BirthYear"}))
>>> fds2.add(FD({"Country"}, {"Country"}))
>>> basis = fds2.basis()
>>> fds == basis and basis.basis() == basis
True

What is computed as basis here, is called "minmal cover" elsewhere (e.g.,
[Abiteboul, Hull, Vianu (1995): Foundations of Databases](https://wiki.epfl.ch/provenance2011/documents/foundations%20of%20databases-abiteboul-1995.pdf)):
Such a set G

- contains only simple FDs (guaranteed by `FD.rminimize()`),
- contains only l-minimal FDs (guaranteed by `FDSet.lminimize()`),
- is minimal or nonredundant, i.e., no subset of G has the same closure
  (tested by iterative removal attempts of individual FDs in `FDSet.basis()`).

>>> {"CustomerID"} == fds2.lminimize({"CustomerID", "DateOfBirth"}, {"BirthYear"})
True

Normal Forms
============
*Normal forms* are quality criteria for "good" schemata.  Normal forms for
relational schemata start from the first normal form (1NF), for which
different interpretations exist.  Codd initially ruled out sets as attribute
values with 1NF, while other sources rule out non-atomic values.  We don't
bother with the subtleties here but note that a person's name consisting of
components, such first and last name, is not atomic, which precludes queries
by last name and hints therefore at disadvantages of non-atomic values.
However, the boundaries are fuzzy.  Are dates including year, month, and day
atomic or not?  Are strings consisting of characters atomic?

Higher normal forms (2NF, 3NF, ...) suppose that 1NF is satisfied.  Then they
aim to avoid *redundancy* and so-called *update anomalies*, see
[Wikipedia](https://en.wikipedia.org/wiki/Database_normalization)
for examples.

3NF
---
The present Python module focuses on 3NF normalization.  Intuitively, 3NF
makes sure that each relation schema only contains attributes that belong to a
"reasonable" semantic unit.  A relation schema in 1NF is in *3NF* iff (if and
only if) for every non-key attribute A and every key K the FD K -> A is
direct.  Equivalently, it is in 3NF iff for every non-trivial FD Y -> A either
Y is a superkey or A is a key attribute.  (Note that you do not need to know
2NF to understand 3NF.  Also, we can normalize to 3NF directly, without an
intermediate step via 2NF.)

*Warning!*  Again, if some text introduces normal forms with reference to "the
key", please stay away.  (Under such approaches, it might be sufficient to add
a new attribute, say with increasing integer numbers, as primary key to
"normalize" the schema.  Clearly, adding a new attribute does not remove
redundancy and does not avoid update anomalies.  Thus, such approaches are
flawed.)

Synthesis
---------
The class of *synthesis* algorithms transforms or *normalizes* an input schema
with a given set F of FDs into a set of relation schemata in third normal form
(3NF).  The essential structure of synthesis algorithms is as follows:

1. "Minimize" F to obtain an equivalent set F’
   (remove redundancies, group common left hand sides together)
2. For each FD X → Y in F' create a relation schema over attributes X∪Y
   with *key X*
3. If no created schema contains a key for the input schema, then add a further
   schema having such a key

To "minimize", the implementation here first computes a basis for F.
Then, it creates a relation schema for each lhs occurring in the
basis.

Supplier example of Vossen (1999).
>>> fds = FDSet()
>>> fds.add(FD({"Lieferant", "Teil"}, {"Anzahl", "Ort", "Entfernung"}))
>>> fds.add(FD({"Lieferant"}, {"Ort"}))
>>> fds.add(FD({"Ort"}, {"Entfernung"}))
>>> fds.key() == {"Lieferant", "Teil"}
True
>>> lieferant = RelSchema(fds.attributes(), fds)
>>> lieferant.key() == {"Lieferant", "Teil"}
True
>>> normalisiert = lieferant.synthesize()
>>> logging.debug(_rels2string(normalisiert))
>>> len(normalisiert) == 3
True

Synthesize the account example of Vossen (1999),
which adds a global key:
>>> fds = FDSet()
>>> fds.add(FD({"Kunde"}, {"Saldo"}))
>>> fds.add(FD({"Nummer"}, {"Zweigstelle", "Saldo"}))
>>> fds.key() == {"Kunde", "Nummer"}
True
>>> kunde = RelSchema(fds.attributes(), fds)
>>> normalisiert = kunde.synthesize()
>>> logging.debug(_rels2string(normalisiert))
>>> len(normalisiert) == 3
True

Synthesize 3NF schemata for exercise 7.8 (10) of Vossen (1999).
Note that we start from 6 FDs, where one is redundant.  Which one is it why?
>>> ex10 = FDSet()
>>> ex10.add(FD({"Course"}, {"Teacher"}))
>>> ex10.add(FD({"Hour", "Room"}, {"Course"}))
>>> ex10.add(FD({"Hour", "Teacher"}, {"Room"}))
>>> ex10.add(FD({"Course", "Student"}, {"Grade"}))
>>> ex10.add(FD({"Hour", "Student"}, {"Room"}))
>>> ex10.add(FD({"Hour", "Room"}, {"Teacher"}))
>>> relschema = RelSchema(ex10.attributes(), ex10)
>>> normalized = relschema.synthesize()
>>> logging.debug(_rels2string(normalized))
>>> len(normalized) == 5
True

A schema for class usage.
>>> misdwh = FDSet()
>>> misdwh.add(FD({"AccID"}, {"AccID", "Type", "CustID"}))
>>> misdwh.add(FD({"AccID", "Date"},
... {"AccID", "Date", "Type", "CustID", "Balance", "CustAge"}))
>>> misdwh.add(FD({"AccID", "Date"}, {"Balance", "CustAge"}))
>>> misdwh.add(FD({"CustID", "Date"}, {"CustAge", "CustValue"}))
>>> misdwh.add(FD({"CustID"}, {"CustName", "DateOfBirth", "Address"}))
>>> banking = RelSchema(misdwh.attributes(), misdwh)
>>> starschema = banking.synthesize()
>>> logging.debug(_rels2string(starschema))
>>> len(starschema) == 4
True

`RelSchema.synthesize()` may output redundant schemata as an address example
of Vossen (1999) shows (a classical example of a schema in 3NF but not in
Boyce-Codd Normal Form, BCNF).
>>> fdaddr = FDSet()
>>> fdaddr.add(FD({"City", "Address"}, "ZipCode"))
>>> fdaddr.add(FD("ZipCode", "City"))
>>> addrschema = RelSchema(fdaddr.attributes(), fdaddr)
>>> addr3nf = addrschema.synthesize()
>>> logging.debug(_rels2string(addr3nf))
>>> len(addr3nf) == 2
True

Use parameter `minimize=True` to remove redundant schemata.
>>> addr3nf = addrschema.synthesize(minimize=True)
>>> logging.debug(_rels2string(addr3nf))
>>> len(addr3nf) == 1
True

"""

import logging


def _set2string(elems):
    """Return string representing the set elems.

    Produce braces and commas, sort elements.
    """
    return "{{{}}}".format(", ".join(sorted([str(elem) for elem in elems])))


def _maybe2set(thing):
    """Return thing in or as set.

    If thing is a set, return unchanged.
    Otherwise, return set containing just thing.
    """
    result = thing
    if not isinstance(thing, set):
        result = set()
        result.add(thing)
    return result


def _rels2string(relations):
    """Return relations as string, one per line in random order."""
    return "\n".join([str(relation) for relation in relations])


class FD(object):
    """A functional dependency with left- and right-hand side."""

    def __init__(self, lhs, rhs):
        """Create FD with lhs and rhs.

        Each argument can be a single attribute or a set of attributes.
        """
        self.lhs = _maybe2set(lhs)
        self.rhs = _maybe2set(rhs)

    def __str__(self):
        """Return string for self.  Use sorting for unique string."""
        return "{} -> {}".format(_set2string(self.lhs), _set2string(self.rhs))

    def __eq__(self, other):
        """Return True iff lhs and rhs of self and other are equal."""
        if isinstance(other, FD):
            return self.lhs == other.lhs and self.rhs == other.rhs
        return False

    def __ne__(self, other):
        """Return not `__eq__()`."""
        return not self.__eq__(other)

    def __hash__(self):
        """Return `hash()` of string."""
        return hash(str(self))

    def isrminimal(self):
        """Return true iff self is r-minimal.

        An FD is r-minimal if the right-hand side is a singleton.
        """
        return len(self.rhs) == 1

    def attributes(self):
        """Return attributes of self (union of left- and right-hand side)."""
        return self.lhs.union(self.rhs)

    def rminimize(self):
        """Return a minimal cover of r-minimal FDs for self.

        Achieve minimality by removal of trivial FDs.
        """
        result = FDSet()
        for attr in self.rhs:
            singleton = set()
            singleton.add(attr)
            if attr in self.lhs:
                # FDs of the form XA->A are trivial.
                logging.debug("rminimize: omitted trivial FD %s",
                              FD(self.lhs, singleton))
                continue
            result.add(FD(self.lhs.copy(), singleton))
        return result


class FDSet(set):
    """A set of functional dependencies."""

    def __init__(self, fdset=None):
        """Construct FDSet, either as empty set of from given set."""
        set.__init__(self)
        if fdset:
            self.update(fdset)

    def __str__(self):
        """Return set with braces, commas, and sorted elements."""
        return _set2string(self)

    def __eq__(self, other):
        """Test for set equality of self and other."""
        return self.issubset(other) and other.issubset(self)

    def attributes(self):
        """Return set with all attributes in FDs in self."""
        result = set()
        for fdep in self:
            result.update(fdep.attributes())
        return result

    def project(self, attributes):
        """Project self to FDs that contain given attributes."""
        result = set()
        for fdep in self:
            if fdep.lhs.issubset(attributes) and fdep.rhs.issubset(attributes):
                result.add(fdep)
        return result

    def closure(self, attributes):
        """Compute closure of attributes under self."""
        result = set(attributes)
        more = True
        while more:
            more = False
            for fdep in self:
                if fdep.lhs.issubset(result) and not fdep.rhs.issubset(result):
                    more = True
                    result.update(fdep.rhs)
        return result

    def isimplied(self, lhs, rhs):
        """Return true iff lhs -> rhs is implied in self.

        Test whether the closure of lhs contains rhs, where rhs can be a
        single attribute or a set of attributes.
        """
        return self.closure(lhs).issuperset(_maybe2set(rhs))

    def lminimize(self, lhs, rhs):
        """Compute minimum subset of lhs that determines rhs.

        Repeatedly remove attributes from lhs as long as it still determines
        rhs.  Note that this removal is non-deterministic.
        """
        cand = lhs.copy()
        for attr in lhs:
            cand.remove(attr)
            if not self.isimplied(cand, rhs):
                # attr is necessary to determine rhs.  Do not remove.
                cand.add(attr)
            else:
                logging.debug(
                    "lminimize: removed %s for rhs %s: new lhs: %s",
                    attr, _set2string(rhs), _set2string(cand))
        return cand

    def key(self):
        """Compute (some) key of self.

        Start with entire set of attributes as superkey.  Use lminimize()
        to remove attributes as long as superkey property is satisfied.
        As lminimize() is non-deterministic, this method is non-deterministic
        as well.
        """
        return self.lminimize(self.attributes(), self.attributes())

    def basis(self):
        """Compute non-redundant r- and l-minimal basis.

        The algorithm here is based on pseudo-code on p. 166 in
        Vossen (1999): Datenbankmodelle, Datenbanksprachen und
        Datenbankmanagementsysteme, 3. Aufl., Oldenbourg
        """
        result = FDSet()
        # First, create simple FDs for self.
        for fdep in self:
            result.update(fdep.rminimize())

        # Second, make each FD l-minimal.
        rcopy = result.copy()
        for fdep in rcopy:
            lhs = self.lminimize(fdep.lhs, fdep.rhs)
            if lhs != fdep.lhs:
                result.remove(fdep)
                logging.debug(
                    "basis: replaced lhs in %s with %s",
                    fdep, _set2string(lhs))
                result.add(FD(lhs, fdep.rhs))

        # Third, remove redundant FDs.  (An FD is redundant if it is implied
        # by other FDs.)
        rcopy = result.copy()
        for fdep in rcopy:
            result.remove(fdep)
            if not result.isimplied(fdep.lhs, fdep.rhs):
                result.add(fdep)
            else:
                logging.debug("basis: removed implied FD %s", fdep)

        return result


class RelSchema(object):
    """A relation schema consists of a set of attributes and a set of FDs.

    Various normal forms exist to describe "good" schemata.  Normalization
    is the process of creating schemata that satisfy certain normal forms.
    The class of synthesis algorithms targets 3NF.
    """

    def __init__(self, attributes, fds):
        """Construct relation schema with attributes and FDs."""
        self.attributes = attributes
        self.fds = fds

    def __str__(self):
        """Return relation schema in usual pair representation."""
        return "({}, {})".format(_set2string(self.attributes),
                                 _set2string(self.fds))

    def key(self):
        """Return a key."""
        return self.fds.key()

    def synthesize(self, minimize=False):
        """Synthesize set of 3NF schemata for self.

        The essential step is the computation of a basis.  Then, create a
        relation schema for each lhs in the basis.  To ensure losslessness, a
        global key may need to be added.

        If `minimize` is True, remove redundant schemata from output.
        """
        basis = self.fds.basis()
        bcopy = FDSet(basis.copy())
        result = set()

        # Iterate over FDs in basis to create schemata per lhs.
        while len(basis) > 0:
            result.add(extract_by_lhs(basis, next(iter(basis))))

        # Test whether a global key is contained.
        havekey = False
        for schema in result:
            if bcopy.isimplied(schema.attributes, bcopy.attributes()):
                havekey = True
                break
        if not havekey:
            key = bcopy.key()
            result.add(RelSchema(key, FDSet()))
            logging.debug("synthesize: added key %s", _set2string(key))

        if minimize:
            rcopy = result.copy()
            for schema in rcopy:
                for cand in rcopy:
                    if schema.attributes == cand.attributes:
                        continue
                    if schema.attributes.issubset(cand.attributes):
                        result.remove(schema)
                        logging.debug("synthesize: removed %s", schema)

        return result


def extract_by_lhs(basis, fdep):
    """Synthesize an instance of RelSchema for lhs of fdep.

    FD fdep must be an element of basis.
    We collect the lhs of fdep and all attributes that are determined by
    the lhs (of fdep and other FDs in basis that share the same lhs) into the
    result schema.

    Note: FDs with matching lhs are removed from basis.  Thus, we can
    iteratively call this until the basis is empty for a synthesis algorithm.
    """
    assert fdep in basis
    attr = set()
    attr.update(fdep.lhs)
    bcopy = FDSet(basis)
    for fdi in bcopy:
        if fdi.lhs == fdep.lhs:
            attr.update(fdi.rhs)
            basis.remove(fdi)
    result = RelSchema(attr, bcopy.project(attr))
    return result


# Run doctests by default.
if __name__ == '__main__':
    import doctest
    print(doctest.testmod())

