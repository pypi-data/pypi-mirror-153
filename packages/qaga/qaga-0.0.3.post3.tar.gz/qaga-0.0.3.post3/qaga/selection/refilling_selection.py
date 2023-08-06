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

from typing import Callable
from dimod.sampleset import SampleSet, concatenate
from numpy.random import Generator, default_rng

from .selection import Selector, Selection
from ..startup.random_startup import create_random
from ..problem import ProblemType


MAX_FILLING_ITERATION = 1_000
""" Maximal number of iterations that are performed to generate enough distinct
individuals.

 """

class RefillingSelector(Selector[ProblemType]):
    """Guarantees a certain population size after a selection.

    An arbitrary `Selector[ProblemType]` is injected, that performs selection.
    If its result population is below a specific value, random individuals are
    added.

    Args:
        num_preserved (int): Positive number of individuals the output
            population should have. It is guaranteed unless the solution space
            size makes this impossible.

        problem (ProblemType): The concrete problem instance this
            selection is performed for.

        internal (Selector[ProblemType]): Determines the selection that is done
            first, before additional individuals are added.

        rng (Generator, optional): A random number generator that can be
            specified if reproducability is needed.

    """
    def __init__(self, num_preserved: int, problem: ProblemType,
                 internal: Selector, rng: Generator = default_rng()):
        assert num_preserved > 0
        self._num_preserved = num_preserved
        self._problem = problem
        self._internal = internal
        self._rng = rng

    def select(self, population: SampleSet) -> SampleSet:
        """Performs internal selection on the current population and refills
        with random individuals.

        If the selection of `population` does not contain at least
        `num_preserved` solutions, random ones are added till the size
        `num_preserved` is established.

        Args:
            population (dimod.SampleSet): The current population that should be
                transformed. Variable type and number of qubits must coincide
                with `problem`.

        Returns:
            A `dimod.SampleSet` that preserves the guarantees of `internal`. In
            addition, it contains `num_preserved` distinct individuals the
            solution space size makes this impossible.

        Raises:
            Exception: Due to randomness there is a chance that always already
                existing solutions are drawn, the population size stays the
                same. To guarantee termination a limited number of rerolls are
                done. If it is exceeded a exception is thrown.

        """
        # Do not try to pick more states that available.
        new_population = self._internal.select(population)

        for _ in range(MAX_FILLING_ITERATION):
            if len(new_population) == self._num_preserved:
                return new_population

            # Compute how many additional elements must be created including the replanishing ones.
            num_missing = self._num_preserved - len(new_population)

            # Create new individuals
            additional_individuals = create_random(len(self._problem.bqm), num_missing,
                                                   self._problem.bqm.vartype, MAX_FILLING_ITERATION, self._rng)
            sampleset = SampleSet.from_samples_bqm((additional_individuals, self._problem.bqm.variables),
                                                   self._problem.bqm)
            # Merge both sets removing duplicates
            new_population = concatenate([new_population, sampleset]).aggregate()

        raise Exception(
            "Tried to create new individuals "
            "but failed {MAX_FILLING_ITERATION}-times!"
        )


class RefillingSelection(Selection[ProblemType]):
    """Configure a selection to guarantee a certain population size.

    An arbitrary `Selection[ProblemType]` is used to perform selection. If its result
    population is below a specific value, random individuals are added.

    This helps to prevent so called elitism, i.e. the degeneration of the
    population of later generations because all individuals have been mutated to
    the same, possibly local, minima. New, unrelated solutions widen the search
    space and increase the chance of finding global minima.

    Monotonicity is only guaranteed if `internal` guarantees it.

    Args:
        num_preserved (int): Positive number of individuals output population
            should have. It is guaranteed unless the solution space size makes
            this impossible.

        internal (Selection[ProblemType]): Configures the selection that is done first,
            before additional individuals are added.

        rng (Callable[[], Generator]], optional): A function that creates an
            isolated random number generator that can be specified if
            reproducability is needed.

    """
    def __init__(self,
                 num_preserved: int,
                 internal: Selection,
                 rng: Callable[[], Generator] = default_rng):
        assert num_preserved > 0
        self._num_preserved = num_preserved
        self._internal = internal
        self._rng = rng

    def initialise(self, problem: ProblemType) -> Selector[ProblemType]:
        """Configures a `RefillingSelector[ProblemType]` with the respective
        `num_preserved` and internal selection.

        Args:
            problem (ProblemType): The concrete problem instance this
                selection is performed for. It determines variable type and number
                for the randomly created individuals.

        """
        return RefillingSelector(
            self._num_preserved,
            problem,
            self._internal.initialise(problem),
            self._rng()
            )
