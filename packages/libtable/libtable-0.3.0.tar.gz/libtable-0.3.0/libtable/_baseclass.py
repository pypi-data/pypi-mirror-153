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

import json


class BaseTableHeader:
    def __init__(self,
                 column: str,
                 name: str,
                 width: int = -1,
                 weight: int = 1,
                 rightalign: bool = False
                 ) -> None:
        self.column = column
        self.name = name
        self.width = width
        self.weight = weight
        self.rightalign = rightalign

    def to_json(self) -> json:
        return {
            "column": self.column,
            "name": self.name,
            "width": self.width,
            "weight": self.weight,
            "rightalign": self.rightalign
        }

    def __str__(self) -> str:
        return json.dumps(self.to_json(), indent=4)


class BaseTableOptions():
    def __init__(self,
                 span: int = 1,
                 show_auto: bool = False,
                 show_even: bool = True,
                 show_header: bool = True,
                 show_selection: bool = True,
                 header_style: str = "bold ansimagenta underline",
                 selection_style: str = "bg:ansiblue"
                 ) -> None:
        self.span = span
        self.show_auto = show_auto
        self.show_even = show_even
        self.show_header = show_header
        self.show_selection = show_selection
        self.header_style = header_style
        self.selection_style = selection_style

    def to_json(self) -> json:
        return {
            "span": self.span,
            "show_auto": self.show_auto,
            "show_even": self.show_even,
            "show_header": self.show_header,
            "show_selection": self.show_selection,
            "header_style": self.header_style,
            "selection_style": self.selection_style
        }

    def __str__(self) -> str:
        return json.dumps(self.to_json(), indent=4)


class BaseTableData:
    def __init__(self,
                 headers: [BaseTableHeader] = [],
                 rows: [dict] = [],
                 options: BaseTableOptions = BaseTableOptions()
                 ) -> None:
        self.headers: [BaseTableHeader] = headers
        self.rows = rows
        self.options = options

    def add_header(self,
                   column: str,
                   name: str,
                   width: int = -1,
                   weight: int = 1,
                   rightalign: bool = False
                   ):
        self.headers.append(BaseTableHeader(column, name, width=width, weight=weight, rightalign=rightalign))

    def to_json(self) -> json:
        return {
            "headers": list(map(lambda header: header.to_json(), self.headers)),
            "rows": json.loads(self.rows),
            "options": self.options.to_json()
        }

    def __str__(self) -> str:
        return json.dumps(self.to_json(), indent=4)
