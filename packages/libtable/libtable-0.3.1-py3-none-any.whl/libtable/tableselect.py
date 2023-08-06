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

from prompt_toolkit import Application
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.containers import HSplit
from prompt_toolkit.layout.containers import Window


class TableSelect:
    def __init__(self,
                 table: BaseTableData,
                 full_screen: bool = False,
                 erase_when_done: bool = False,
                 show_header: bool = None,
                 show_auto: bool = None,
                 show_search: bool = True,
                 show_sort: bool = True
                 ) -> None:
        self.table = table
        self.full_screen = full_screen
        self.erase_when_done = erase_when_done
        self.table_control = TableSelectControl(self.table,
                                                show_header=show_header,
                                                show_auto=show_auto,
                                                show_search=show_search,
                                                show_sort=show_sort
                                                )

    def show(self) -> tuple:
        body = HSplit([
            Window(content=self.table_control)
        ])
        self.app = Application(layout=Layout(body),
                               full_screen=self.full_screen,
                               key_bindings=self.table_control.get_key_bindings(),
                               erase_when_done=self.erase_when_done
                               )
        self.app.run()
        return self.table_control.get_response()
