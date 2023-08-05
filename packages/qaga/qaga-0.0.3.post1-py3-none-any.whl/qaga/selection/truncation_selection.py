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

from .selection import Selector, Selection
from ..problem import ProblemType


class TruncationSelector(Selector[ProblemType]):
    """Selection by preserving only the best individuals.

    Preserves the `num_preserved` best individuals regarding their energies and
    discards the remaining ones.

    Args:
        num_preserved (int): Positive, maximal number of individuals in the next
            population. It can be less if the input population is too small.

    """
    def __init__(self, num_preserved: int):
        assert num_preserved >= 0
        self._num_preserved = num_preserved

    def select(self, population: SampleSet) -> SampleSet:
        """Removes individuals with the worst energies.

        Args:
            population (dimod.SampleSet): Nonempty population to select from.

        Returns:
            A nonempty `dimod.SampleSet` with at most `num_preserved` elements.
            It is an at least as good subset of `population`

        """
        assert len(population) > 0
        return population.truncate(self._num_preserved)


class TruncationSelection(Selection[ProblemType]):
    """Configuration of a simple only-the-best selection.

    If an algorithm is configured with it, after each iteration, energies are
    sorted regarding their energy; the `num_preserved` best individuals are
    selected and the remaining ones are discarded.

    Monotonicity is guaranteed.

    Args:
        num_preserved (int): Positive, maximal number of individuals in the next
            population. It can be less if the input population is too small.

            Small populations decrease time to solution, but large ones might
            have more diversity, i.e. varying individuals, which increases the
            chance of finding an optimal solution.

    """
    def __init__(self, num_preserved: int):
        assert num_preserved >= 1
        self._num_preserved = num_preserved

    def initialise(self, problem: ProblemType) -> Selector[ProblemType]:
        """Configures a `TruncationSelector[ProblemType]` with the respective `num_preserved`.
        """
        return TruncationSelector[ProblemType](self._num_preserved)
