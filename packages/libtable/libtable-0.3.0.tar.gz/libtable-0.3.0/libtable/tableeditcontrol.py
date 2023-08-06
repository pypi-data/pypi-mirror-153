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

from ._baseclass import BaseTableData
from .tableselectcontrol import TableSelectControl

from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding import merge_key_bindings


class TableEditControl(TableSelectControl):
    def __init__(self,
                 table: BaseTableData,
                 show_header: bool = None,
                 show_auto: bool = None,
                 global_key_bindings: bool = True,
                 show_search: bool = True,
                 show_sort: bool = False
                 ) -> None:
        self.kb = KeyBindings()
        super().__init__(table,
                         show_header=show_header,
                         show_auto=show_auto,
                         global_key_bindings=global_key_bindings,
                         show_search=show_search,
                         show_sort=show_sort
                         )

    def get_key_bindings(self) -> KeyBindings:
        key_bindings = super().get_key_bindings()
        return merge_key_bindings([self.kb, key_bindings])

    def addEvent(self, *name: str, fn) -> None:
        @self.kb.add(*name)
        def _(event):
            fn(self.get_current_index(), self.get_current_row()[1])
