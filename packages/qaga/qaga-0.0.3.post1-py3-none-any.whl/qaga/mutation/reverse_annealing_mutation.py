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

from dimod import Sampler
from dwave.system import ReverseBatchStatesComposite
from typing import Dict, Any

from .mutation import Mutator
from .sampler_mutation import SamplerMutator, SamplerMutation
from ..problem import ProblemType


class ReverseAnnealingMutation(SamplerMutation[ProblemType]):
    """Individual improvement by means of reverse annealing.

    Lifts an ordinary genetic algorithm to a Quantum-Assisted Genetic
    Algorithm (QAGA). Reverse Annealing facilitates DWave's quantum annealer
    hardware to start a given state and perform local search. Thus it is
    predestined as a mutation procedure.

    Does not guarantee monotonicity.

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
        # Avoid a current bug in DWave-API
        sampler.parameters.pop("num_reads")
        super().__init__(ReverseBatchStatesComposite(sampler), sampler_config)

    def initialise(self, problem: ProblemType) -> Mutator[ProblemType]:
        """Configures and creates a new object that performs mutation
        with reverse annealing.

        Args:
            problem (ProblemType): The problem the mutation should be used for.

        Returns:
            A `SamplerMutator[ProblemType]`

        """
        return SamplerMutator[ProblemType](self._sampler, problem, self._sampler_config)
