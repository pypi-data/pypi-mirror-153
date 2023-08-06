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
from numpy.random import Generator, default_rng
from dimod import SampleSet
from typing import Callable

from .recombination import Recombinator
from .pair_recombination import PairRecombinator, PairRecombination
from ..problem import ProblemType


class RandomBitsRecombinator(PairRecombinator[ProblemType]):
    """Pairwise recombination by flipping random bits.

    Seeks locations where two, randomly mated individuals differ and randomly
    chooses and flips some of those bits

    Args:
        problem (ProblemType): The problem to perform recombination.

        num_bits (int): Positive, maximal number of bits to flip. The actual
            value is less if two individuals do not differ in that many bits.

        recombination_rate (int): Positive number suggesting the amount of mates
            each individual is assigned to.

            The actual number can be both below or above this value depending on
            the existence of an appropriate apportionment. For instance, in a
            population consisting of two elements one cannot mate with more than
            one individual.

        rng (Generator, optional): A random number generator that can be
            specified if reproducability is needed.

    """
    def __init__(self,
                 problem: ProblemType,
                 num_bits: int,
                 recombination_rate: int,
                 rng: Generator = default_rng()
                 ):

        self._problem = problem
        self._num_bits = num_bits
        super().__init__(recombination_rate, rng)

    def _mate(self, population: SampleSet, pairs: np.ndarray) -> SampleSet:
        strings = population.record.sample
        left = strings[pairs[0]]
        right = strings[pairs[1]]

        result = np.zeros((2 * len(pairs), strings.shape[1]), dtype=strings.dtype)

        for i in range(len(pairs)):
            arg_xor = np.flatnonzero(left[i] != right[i])
            num_bits = min(self._num_bits, len(arg_xor))
            bits = self._rng.choice(arg_xor, size=num_bits)

            result[i] = left[i]
            result[i][bits] = right[i][bits]

            j = 2 * i
            result[j] = right[i]
            result[j][bits] = left[i][bits]

        return SampleSet.from_samples_bqm(
            (result, self._problem.bqm.variables),
            self._problem.bqm,
            aggregate_samples=True
            )


class RandomBitsRecombination(PairRecombination[ProblemType]):
    """Configuration of pairwise recombination by flipping random bits.

    Differing bits are randomly choosen and flipped for random pairs of
    individuals. It is a simple, uninformed recombination procedure.

    Does not guarantee monotonicity.

    Args:
        num_bits (int): Positive, maximal number of bits to flip. The actual
            value is less if two individuals do not differ in that many bits.

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
    def __init__(self, num_bits: int, recombination_rate: int, rng: Callable[[], Generator]):
        self._num_bits = num_bits
        super().__init__(recombination_rate, rng)

    def initialise(self, problem: ProblemType) -> Recombinator[ProblemType]:
        """Configures a `RandomBitsRecombination[ProblemType]` with respective
        `num_bits` and `recombination_rate`.

        """
        return RandomBitsRecombinator[ProblemType](
            problem,
            self._num_bits,
            self._recombination_rate,
            self._rng()
            )
