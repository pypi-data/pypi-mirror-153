# Copyright (C) 2022 Sebastien Guerri
#
# This file is part of libtable.
#
# libtable is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# libtable is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from .tablecontrol import TableControl
from .tableselectcontrol import TableSelectControl
from .tableeditcontrol import TableEditControl
from .table import Table
from .tableprompt import TablePrompt
from .tableselect import TableSelect
from .tabledit import TableEdit
from ._exception import TableError

__doc__ = """
libtable - A library for cli tables
===================================
"""

__all__ = [
    "TableControl",
    "TableSelectControl",
    "TableEditControl",
    "Table",
    "TablePrompt",
    "TableSelect",
    "TableEdit",
    "TableError"
]
