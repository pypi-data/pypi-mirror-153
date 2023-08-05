# cython: binding=True

# Copyright 2019 Ingmar Dasseville, Pierre Carbonnelle
#
# This file is part of Interactive_Consultant.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

Methods to interpret a theory in a data structure

* substitute a constant by its value in an expression
* replace symbols interpreted in a structure by their interpretation
* expand quantifiers

This module also includes methods to:

* substitute an node by another in an AST tree
* instantiate an expresion, i.e. replace a variable by a value

This module monkey-patches the ASTNode class and sub-classes.

( see docs/zettlr/Substitute.md )

"""

import copy
from itertools import product

from .Assignments import Status as S
from .Parse import (Extern, TypeDeclaration,
                    SymbolDeclaration, Symbol, Rule, SymbolInterpretation,
                    FunctionEnum, Enumeration, Tuple, ConstructedFrom,
                    Definition)
from .Expression import (SymbolExpr, Expression, Constructor, AQuantification,
                    AImplication, AConjunction, ARImplication, AAggregate,
                    AComparison, AUnary, AppliedSymbol, UnappliedSymbol,
                    Variable, TRUE, AEquivalence)
from .utils import BOOL, RESERVED_SYMBOLS, SYMBOL, OrderedSet, DEFAULT


# class Extern  ###########################################################

def interpret(self, problem):
    pass
Extern.interpret = interpret


# class TypeDeclaration  ###########################################################

def interpret(self, problem):
    if self.name in problem.interpretations:
        problem.interpretations[self.name].interpret(problem)
    if self.interpretation:
        self.constructors = self.interpretation.enumeration.constructors
    self.translate(problem)
    if self.constructors:
        self.range = sum([c.interpret(problem).range for c in self.constructors], [])
    elif self.interpretation.enumeration:  # range declaration
        self.range = [t.args[0] for t in self.interpretation.enumeration.tuples]

TypeDeclaration.interpret = interpret


# class SymbolDeclaration  ###########################################################

def interpret(self, problem):
    self.domain = list(product(*[s.decl.range for s in self.sorts]))
    self.range = self.out.decl.range

    # create instances
    if self.name not in RESERVED_SYMBOLS:
        self.instances = {}
        for arg in self.domain:
            expr = AppliedSymbol.make(Symbol(name=self.name), arg)
            expr.annotate(self.voc, {})
            self.instances[expr.code] = expr
            problem.assignments.assert__(expr, None, S.UNKNOWN)

    # add type constraints to problem.constraints
    if self.out.decl.name != BOOL and self.name not in RESERVED_SYMBOLS:
        for inst in self.instances.values():
            domain = self.out.decl.check_bounds(inst.copy())
            if domain is not None:
                domain.block = self.block
                domain.is_type_constraint_for = self.name
                domain.annotations['reading'] = "Possible values for " + str(inst)
                problem.constraints.append(domain)
SymbolDeclaration.interpret = interpret


# class Definition  ###########################################################

def interpret(self, problem):
    """updates problem.def_constraints, by expanding the definitions

    Args:
        problem (Problem):
            containts the enumerations for the expansion; is updated with the expanded definitions
    """
    self.cache = {}  # reset the cache
    self.instantiables = self.get_instantiables()
    self.add_def_constraints(self.instantiables, problem, problem.def_constraints)
Definition.interpret = interpret

def add_def_constraints(self, instantiables, problem, result):
    """result is updated with the constraints for this definition.

    The `instantiables` (of the definition) are expanded in `problem`.

    Args:
        instantiables (dict[SymbolDeclaration, list[Expression]]):
            the constraints without the quantification

        problem (Problem):
            contains the structure for the expansion/interpretation of the constraints

        result (dict[SymbolDeclaration, Definition, list[Expression]]):
            a mapping from (Symbol, Definition) to the list of constraints
    """
    for decl, bodies in instantiables.items():
        quantees = self.canonicals[decl][0].quantees  # take quantee from 1st renamed rule
        expr = [AQuantification.make('∀', quantees, e, e.annotations)
                .interpret(problem)
                for e in bodies]
        result[decl, self] = expr
Definition.add_def_constraints = add_def_constraints


# class SymbolInterpretation  ###########################################################

def interpret(self, problem):
    status = S.STRUCTURE if self.block.name != DEFAULT else S.GIVEN
    if self.is_type_enumeration:
        self.enumeration.interpret(problem)
        self.symbol.decl.interpretation = self
    else: # update problem.assignments with data from enumeration
        for t in self.enumeration.tuples:
            if type(self.enumeration) == FunctionEnum:
                args, value = t.args[:-1], t.args[-1]
            else:
                args, value = t.args, TRUE
            expr = AppliedSymbol.make(self.symbol, args)
            self.check(expr.code not in problem.assignments
                or problem.assignments[expr.code].status == S.UNKNOWN,
                f"Duplicate entry in structure for '{self.name}': {str(expr)}")
            e = problem.assignments.assert__(expr, value, status)
            if (status == S.GIVEN  # for proper display in IC
                and type(self.enumeration) == FunctionEnum):
                problem.assignments.assert__(e.formula(), TRUE, status)
        if self.default is not None:
            for code, expr in self.symbol.decl.instances.items():
                if (code not in problem.assignments
                    or problem.assignments[code].status != status):
                    e = problem.assignments.assert__(expr, self.default, status)
                    if (status == S.GIVEN  # for proper display in IC
                        and self.default.type != BOOL):
                        problem.assignments.assert__(e.formula(), TRUE, status)
SymbolInterpretation.interpret = interpret


# class Enumeration  ###########################################################

def interpret(self, problem):
    pass
Enumeration.interpret = interpret


# class ConstructedFrom  ###########################################################

def interpret(self, problem):
    self.tuples = OrderedSet()
    for c in self.constructors:
        c.interpret(problem)
        self.tuples.extend([Tuple(args=[e]) for e in c.range])
ConstructedFrom.interpret = interpret


# class Constructor  ###########################################################

def interpret(self, problem):
    self.range = []
    if not self.sorts:
        self.range = [UnappliedSymbol.construct(self)]
    else:
        self.range = [AppliedSymbol.construct(self, e)
                      for e in product(*[s.decl.out.decl.range for s in self.sorts])]
    return self
Constructor.interpret = interpret


# class Expression  ###########################################################

def interpret(self, problem) -> Expression:
    """ uses information in the problem and its vocabulary to:
    - expand quantifiers in the expression
    - simplify the expression using known assignments and enumerations
    - instantiate definitions

    Args:
        problem (Problem): the Problem to apply

    Returns:
        Expression: the resulting expression
    """
    if self.is_type_constraint_for:  # do not interpret typeConstraints
        return self
    out = self.update_exprs(e.interpret(problem) for e in self.sub_exprs)
    return out
Expression.interpret = interpret


# @log  # decorator patched in by tests/main.py
def substitute(self, e0, e1, assignments, tag=None):
    """ recursively substitute e0 by e1 in self (e0 is not a Variable)

    if tag is present, updates assignments with symbolic propagation of co-constraints.

    implementation for everything but AppliedSymbol, UnappliedSymbol and
    Fresh_variable
    """
    assert not isinstance(e0, Variable) or isinstance(e1, Variable), \
               f"Internal error in substitute {e0} by {e1}" # should use instantiate instead
    assert self.co_constraint is None,  \
               f"Internal error in substitue: {self.co_constraint}" # see AppliedSymbol instead

    # similar code in AppliedSymbol !
    if self.code == e0.code:
        if self.code == e1.code:
            return self  # to avoid infinite loops
        return self._change(value=e1)  # e1 is UnappliedSymbol or Number
    else:
        # will update self.simpler
        out = self.update_exprs(e.substitute(e0, e1, assignments, tag)
                                for e in self.sub_exprs)
        return out
Expression.substitute = substitute


def instantiate(self, e0, e1, problem=None):
    """Recursively substitute Variable in e0 by e1 in a copy of self.

    Interpret appliedSymbols immediately if grounded (and not occurring in head of definition).
    Update fresh_vars.
    """
    assert all(type(e) == Variable for e in e0), \
           f"Internal error: instantiate {e0}"
    if self.value:
        return self
    if problem and all(e.name not in self.fresh_vars for e in e0):
        return self.interpret(problem)
    out = copy.copy(self)  # shallow copy !
    out.annotations = copy.copy(out.annotations)
    out.fresh_vars = copy.copy(out.fresh_vars)
    return out.instantiate1(e0, e1, problem)
Expression.instantiate = instantiate

def instantiate1(self, e0, e1, problem=None):
    """Recursively substitute Variable in e0 by e1 in self.

    Interpret appliedSymbols immediately if grounded (and not occurring in head of definition).
    Update fresh_vars.
    """
    # instantiate expressions, with simplification
    out = self.update_exprs(e.instantiate(e0, e1, problem)
                            for e in self.sub_exprs)

    if out.value is not None:  # replace by new value
        out = out.value
    else:
        for o, n in zip(e0, e1):
            if o.name in out.fresh_vars:
                out.fresh_vars.discard(o.name)
                if type(n) == Variable:
                    out.fresh_vars.add(n.name)
            out.code = str(out)
    out.annotations['reading'] = out.code
    return out
Expression.instantiate1 = instantiate1


# class Symbol ###########################################################

def instantiate(self, e0, e1, problem=None):
    return self
Symbol.instantiate = instantiate


# Class AQuantification  ######################################################

def interpret(self, problem):
    """apply information in the problem and its vocabulary

    Args:
        problem (Problem): the problem to be applied

    Returns:
        Expression: the expanded quantifier expression
    """
    # This method is called by AAggregate.interpret !
    if not self.quantees:
        return Expression.interpret(self, problem)
    self.check(len(self.sub_exprs) == 1, "Internal error")

    # type inference
    inferred = self.sub_exprs[0].type_inference()
    for q in self.quantees:
        if not q.sub_exprs:
            assert len(q.vars) == 1 and q.arity == 1, \
                   f"Internal error: interpret {q}"
            var = q.vars[0][0]
            self.check(var.name in inferred,
                        f"can't infer type of {var.name}")
            q.sub_exprs = [inferred[var.name]]

    forms = self.sub_exprs
    new_quantees = []
    for q in self.quantees:
        self.check(q.sub_exprs[0].decl.out.type == BOOL,
                    f"{q.sub_exprs[0]} is not a type or predicate")
        if not q.sub_exprs[0].decl.range:
            new_quantees.append(q)
        else:
            if q.sub_exprs[0].code in problem.interpretations:
                enumeration = problem.interpretations[q.sub_exprs[0].code].enumeration
                range = [t.args for t in enumeration.tuples.values()]
                guard = None
            elif type(q.sub_exprs[0].decl) == SymbolDeclaration:
                range = q.sub_exprs[0].decl.domain
                guard = q.sub_exprs[0]
            else:  # type declaration
                range = [[t] for t in q.sub_exprs[0].decl.range] #TODO1 decl.enumeration.tuples
                guard = None

            for vars in q.vars:
                self.check(q.sub_exprs[0].decl.arity == len(vars),
                            f"Incorrect arity of {q.sub_exprs[0]}")
                out = []
                for f in forms:
                    for val in range:
                        new_f = f.instantiate(vars, val, problem)
                        if guard:  # adds `guard(val) =>` in front of expression
                            applied = AppliedSymbol.make(guard, val)
                            if self.q == '∀':
                                new_f = AImplication.make('⇒', [applied, new_f])
                            else:
                                new_f = AConjunction.make('∧', [applied, new_f])
                        out.append(new_f)
                forms = out

    if new_quantees:
        forms = [f.interpret(problem) if problem else f for f in forms]
    self.quantees = new_quantees
    return self.update_exprs(forms)
AQuantification.interpret = interpret


def instantiate1(self, e0, e1, problem=None):
    out = Expression.instantiate1(self, e0, e1, problem)  # updates fresh_vars
    for q in self.quantees: # for !x in $(output_domain(s,1))
        if q.sub_exprs:
            q.sub_exprs[0] = q.sub_exprs[0].instantiate(e0, e1, problem)
    if problem and not self.fresh_vars:  # expand nested quantifier if no variables left
        out = out.interpret(problem)
    return out
AQuantification.instantiate1 = instantiate1


# Class AAggregate  ######################################################

def interpret(self, problem):
    assert self.using_if, f"Internal error in interpret"
    return AQuantification.interpret(self, problem)
AAggregate.interpret = interpret

AAggregate.instantiate1 = instantiate1  # from AQuantification


# Class AppliedSymbol  ##############################################

def interpret(self, problem):
    self.symbol = self.symbol.interpret(problem)
    sub_exprs = [e.interpret(problem) for e in self.sub_exprs]
    simpler, co_constraint = None, None
    if self.decl:
        if self.is_enumerated:
            assert self.decl.type != BOOL, \
                f"Can't use 'is enumerated' with predicate {self.decl.name}."
            if self.decl.name in problem.interpretations:
                interpretation = problem.interpretations[self.decl.name]
                if interpretation.default is not None:
                    simpler = TRUE
                else:
                    simpler = interpretation.enumeration.contains(sub_exprs, True)
                if 'not' in self.is_enumerated:
                    simpler = AUnary.make('¬', simpler)
                simpler.annotations = self.annotations
        elif self.in_enumeration:
            # re-create original Applied Symbol
            core = AppliedSymbol.make(self.symbol, sub_exprs).copy()
            simpler = self.in_enumeration.contains([core], False)
            if 'not' in self.is_enumeration:
                simpler = AUnary.make('¬', simpler)
            simpler.annotations = self.annotations
        elif (self.decl.name in problem.interpretations
            and any(s.decl.name == SYMBOL for s in self.decl.sorts)
            and all(a.value is not None for a in sub_exprs)):
            # apply enumeration of predicate over symbols to allow simplification
            # do not do it otherwise, for performance reasons
            f = problem.interpretations[self.decl.name].interpret_application
            simpler = f(problem, 0, self, sub_exprs)
        if (not self.in_head and not self.fresh_vars):
            inst = [defin.instantiate_definition(self.decl, sub_exprs, problem)
                              for defin in problem.definitions]
            inst = [x for x in inst if x]
            if len(inst) == 1:
                co_constraint = inst[0]
            elif len(inst) > 1:
                co_constraint = AConjunction.make('∧', inst)
    out = self._change(sub_exprs=sub_exprs, simpler=simpler,
                       co_constraint=co_constraint)
    return out
AppliedSymbol.interpret = interpret


# @log_calls  # decorator patched in by tests/main.py
def substitute(self, e0, e1, assignments, tag=None):
    """ recursively substitute e0 by e1 in self """

    assert not isinstance(e0, Variable) or isinstance(e1, Variable), \
        f"should use 'instantiate instead of 'substitute for {e0}->{e1}"

    new_branch = None
    if self.co_constraint is not None:
        new_branch = self.co_constraint.substitute(e0, e1, assignments, tag)
        if tag is not None:
            new_branch.symbolic_propagate(assignments, tag)

    if self.code == e0.code:
        return self._change(value=e1, co_constraint=new_branch)
    elif self.simpler is not None:  # has an interpretation
        assert self.co_constraint is None, \
               f"Internal error in substitute: {self}"
        simpler = self.simpler.substitute(e0, e1, assignments, tag)
        return self._change(simpler=simpler)
    else:
        sub_exprs = [e.substitute(e0, e1, assignments, tag)
                     for e in self.sub_exprs]  # no simplification here
        return self._change(sub_exprs=sub_exprs, co_constraint=new_branch)
AppliedSymbol .substitute = substitute

def instantiate1(self, e0, e1, problem=None):
    out = Expression.instantiate1(self, e0, e1, problem)  # update fresh_vars
    if type(out) == AppliedSymbol:  # might be a number after instantiation
        if type(out.symbol) == SymbolExpr and out.symbol.is_intentional():  # $(x)()
            out.symbol = out.symbol.instantiate(e0, e1, problem)
            if type(out.symbol) == Symbol:  # found $(x)
                self.check(len(out.sub_exprs) == len(out.symbol.decl.sorts),
                            f"Incorrect arity for {out.code}")
                out = AppliedSymbol.make(out.symbol, out.sub_exprs)
        if problem and not self.fresh_vars:
            return out.interpret(problem)
    return out
AppliedSymbol .instantiate1 = instantiate1


# Class Variable  #######################################################

def interpret(self, problem):
    return self
Variable.interpret = interpret

# @log  # decorator patched in by tests/main.py
def substitute(self, e0, e1, assignments, tag=None):
    if self.sort:
        self.sort = self.sort.substitute(e0,e1, assignments, tag)
    return e1 if self.code == e0.code else self
Variable.substitute = substitute

def instantiate1(self, e0, e1, problem=None):
    if self.sort:
        self.sort = self.sort.instantiate(e0, e1, problem)
    for o, n in zip(e0, e1):
        if self.code == o.code:
            return n
    return self
Variable.instantiate1 = instantiate1



Done = True
