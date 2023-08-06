# copyright 2003-2010 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact https://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of CubicWeb.
#
# CubicWeb is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# CubicWeb is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with CubicWeb.  If not, see <https://www.gnu.org/licenses/>.
"""cubicweb post creation script, set note's workflow

"""

wf = add_workflow("note workflow", "Note")
todo = wf.add_state("todo", initial=True)
done = wf.add_state("done")
wf.add_transition("redoit", done, todo)
wf.add_transition("markasdone", todo, done)
commit()

wf = add_workflow("affaire workflow", "Affaire")
pitetre = wf.add_state("pitetre", initial=True)
encours = wf.add_state("en cours")
finie = wf.add_state("finie")
bennon = wf.add_state("ben non")
wf.add_transition("abort", pitetre, bennon)
wf.add_transition("start", pitetre, encours)
wf.add_transition("end", encours, finie)
commit()
