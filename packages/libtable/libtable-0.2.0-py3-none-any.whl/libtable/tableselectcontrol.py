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

import os
from prompt_toolkit.key_binding import KeyBindings
from ._basetablecontrol import BaseTableControl
from ._exception import TableError


class TableSelectControl(BaseTableControl):
    def __init__(self,
                 table,
                 show_header=True,
                 show_auto=False,
                 global_key_bindings=True
                 ):
        self.table = table
        self.width = os.get_terminal_size().columns
        self.cancelled = False
        self.global_key_bindings = global_key_bindings
        self.__check(show_header, show_auto)
        super().__init__(self.table, self.width)

    def __check(self, show_header: bool, show_auto: bool):
        if "headers" not in self.table:
            raise TableError("Incorrect table - missing headers")
        if "rows" not in self.table:
            raise TableError("Incorrect table - missing rows")
        if "options" not in self.table:
            self.table["options"] = {}
        if "show_header" not in self.table["options"]:
            self.table["options"]["show_header"] = show_header
        if "show_auto" not in self.table["options"]:
            self.table["options"]["show_auto"] = show_auto

    def get_key_bindings(self):
        self.key_bindings = KeyBindings()

        @self.key_bindings.add('up')
        def _(event):
            self.up()

        @self.key_bindings.add('down')
        def _(event):
            self.down()

        @self.key_bindings.add('enter', filter=self.global_key_bindings)
        def _(event):
            event.app.exit()

        @self.key_bindings.add('c-c', filter=self.global_key_bindings)
        def _(event):
            self.cancelled = True
            event.app.exit()

        return self.key_bindings

    def get_response(self):
        if self.cancelled:
            return (-1, "Operation cancelled")
        else:
            return self.get_current_row()
