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
from ._baseclass import BaseTableHeader

from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.formatted_text import to_formatted_text
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.formatted_text import FormattedText


class BaseTableControl(FormattedTextControl):
    def __init__(self,
                 table: BaseTableData,
                 width: int,
                 **kwargs
                 ) -> None:
        self.table = table
        self.width = width
        self.rows_count = len(self.table.rows)
        self.rows_count_width = len(str(len(self.table.rows))) + 1
        self.column_count = len(self.table.headers)
        self.column_widths: dict = {}
        self.column_align: dict = {}
        self.selected = 1 if self.table.options.show_header else 0
        self.indexes = {}
        self.__init_table()
        super().__init__(self._get_choice_tokens, show_cursor=False, **kwargs)

    def __init_table(self) -> None:
        self.column_widths.clear()
        nb_columns = 0
        available_width = self.width - (self.column_count - 1) * self.table.options.span
        available_width -= (self.rows_count_width + self.table.options.span) if self.table.options.show_auto else 0
        not_done = []
        index = 0
        header: BaseTableHeader
        for header in self.table.headers:
            if header.width != -1:
                available_width -= header.width
                self.column_widths[index] = header.width
            else:
                nb_columns += header.weight
                not_done.append((index, header.weight))
            self.column_align[index] = header.rightalign
            index += 1
        min_width = int(available_width / nb_columns)
        available_width -= min_width * nb_columns
        for (index, weight) in not_done:
            col_width = min_width * weight
            nb_span = min(weight, available_width)
            col_width += nb_span
            available_width -= nb_span
            self.column_widths[index] = col_width

    def _get__header_tokens(self) -> FormattedText([]):
        tokens = []
        if self.table.options.show_header:
            line = ""
            if self.table.options.show_auto:
                line += "N".rjust(self.rows_count_width)
                line += "".ljust(self.table.options.span)
            index = 0
            header: BaseTableHeader
            for header in self.table.headers:
                content = header.name[0:self.column_widths[index]]
                if self.column_align[index]:
                    content = content.rjust(self.column_widths[index])
                else:
                    content = content.ljust(self.column_widths[index])
                line += content
                if index != self.column_count - 1:
                    line += "".ljust(self.table.options.span)
                index += 1
            line += "\n"
            tokens.append((self.table.options.header_style, line))
        return tokens

    def _get_rows_tokens(self) -> [FormattedText([])]:
        self.indexes.clear()
        tokens = []
        row_index = 1
        row: dict
        for row in self.table.rows:
            formatted_line = FormattedText([])
            if self.table.options.show_auto:
                formatted_line.append(('', str(row_index).rjust(self.rows_count_width)))
                formatted_line.append(('', "".ljust(self.table.options.span)))
            index = 0

            header: BaseTableHeader
            for header in self.table.headers:
                available_width = self.column_widths[index]
                cell_items = [('', '')]
                if header.column in row.keys():
                    cell_items = to_formatted_text(HTML(row[header.column]))
                temp_items = []
                for cell_item in cell_items:
                    content = cell_item[1][0:available_width]
                    available_width -= len(content)
                    temp_items.append((cell_item[0], content))
                if available_width > 0 and self.column_align[index]:
                    formatted_line.append(('', "".rjust(available_width)))
                formatted_line.extend(temp_items)
                if available_width > 0 and not self.column_align[index]:
                    formatted_line.append(('', "".rjust(available_width)))
                if index != self.column_count - 1:
                    formatted_line.append(('', "".ljust(self.table.options.span)))
                index += 1

            tokens.append(formatted_line)
            self.indexes[row_index - 1] = row_index - 1
            row_index += 1
        return tokens

    def __get_rows_tokens_with_style(self) -> FormattedText([]):
        rows = self._get_rows_tokens()
        self.rows_count = len(rows)
        tokens = []
        even = True
        row_index = 1
        for row in rows:
            style = "bg:#222222" if self.table.options.show_even and even else ""
            delta = 0 if self.table.options.show_header else 1
            style = self.table.options.selection_style if self.table.options.show_selection and row_index == self.selected + delta else style
            if row_index != self.rows_count:
                row.append(('', "\n"))
            formatted_line = to_formatted_text(row, style=style)
            tokens.append(formatted_line)
            row_index += 1
            even = not even
        if self.rows_count == 0:
            tokens.append([("italic fg:grey", "No data")])
        return tokens

    def _get_choice_tokens(self) -> FormattedText([]):
        tokens = []
        if self.table.options.show_header:
            tokens.extend(self._get__header_tokens())
        for row in self.__get_rows_tokens_with_style():
            tokens.extend(row)
        return tokens

    def up(self) -> None:
        min_index = 1 if self.table.options.show_header else 0
        if self.selected != min_index:
            self.selected -= 1

    def down(self) -> None:
        max_delta = 0 if self.table.options.show_header else 1
        if self.selected != self.rows_count - max_delta:
            self.selected += 1

    def get_selection(self) -> int:
        if self.selected == -1:
            return -1
        delta = 1 if self.table.options.show_header else 0
        return self.selected - delta

    def clear_selection(self) -> None:
        self.selected = -1

    def reset_selection(self) -> None:
        self.selected = 1 if self.table.options.show_header else 0

    def set_selection(self, value) -> None:
        min_index = 1 if self.table.options.show_header else 0
        max_index = self.rows_count - (1 - min_index)
        self.selected = value
        self.selected = max(min_index, self.selected)
        self.selected = min(max_index, self.selected)

    def get_current_index(self) -> int:
        try:
            return self.indexes[self.get_selection()]
        except Exception:
            return -1

    def get_current_row(self) -> tuple:
        index = self.get_current_index()
        if index == -1:
            return (-1, 'No selection')
        return (index, self.table.rows[index])

    def to_formatted_text(self) -> FormattedText:
        return FormattedText(self._get_choice_tokens())
