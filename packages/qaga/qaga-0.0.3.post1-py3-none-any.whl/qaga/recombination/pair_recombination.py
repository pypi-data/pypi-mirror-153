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

import numpy as np
from abc import abstractmethod
from numpy.random import Generator, default_rng
from typing import Callable

from dimod import SampleSet

from .recombination import Recombinator, Recombination
from ..problem import ProblemType


def create_pairs(population_size: int, recombination_rate: int, rng: Generator = default_rng()):
    """Recombination of pairs.

    Tries to choose randomly `recombination_rate` mates for each `population_size` elements.
    An element cannot be mated with itself and there are no dublicate pairs.

    Args:
        population_size: Number of individuals that should be mated. There must be at least two.
        recombination_rate: Amount of mates each individual should be with paired.
        rng: Random number generator.
    """
    assert population_size > 1
    assert recombination_rate >= 1

    # If recombination rate is too large, create all possible pairs
    if population_size <= recombination_rate:
        recombination_rate = population_size - 1


    # Stores pairs
    assignment = np.zeros((2, population_size * recombination_rate), dtype=int)
    # Stores which mates are choosable in the respective iteration
    assignable = np.arange(1, population_size, dtype=int)

    # Sample mates for first individual
    assignment[1, :recombination_rate] = rng.choice(assignable, size=recombination_rate, replace=False)

    chosen = recombination_rate
    for individual in range(1, population_size):
        # Prohibit choosing one self
        assignable[individual-1] -= 1

        # Sample mates for current individual
        new_chosen = chosen + recombination_rate
        assignment[0, chosen:new_chosen] = individual
        assignment[1, chosen:new_chosen] = rng.choice(assignable, size=recombination_rate, replace=False)

        chosen = new_chosen

    # Eliminate duplicates
    assignment = np.unique(np.sort(assignment, axis=0), axis=1)

    return assignment


class PairRecombinator(Recombinator[ProblemType]):
    """Abstract class for combining pairs of individuals.

    It implements random creation of pairs, that subclasses can use to recombine
    new individuals from them.

    Args:
        recombination_rate (int): Positive number suggesting the amount of mates
            each individual is assigned to.

            The actual number can be both below or above this value depending on
            the existence of an appropriate apportionment. For instance, in a
            population consisting of two elements one cannot mate with more than
            one individual.

        rng (Generator, optional): A random number generator that can be
            specified if reproducability is needed.

    """
    def __init__(self, recombination_rate: int, rng: Generator = default_rng()):
        assert recombination_rate > 0
        self._recombination_rate = recombination_rate
        self._rng = rng

    def recombine(self, population: SampleSet) -> SampleSet:
        """Combines individuals pairwise.

        First, pairs of individuals are created randomly and then `self._mate`
        is used to recombine those.

        """
        pairs = create_pairs(len(population), self._recombination_rate)
        return self._mate(population, pairs)

    @abstractmethod
    def _mate(self, population: SampleSet, pairs: np.ndarray) -> SampleSet:
        """Abstract method determining combination of pairs.

        Args:
            pairs (np.ndarray): An array of pairs indices representing the
                respective individuals. Two solutions are at most paired once
                and never with oneself.

        """
        pass


class PairRecombination(Recombination[ProblemType]):
    """Basic, abstract configuration for pairwise recombination.

    Args:
        recombination_rate (int): Positive number suggesting the amount of mates
            each individual is assigned to.

            The actual number can be both below or above this value depending on
            the existence of an appropriate apportionment. For instance, in a
            population consisting of two elements one cannot mate with more than
            one individual.

        rng (Callable[[], Generator]], optional): A function that creates an
            isolated random number generator that can be specified if
            reproducability is needed.
    """
    def __init__(self, recombination_rate: int, rng: Callable[[], np.random.Generator] = default_rng):
        assert recombination_rate > 1
        self._recombination_rate = recombination_rate
        self._rng = rng
