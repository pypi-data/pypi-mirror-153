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
                 global_key_bindings=True,
                 show_search=True,
                 show_sort=False
                 ):
        self.table = table
        self.width = os.get_terminal_size().columns
        self.cancelled = False
        self.show_search = show_search
        self.show_sort = show_sort
        self.searched = ""
        self.searched_update = False
        self.sort_methods = {}
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

    def _get_rows_tokens(self):
        rows = super()._get_rows_tokens()
        new_rows = []
        if self.show_search and self.searched != "":
            self.indexes.clear()
            new_index = 0
            old_index = 0
            for row in rows:
                is_filtered = False
                for (style, text) in row:
                    if self.searched.lower() in text.lower():
                        is_filtered = True
                if is_filtered:
                    new_rows.append(row)
                    self.indexes[new_index] = old_index
                    new_index += 1
                old_index += 1
        else:
            new_rows = rows
        return new_rows

    def _get_choice_tokens(self):
        tokens = super()._get_choice_tokens()
        if self.show_search and self.searched != "":
            tokens.append(("", "\n"))
            tokens.append(("bg:ansiyellow fg:ansiblack italic", f"> Searching: {self.searched} "))
        if self.show_search and self.searched_update:
            self.searched_update = False
            self.reset_selection()
        return tokens

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

        @self.key_bindings.add('c-s', '<any>', filter=self.show_sort)
        def _(event):
            char = event.key_sequence[1].data
            if char not in '0123456789':
                return
            char = int(char)
            delta = 1 if self.has_auto else 0

            def sort(row):
                try:
                    return str(row[char-delta])
                except Exception:
                    return ""

            if self.has_auto and char == 0:
                pass
            else:
                if (char - delta) in self.sort_methods.keys():
                    self.table["rows"] = sorted(self.table["rows"], key=self.sort_methods[char - delta])
                else:
                    self.table["rows"] = sorted(self.table["rows"], key=sort)

        @self.key_bindings.add('escape', filter=self.show_search)
        def _(event):
            self.searched = ""
            self.searched_update = True

        @self.key_bindings.add('backspace', filter=self.show_search)
        def _(event):
            self.searched = self.searched[:-1]
            self.searched_update = True

        @self.key_bindings.add('<any>', filter=self.show_search)
        def _(event):
            char = event.key_sequence[0].data
            self.searched += char
            self.searched_update = True

        return self.key_bindings

    def add_sort_method(self, index: int, fn):
        self.sort_methods[index] = fn

    def get_response(self):
        if self.cancelled:
            return (-1, "Operation cancelled")
        else:
            return self.get_current_row()
