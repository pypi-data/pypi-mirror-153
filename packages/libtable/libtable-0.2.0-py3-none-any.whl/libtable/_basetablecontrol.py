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

from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.formatted_text import to_formatted_text
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.formatted_text import FormattedText


class BaseTableControl(FormattedTextControl):
    def __init__(self, table, width, **kwargs):
        self.table = table
        self.width = width
        self.rows_count = len(table["rows"])
        self.rows_count_width = len(str(self.rows_count)) + 1
        self.column_count = len(table["headers"])
        self.column_widths: dict = {}
        self.column_align: dict = {}
        self.span = table["options"]["span"] if "options" in table and "span" in table["options"] else 1
        self.has_auto = table["options"]["show_auto"] if "options" in table and "show_auto" in table["options"] else False
        self.has_even = table["options"]["show_even"] if "options" in table and "show_even" in table["options"] else True
        self.has_header = table["options"]["show_header"] if "options" in table and "show_header" in table["options"] else True
        self.header_style = table["options"]["header_style"] if "options" in table and "header_style" in table["options"] else "bold ansimagenta underline"
        self.selection = table["options"]["selection"] if "options" in table and "selection" in table["options"] else True
        self.selection_style = table["options"]["selection_style"] if "options" in table and "selection_style" in table["options"] else "bg:ansiblue"
        self.selected = 1 if self.has_header else 0
        self.__init_table()
        super().__init__(self._get_choice_tokens, show_cursor=False, **kwargs)

    def __init_table(self):
        self.column_widths.clear()
        nb_columns = 0
        available_width = self.width - (self.column_count - 1) * self.span
        available_width -= (self.rows_count_width + self.span) if self.has_auto else 0
        not_done = []
        index = 0
        for header in self.table["headers"]:
            if "width" in header:
                available_width -= header["width"]
                self.column_widths[index] = header["width"]
            else:
                weight = header["weight"] if "weight" in header else 1
                nb_columns += weight
                not_done.append((index, weight))
            rightalign = header["rightalign"] if "rightalign" in header else False
            self.column_align[index] = rightalign
            index += 1
        min_width = int(available_width / nb_columns)
        available_width -= min_width * nb_columns
        for (index, weight) in not_done:
            col_width = min_width * weight
            nb_span = min(weight, available_width)
            col_width += nb_span
            available_width -= nb_span
            self.column_widths[index] = col_width

    def _get_choice_tokens(self):
        tokens = []
        if self.has_header:
            line = ""
            if self.has_auto:
                line += "N".rjust(self.rows_count_width)
                line += "".ljust(self.span)
            index = 0
            for header in self.table["headers"]:
                if "name" not in header:
                    continue
                content = header["name"][0:self.column_widths[index]]
                if self.column_align[index]:
                    content = content.rjust(self.column_widths[index])
                else:
                    content = content.ljust(self.column_widths[index])
                line += content
                if index != self.column_count - 1:
                    line += "".ljust(self.span)
                index += 1
            line += "\n"
            tokens.append((self.header_style, line))
        row_index = 1
        even = True
        for row in self.table["rows"]:
            formatted_line = FormattedText([])
            if self.has_auto:
                formatted_line.append(('', str(row_index).rjust(self.rows_count_width)))
                formatted_line.append(('', "".ljust(self.span)))
            index = 0
            for cell in row:
                if index >= self.column_count:
                    break
                available_width = self.column_widths[index]
                cell_items = to_formatted_text(HTML(cell)) if cell is not None else [('', '')]
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
                    formatted_line.append(('', "".ljust(self.span)))
                index += 1
            while index != self.column_count:
                formatted_line.append(('', "".ljust(self.column_widths[index])))
                if index != self.column_count - 1:
                    formatted_line.append(('', "".ljust(self.span)))
                index += 1
            if row_index != self.rows_count:
                formatted_line.append(('', "\n"))
            style = "bg:#111111" if self.has_even and even else ""
            delta = 0 if self.has_header else 1
            style = self.selection_style if self.selection and row_index == self.selected + delta else style
            formatted_line = to_formatted_text(formatted_line, style=style)
            tokens.extend(formatted_line)
            row_index += 1
            even = not even
        return tokens

    def up(self):
        min_index = 1 if self.has_header else 0
        if self.selected != min_index:
            self.selected -= 1

    def down(self):
        max_delta = 0 if self.has_header else 1
        if self.selected != self.rows_count - max_delta:
            self.selected += 1

    def get_selection(self):
        if self.selected == -1:
            return -1
        delta = 1 if self.has_header else 0
        return self.selected - delta

    def clear_selection(self):
        self.selected = -1

    def reset_selection(self):
        self.selected = 1 if self.has_header else 0

    def set_selection(self, value):
        min_index = 1 if self.has_header else 0
        max_index = self.rows_count - (1 - min_index)
        self.selected = value
        self.selected = max(min_index, self.selected)
        self.selected = min(max_index, self.selected)

    def get_current_index(self):
        return self.get_selection()

    def get_current_row(self):
        if self.selected == -1:
            return (-1, 'No selection')
        return (self.get_selection(), self.table["rows"][self.get_selection()])

    def to_formatted_text(self):
        return FormattedText(self._get_choice_tokens())
