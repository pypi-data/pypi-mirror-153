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
"""This module contains all important classes and implementations of the
components that are necessary to have a quick start on how to use this library.

Note that classes in this module may differ in implementation from those in the
respective submodules with same name. This enables for the latter a more general
area of applications.

"""

from dimod import Sampler, BinaryQuadraticModel
from typing import Callable, Dict, Any
from numpy.random import Generator

from qaga import mutation as _mutation
from qaga import recombination as _recombination
from qaga import selection as _selection

from .genetic_algorithm import GeneticAlgorithm
from .startup import RandomStartup, WarmStartup, SamplingStartup
from .problem import Problem, ProblemType
from .termination import *


class SamplerMutation(_mutation.SamplerMutation[ProblemType]):
    """Configuration of individual improvement by means of local search
    annealing.

    Classically simulates an actual Quantum-Assisted Genetic Algorithm (QAGA).
    It should be the default class for testing and experimenting, as it does not
    require access to any proprietary quantum hardware.

    The results of the sampler runs are merge with the input population, thus,
    monotonicity is guaranteed.

    Args:
        sampler (dimod.Sampler): A classical sampler.

        sampler_config (dict): Possible configuration for the sampler that is
            specifically used to force local instead of global search

    """
    def __init__(self, sampler: Sampler, sampler_config: Dict[str, Any] = {}):
        mutation = _mutation.SamplerMutation(sampler, sampler_config)
        self._internal = _mutation.AdditionMutation(mutation)

    def initialise(self, problem: BinaryQuadraticModel) -> _mutation.Mutator:
        return self._internal.initialise(problem)


class ReverseAnnealingMutation(_mutation.ReverseAnnealingMutation[ProblemType]):
    """Individual improvement by means of reverse annealing.

    Lifts an ordinary genetic algorithm to a Quantum-Assisted Genetic
    Algorithm (QAGA). Reverse Annealing facilitates DWave's quantum annealer
    hardware to start a given state and perform local search. Thus it is
    predestined as a mutation procedure.

    The results of the sampler runs are merge with the input population, thus,
    monotonicity is guaranteed.

    Note:
        Usage of this class requires access to DWave's commercial samplers.
        For an alternative have a look at `qaga.mutation.SamplerMutation`,
        that offers support for free, classical samplers.

    Args:
        sampler (dimod.Sampler): One of DWave's proprietary samplers. If
            embeddings are needed, using `FixedEmbeddingComposite` or
            `LazyFixedEmbeddingComposite` is strongly encouraged to avoid
            recalculation in each generation.

        sampler_config (dict): Possible configuration for the sampler. For
            instance, to do reverse annealing an 'annealing_path' must
            be given.

    """
    def __init__(self, sampler: Sampler, sampler_config: Dict[str, Any] = {}):
        mutation = _mutation.ReverseAnnealingMutation(sampler, sampler_config)
        self._internal = _mutation.AdditionMutation(mutation)

    def initialise(self, problem: BinaryQuadraticModel) -> _mutation.Mutator[ProblemType]:
        return self._internal.initialise(problem)


class RandomBitsRecombination(_recombination.RandomBitsRecombination[ProblemType]):
    """Configuration of pairwise recombination by flipping random bits.

    Differing bits are randomly choosen and flipped for random pairs of
    individuals. It is a simple, uninformed recombination procedure.

    The results of the bit flips are merge with the input population, thus,
    monotonicity is guaranteed.

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
        recombination = _recombination.RandomBitsRecombination(num_bits, recombination_rate, rng)
        self._internal = _recombination.AdditionRecombination(recombination)

    def initialise(self, problem: BinaryQuadraticModel) -> _recombination.Recombinator:
        return self._internal.initialise(problem)


class RandomClusterRecombination(_recombination.RandomClusterRecombination[ProblemType]):
    """Configuration of pairwise recombination by flipping random regions bits.

    Coherent regions of differing bits are randomly choosen and flipped for
    random pairs of individuals. It is a simple, uninformed recombination
    procedure.

    The results of the bit flips are merge with the input population, thus,
    monotonicity is guaranteed.

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
    def __init__(self, recombination_rate: int, rng: Callable[[], Generator]):
        recombination = _recombination.RandomClusterRecombination(recombination_rate, rng)
        self._internal = _recombination.AdditionRecombination(recombination)

    def initialise(self, problem: BinaryQuadraticModel) -> _recombination.Recombinator:
        return self._internal.initialise(problem)


class TruncationSelection(_selection.TruncationSelection[ProblemType]):
    """Configuration of a simple only-the-best selection.

    If an algorithm is configured with it, after each iteration, energies are
    sorted regarding their energy; the `num_preserved` best individuals are
    selected and the remaining ones are discarded. However, if the population
    size is below a specific value, random individuals are added.

    This helps to prevent so called elitism, i.e. the degeneration of the
    population of later generations because all individuals have been mutated to
    the same, possibly local, minima. New, unrelated solutions widen the search
    space and increase the chance of finding global minima.

    Monotonicity is guaranteed.

    Args:

        num_preserved (int): Positive number of individuals that are preserved
            from the input population. It is guaranteed unless the solution space
            size makes this impossible. If the population size is less then
            random individuals are created.

        num_new_solutions(int): Positive number of additional, randomly created
            individuals regardless of input population size.

        rng (Callable[[], Generator]], optional): A function that creates an
            isolated random number generator that can be specified if
            reproducability is needed.

    """
    def __init__(self, num_preserved: int, num_new_solutions: int, rng: Callable[[], Generator]):
        assert num_preserved > 0
        assert num_new_solutions > 0
        recombination = _selection.TruncationSelection(num_preserved)
        self._internal = _selection.RefillingSelection(num_preserved + num_new_solutions, recombination, rng)

    def initialise(self, problem: BinaryQuadraticModel) -> _selection.Selector:
        return self._internal.initialise(problem)

