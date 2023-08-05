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
from dimod import SampleSet, Vartype
from numpy.random import Generator, default_rng

from .startup import Startup
from ..problem import ProblemType


MAX_ITERATIONS = 100


def create_random(num_qubits: int, size: int, vartype: Vartype, max_tries: int, rng: Generator) -> np.ndarray:
    """Creates an array of spin or bit strings randomly.

    Args:
        num_qubits (int): Positive number of qubits each string should have.

        size (int): Positive number of strings in the collection.

        vartype (dimod.Vartype): Variable type, i.e. 'SPIN' or 'BINARY'.

        max_tries (int): Number of tries the procedure performs to avoid
            duplicates until it gives up.

        rng (Generator): A random number generator.

    Returns:
        A 2D numpy array with `num_qubits` columns and at most `size` rows.
    """
    assert num_qubits > 0
    assert size > 0

    # Set of values a bit/spin can have.
    choosable = np.array(list(vartype.value), dtype='i1')

    # Create bit/strings strings randomly
    # and remove duplicates
    sample = np.unique(rng.choice(choosable, size=(size, num_qubits)), axis=0)
    tries = 1

    # If we have enough individuals return population.
    # Else generate new solutions and discard duplicates
    # After some tries give up and return incomplete population
    while len(sample) != size and tries <= max_tries:
        additional = rng.choice(choosable, size=(size-len(sample), num_qubits))
        sample = np.unique(np.concatenate([sample, additional]), axis=0)
        tries += 1

    return sample


class RandomStartup(Startup[ProblemType]):
    """Random population creation.

    A lightweight start for a genetic algorithm with a diverse population.

    Args:
        population_size (int): Positive, maximal number of individuals to create.

        rng (Generator, optional): A random number generator that can be
            specified if reproducability is needed.

    """
    def __init__(self, population_size: int, rng: Generator=default_rng()):
        assert population_size > 0
        self._population_size = population_size
        self._rng = rng

    def startup(self, problem: ProblemType) -> SampleSet:
        """Creates a random population.

        Args:
            problem (ProblemType): The problem for which a population is
                created. Only variable type and amount of qubits of its
                `BinaryQuadraticModel` matter, any additional information is
                ignored.

        Returns:
            A `dimod.SampleSet` that contains at most `population_size`,
            distinct individuals. Due to randomness the actual population
            might be smaller.

        """
        sample = create_random(
            len(problem.bqm),
            self._population_size,
            problem.bqm.vartype,
            MAX_ITERATIONS,
            self._rng
            )

        return SampleSet.from_samples_bqm(
            (sample, problem.bqm.variables),
            problem.bqm,
            aggregate_samples=True
            )
