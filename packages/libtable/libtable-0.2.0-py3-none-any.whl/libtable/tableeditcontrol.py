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

from .tableselectcontrol import TableSelectControl

from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding import merge_key_bindings


class TableEditControl(TableSelectControl):
    def __init__(self,
                 table,
                 show_header=True,
                 show_auto=False,
                 global_key_bindings=True
                 ):
        self.kb = KeyBindings()
        super().__init__(table, show_header=show_header, show_auto=show_auto, global_key_bindings=global_key_bindings)

    def get_key_bindings(self):
        key_bindings = super().get_key_bindings()
        return merge_key_bindings([self.kb, key_bindings])

    def addEvent(self, *name: str, fn):
        @self.kb.add(*name)
        def _(event):
            fn(self.get_current_index(), self.get_current_row())

    def updateValue(self, index, column, value):
        try:
            temp = list(self.table["rows"][index])
            temp[column] = value
            self.table["rows"][index] = tuple(temp)
        except Exception:
            return
