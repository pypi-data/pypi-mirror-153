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

from .tableeditcontrol import TableEditControl
from prompt_toolkit import Application
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.containers import HSplit
from prompt_toolkit.layout.containers import Window


class TableEdit:
    def __init__(self,
                 table,
                 full_screen,
                 erase_when_done=False,
                 show_header=True,
                 show_auto=False
                 ):
        self.table = table
        self.full_screen = full_screen
        self.erase_when_done = erase_when_done
        self.table_control = TableEditControl(self.table, show_header=show_header, show_auto=show_auto)

    def addEvent(self, *name: str, fn):
        self.table_control.addEvent(*name, fn=fn)

    def updateValue(self, index, column, value):
        self.table_control.updateValue(index, column, value)

    def show(self):
        body = HSplit([Window(content=self.table_control)])
        self.app = Application(layout=Layout(body), full_screen=self.full_screen, key_bindings=self.table_control.get_key_bindings(), erase_when_done=self.erase_when_done)
        self.app.run()
        return self.table_control.get_response()


"""
import os
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.containers import HSplit
from prompt_toolkit.layout.containers import Window
from ._tablecontrol import TableControl
from ._exception import TableError


class TableEdit:
    def __init__(self,
                 table,
                 full_screen,
                 erase_when_done=False,
                 show_header=True,
                 show_auto=False
                 ):
        self.table = table
        self.__check(show_header, show_auto)
        self.width = os.get_terminal_size().columns
        self.table_control = TableControl(self.table, self.width)
        self.__init_kb()
        body = HSplit([Window(content=self.table_control)])
        self.app = Application(layout=Layout(body), full_screen=full_screen, key_bindings=self.kb, erase_when_done=erase_when_done)
        self.cancelled = False

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

    def __init_kb(self):
        self.kb = KeyBindings()

        @self.kb.add('up')
        def _(event):
            self.table_control.up()

        @self.kb.add('down')
        def _(event):
            self.table_control.down()

        @self.kb.add('c-c')
        def _(event):
            self.cancelled = True
            event.app.exit()

    def addEvent(self, *name: str, fn):
        @self.kb.add(*name)
        def _(event):
            delta = 1 if self.table_control.has_header else 0
            fn(self.table_control.selected - delta)

    def updateValue(self, index, column, value):
        temp = list(self.table["rows"][index])
        temp[column] = value
        self.table["rows"][index] = tuple(temp)

    def show(self):
        self.app.run()
        if self.cancelled:
            return (-1, "Operation cancelled")
        else:
            return (1, "Done")
"""
