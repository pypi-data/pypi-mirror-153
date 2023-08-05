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

from dimod import SampleSet, Vartype, BinaryQuadraticModel
from dimod.generators import uniform
from numpy.testing import assert_array_equal
from hypothesis.strategies import composite, integers, floats
from hypothesis.extra.numpy import arrays

from ..startup.random_startup import create_random, MAX_ITERATIONS


MAX_NUM_QUBITS = 50
MAX_POPULATION_SIZE = 100


@composite
def uniform_bqm(draw, vartype: Vartype, max_num_qubits: int = MAX_NUM_QUBITS) -> BinaryQuadraticModel:
    graph = draw(integers(0, max_num_qubits))
    return uniform(graph, vartype)


@composite
def population(draw, vartype: Vartype,
               max_population_size: int = MAX_POPULATION_SIZE,
               max_num_qubits: int = MAX_NUM_QUBITS,
               max_tries: int = MAX_ITERATIONS):

    rng = np.random
    num_qubits = draw(integers(min_value=1, max_value=max_num_qubits))
    population_size = draw(integers(min_value=1, max_value=min(max_population_size, 2**num_qubits)))

    samples = create_random(num_qubits, population_size, vartype, max_tries, rng)
    energies = draw(
        arrays(
            dtype=np.float_,
            shape=population_size,
            elements=floats(allow_infinity=False, allow_nan=False)
        ))
    occurrences = draw(
        arrays(
            dtype=np.int_,
            shape=population_size,
        ))

    return SampleSet.from_samples(samples, vartype, energies, num_occurrences=occurrences)


def assert_population_equal(population: SampleSet, expected: SampleSet):
    population_indices = np.argsort(population.record)
    expected_indices = np.argsort(expected.record)

    assert_array_equal(
        population.record.sample[population_indices],
        expected.record.sample[expected_indices]
    )
    assert_array_equal(
        population.record.energy[population_indices],
        expected.record.energy[expected_indices]
    )

def assert_no_duplicates(population: SampleSet):
    """Assert that the given population does not contain any duplicates.

    Args:
        population

    Raises:
        AssertionError: If a
    """
    expected = population.aggregate()
    assert_population_equal(population, expected)


def assert_improvement(input_population: SampleSet, output_population: SampleSet):
    """Assert that the output is at least as good as the input, i.e. there is a
    solution with less equal energy than all individuals of the input population.

    Raises:
        AssertionError:
    """
    input_energy = input_population.lowest().energy
    output_energy = output_population.lowest().energy
    assert output_energy <= input_energy, \
        f"Output energy is worse than input: {output_energy} > {input_energy}."
