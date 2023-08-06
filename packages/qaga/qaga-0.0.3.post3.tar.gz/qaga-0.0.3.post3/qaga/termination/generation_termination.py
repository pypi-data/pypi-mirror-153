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

from dimod import SampleSet

from .termination import Terminator, Termination
from ..problem import ProblemType


class GenerationTerminator(Terminator[ProblemType]):
    """Terminating an algorithm by bounding the number of generations.

    Args:
        num_generations: Positive number of iterations after that an algorithm
            should terminate.

    """
    def __init__(self, num_generations: int):
        assert num_generations > 0
        self._num_generations = num_generations
        self._current_generation = 0

    def should_terminate(self, population: SampleSet) -> bool:
        """Checks if itself was called at least `num_generation` times.

        Returns:
            `True` to terminate if this method was called more than
            `num_generation` times, `False` to proceed if not.

        """
        self._current_generation += 1
        return self._current_generation > self._num_generations


class GenerationTermination(Termination[ProblemType]):
    """Configuration on after how many generations an algorithm terminates.

    This is the preferred way to guarantee termination.

    Args:
        num_generations: Positive number of iterations after that an algorithm
            should terminate. If it is too small, population quality might be
            negatively affected.

    """
    def __init__(self, num_generations: int):
        assert num_generations > 0
        self.num_generations = num_generations

    def initialise(self, problem: ProblemType) -> Terminator[ProblemType]:
        """Configurates a `GenerationTerminator[ProblemType]` with the
        respective number of generations.

        """
        return GenerationTerminator[ProblemType](self.num_generations)
