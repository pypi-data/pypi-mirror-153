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

from dimod import Sampler, SampleSet
from typing import Dict, Any

from .mutation import Mutator, Mutation
from ..problem import ProblemType


class SamplerMutator(Mutator[ProblemType]):
    """Individual improvement by means classic local search.

    Args:
        sampler (dimod.Sampler): A classical sampler.

        sampler_config (dict): Possible configuration for the sampler that is
            specifically used to force local instead of global search

    """
    def __init__(self, sampler: Sampler, problem: ProblemType, sampler_config: Dict[str, Any] = {}):
        self._sampler = sampler
        self._sampler_config = sampler_config
        self._problem = problem

    def mutate(self, population: SampleSet) -> SampleSet:
        """Performs one sampler run for each individual.

        """
        return self._sampler.sample(self._problem.bqm, initial_states=population, **self._sampler_config)


class SamplerMutation(Mutation[ProblemType]):
    """Configuration of individual improvement by means of local search
    annealing.

    Classically simulates an actual Quantum-Assisted Genetic Algorithm (QAGA).
    It should be the default class for testing and experimenting, as it does not
    require access to any proprietary quantum hardware.

    Does not guarantee monotonicity.

    Args:
        sampler (dimod.Sampler): A classical sampler.

        sampler_config (dict): Possible configuration for the sampler that is
            specifically used to force local instead of global search

    """
    def __init__(self, sampler: Sampler, sampler_config: Dict[str, Any] = {}):
        self._sampler = sampler
        self._sampler_config = sampler_config

    def initialise(self, problem: ProblemType) -> Mutator[ProblemType]:
        """Configures and creates a new object that performs mutation with an
        injected sampler.

        Args:
            problem (ProblemType): The problem the mutation should be used for.

        Returns:
            A `SamplerMutator[ProblemType]`

        """
        return SamplerMutator[ProblemType](self._sampler, problem, self._sampler_config)
