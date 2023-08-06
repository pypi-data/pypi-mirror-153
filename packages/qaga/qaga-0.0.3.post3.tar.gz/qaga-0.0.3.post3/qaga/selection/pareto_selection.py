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


from abc import abstractmethod
from dimod.sampleset import SampleSet, concatenate

from .selection import Selection, Selector
from ..problem import ProblemType


class ParetoSelector(Selector[ProblemType]):
    """Abstract base class for selection procedures that truncate primarily
    regarding some predicate and then subordinately regarding energy.

    Preserves individuals with best energies satisfying the predicate up
    to a certain population size. If there are not enough individuals, it is
    refilled with the best non-satisfactory ones.

    Args:
        num_preserved (int): Positive, maximal number of individuals to
            preserve.

        problem (ProblemType): Problem to perform the selection for. For this
            class it likely contains domain knowledge.

    """
    def __init__(self, num_preserved: int, problem: ProblemType):
        assert num_preserved > 0
        self._num_preserved = num_preserved
        self._problem = problem

    def select(self, population: SampleSet) -> SampleSet:
        """Preserves `num_preserved` individuals with best energies satisfying
        `_sample_predicate` of the current population.

        Missing solutions are refilled with the best remaining ones. Moreover,
        the actual population size is below its target iff the input population
        is below.

        """
        # Discard individuals not satisfying predicate.
        new_population = population\
            .filter(lambda s: self._sample_predicate(self._problem, s))\
            .truncate(self._num_preserved)

        # If individuals missing, add best non satisfactory individuals
        missing = self._num_preserved - len(population)
        if missing > 0:
            addition = population\
                .filter(lambda s: not self._sample_predicate(self._problem, s))\
                .truncate(missing)
            new_population = concatenate([new_population, addition])

        return new_population


    @staticmethod
    @abstractmethod
    def _sample_predicate(problem: ProblemType, sample) -> bool:
        """Abstract static method that determines, which individuals are
        preserved, even if they do not have a good energy.

        """
        pass


class ParetoSelection(Selection[ProblemType]):
    """Abstract base class for configurating a not purely energy guided,
    truncating selection.

    The simplest selection just discards individuals with bad energies. Hence,
    only constraints that are integrated in the `dimod.BinaryQuadraticModel` are
    considered. However, there are constraints tedious to express in a
    `dimod.BinaryQuadraticModel` but easy to check for a given solution. One can
    use of this by selecting only elements that satisfy this constraint. Of
    course, one must additionally consider the energy of these to respect other
    constraints.

    This idea is implemented in this class with a possibility to filter
    individuals. Note that to enable some diversity, the best, non-satisfactory
    solutions may still appear if there a not enough satisfactory individuals.

    Args:
        num_preserved (int): Positive, maximal number of individuals in the next
            population. It can be less if the input population is too small.

            Small populations decrease time to solution, but large ones might
            have more diversity, i.e. varying individuals, which increases the
            chance of finding an optimal solution.
    """
    def __init__(self, num_preserved: int):
        assert num_preserved > 0
        self._num_preserved = num_preserved
