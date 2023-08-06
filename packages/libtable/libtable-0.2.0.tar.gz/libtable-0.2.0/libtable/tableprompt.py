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
from prompt_toolkit import prompt
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.validation import Validator


class TablePrompt:
    def __init__(self,
                 table,
                 show_header=True,
                 show_auto=False,
                 index_column="auto",
                 prompt_style="yellow"
                 ):
        self.table = table
        self.index_column = index_column
        self.prompt_style = prompt_style
        self.valid = True
        self.error_message = ""
        self.__get_valid_values()
        self.table_control = TableControl(table, show_header=show_header, show_auto=show_auto)
        self.table_control.clear_selection()
        self.validator = Validator.from_callable(
            self.__is_valid_index,
            error_message=f"Invalid input ({self.index_column} value expected)",
            move_cursor_to_end=True,
        )

    def __get_valid_values(self):
        self.valid_values = []
        if self.index_column == "auto":
            if not self.table["options"]["show_auto"]:
                self.valid = False
                self.error_message = "ERROR: index_column is auto but no auto column"
            else:
                self.valid_values = list(range(1, len(self.table["rows"]) + 1))
        else:
            headers = list(map(lambda x: x["name"], self.table["headers"]))
            if self.index_column not in headers:
                self.valid = False
                self.error_message = "ERROR: index_column is not a valid column"
            else:
                self.column_index = headers.index(self.index_column)
                self.valid_values = list(map(lambda x: x[self.column_index] if len(list(x)) > self.column_index else None, self.table["rows"]))
                self.valid_values = list(filter(None, self.valid_values))
                self.valid_values = list(filter(lambda x: str(x).isnumeric(), self.valid_values))
                if len(self.valid_values) == 0:
                    self.valid = False
                    self.error_message = "ERROR: no valid values"
                self.valid_values = list(map(lambda x: int(x), self.valid_values))

    def __is_valid_index(self, text):
        try:
            index = int(text)
        except ValueError:
            return False
        return index in self.valid_values

    def show(self):
        if not self.valid:
            return (-1, self.error_message)
        print_formatted_text(FormattedText(self.table_control._get_choice_tokens()))
        try:
            message_part = "index" if self.index_column == "auto" else self.index_column
            index = int(prompt(FormattedText([(self.prompt_style, f"Enter {message_part}: ")]), validator=self.validator, validate_while_typing=False))
        except KeyboardInterrupt:
            return (-1, "Operation cancelled")
        if self.index_column == "auto":
            return (index - 1, self.table["rows"][index - 1])
        else:
            return (index, list(filter(lambda x: int(x[self.column_index]) == index, self.table["rows"]))[0])
