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
from dimod import SampleSet, BinaryQuadraticModel
from numpy.random import Generator, default_rng

from .recombination import Recombinator
from .pair_recombination import PairRecombinator, PairRecombination
from ..problem import ProblemType


class RandomClusterRecombinator(PairRecombinator[ProblemType]):
    """Pairwise recombination by flipping random regons bits.

    Seeks coherent regions where two, randomly mated individuals differ,
    randomly chooses such a region and flips all of its bits.

    Args:
        problem (ProblemType): The problem to perform recombination.

        recombination_rate (int): Positive number suggesting the amount of mates
            each individual is assigned to.

            The actual number can be both below or above this value depending on
            the existence of an appropriate apportionment. For instance, in a
            population consisting of two elements one cannot mate with more than
            one individual.

        rng (Generator, optional): A random number generator that can be
            specified if reproducability is needed.

    """
    def __init__(self, problem: ProblemType, recombination_rate: int, rng: Generator = default_rng()):
        self._problem = problem
        super().__init__(recombination_rate, rng)

    def _mate(self, population: SampleSet, pairs: np.ndarray) -> SampleSet:
        strings = population.record.sample
        left = strings[pairs[0]]
        right = strings[pairs[1]]

        result = np.zeros((2 * len(pairs), strings.shape[1]), dtype=strings.dtype)

        for i in range(len(pairs)):
            arg_xor = np.flatnonzero(left[i] != right[i])
            bit = self._rng.choice(arg_xor, size=1)[0]

            j = 2 * i
            result[i] = left[i]
            result[j] = right[i]

            cluster_start = bit
            while cluster_start >= 0 and right[i][cluster_start] != left[i][cluster_start]:
                result[i][cluster_start] = right[i][cluster_start]
                result[j][cluster_start] = left[i][cluster_start]
                cluster_start -= 1

            cluster_end = bit
            while cluster_end < strings.shape[1] and right[i][cluster_end] != left[i][cluster_end]:
                result[i][cluster_end] = right[i][cluster_end]
                result[j][cluster_end] = left[i][cluster_end]
                cluster_end += 1


        return SampleSet.from_samples_bqm(
            (result, self._problem.bqm.variables),
            self._problem.bqm,
            aggregate_samples=True
            )

class RandomClusterRecombination(PairRecombination[ProblemType]):
    """Configuration of pairwise recombination by flipping random regions bits.

    Coherent regions of differing bits are randomly choosen and flipped for
    random pairs of individuals. It is a simple, uninformed recombination
    procedure.

    Does not guarantee monotonicity.

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
    def initialise(self, problem: ProblemType) -> Recombinator[ProblemType]:
        """Configures a `RandomClusterRecombination[ProblemType]` with
        respective recombination_rate`.

        """
        return RandomClusterRecombinator[ProblemType](
            problem,
            self._recombination_rate,
            self._rng()
            )
