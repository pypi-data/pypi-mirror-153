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


class IdentitySelector(Selector[ProblemType]):
    """Selection by no selection.

    """
    def select(self, population: SampleSet) -> SampleSet:
        """Passes the input population without any changes.

        """
        return population

class IdentitySelection(Selection[ProblemType]):
    """Configuration of algorithm with no selection.

    Useful for writing test cases that just need some selection.

    """
    def initialise(self, problem: ProblemType) -> Selector[ProblemType]:
        """Creates a problem independent `IdentitySelector[ProblemType]`.

        """
        return IdentitySelector()
