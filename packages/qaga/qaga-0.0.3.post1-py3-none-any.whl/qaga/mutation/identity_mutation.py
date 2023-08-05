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

from .mutation import Mutator, Mutation
from ..problem import ProblemType


class IdentityMutator(Mutator[ProblemType]):
    """Mutation by no mutation.

    """
    def mutate(self, population: SampleSet) -> SampleSet:
        """Passes the input population without any changes.

        """
        return population


class IdentityMutation(Mutation[ProblemType]):
    """Configuration of algorithm with no mutation.

    Useful for writing test cases that just need some mutation.

    """
    def initialise(self, problem: ProblemType) -> Mutator[ProblemType]:
        """Creates a problem independent `IdentityMutator[ProblemType]`.

        """
        return IdentityMutator[ProblemType]()
