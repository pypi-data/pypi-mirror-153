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

from ._baseclass import BaseTableData
from ._basetablecontrol import BaseTableControl


class TableControl(BaseTableControl):
    def __init__(self,
                 table: BaseTableData,
                 show_header: bool = None,
                 show_auto: bool = None
                 ) -> None:
        self.table = table
        self.width = os.get_terminal_size().columns
        self.__check(show_header, show_auto)
        super().__init__(self.table, self.width)
        self.clear_selection()

    def __check(self,
                show_header: bool,
                show_auto: bool
                ) -> None:
        if show_header is not None:
            self.table.options.show_header = show_header
        if show_auto is not None:
            self.table.options.show_auto = show_auto
