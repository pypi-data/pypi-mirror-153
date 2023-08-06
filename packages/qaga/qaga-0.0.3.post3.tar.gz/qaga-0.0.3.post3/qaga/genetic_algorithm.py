# Copyright (C) 2022 PlanQK
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

from dataclasses import dataclass
from typing import Generic

from dimod import SampleSet
from toolz.curried import pipe

from .mutation import Mutation
from .recombination import Recombination
from .selection import Selection
from .startup import Startup
from .termination import Termination
from .problem import ProblemType


@dataclass
class GeneticAlgorithm(Generic[ProblemType]):
    """Configurable implementation of a genetic algorithm.

    Solves minimisation problems of one specific subtype of `Problem`, i.e.
    problems that can be encoded as `dimod.BinaryQuadraticModel` potentially
    with additional domain knowledge.

    Returns a set of solutions as `dimod.SampleSet`. It is thus fully compatible
    with the `dimod`-API.

    This class itself is just a template that must be filled with respective
    components to work. `mutation`, `recombination`, and `selection` must
    thereby guarantee monotonicity, i.e. after their execution their best
    individual is not worse than the one of previous population.

    Args:
        startup (Startup[problemtype])): Determines the initial population. For
            instance, it can be random or used as a warm start.

        mutation (Mutation[ProblemType]): Improves quality of the current
            population by starting a local search from its individuals.

        recombination (Recombination[ProblemType]): Procreates new individuals
            by combining existing ones.

        selection (Selection[ProblemType]): Truncates low quality solutions to
            keep the population small.

        termination (Termination[ProblemType]): Allows to stop the algorithm if
            the population has achieved a certain quality level or takes too
            long.

    Note that this class is stateless, i.e. calling `optimise` multiple times
    parallelly works without any problems, as long as its components do not
    share a common object, for instance a file.

    """
    startup: Startup[ProblemType]
    mutation: Mutation[ProblemType]
    recombination: Recombination[ProblemType]
    selection: Selection[ProblemType]
    termination: Termination[ProblemType]

    def optimise(self, problem: ProblemType) -> SampleSet:
        # Instantiate each component for a each optimisation run. Therefore, they have their own internal state that
        # should not interfere with the outside environment.
        mutator = self.mutation.initialise(problem)
        recombinator = self.recombination.initialise(problem)
        selector = self.selection.initialise(problem)
        terminator = self.termination.initialise(problem)

        # Produce a first population
        population = self.startup.startup(problem)

        while True:
            # Add new individuals by mutation and recombination.
            population = pipe(population,
                              mutator.mutate,
                              recombinator.recombine)

            # Check termination condition, e.g. existence of a good solution.
            if terminator.should_terminate(population):
                break

            # Truncate low quality individuals.
            population = selector.select(population)
        return population


