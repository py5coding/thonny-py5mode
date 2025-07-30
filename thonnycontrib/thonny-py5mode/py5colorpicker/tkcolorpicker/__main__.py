# -*- coding: utf-8 -*-
"""
tkcolorpicker - Alternative to colorchooser for Tkinter.
Copyright 2017 Juliette Monsel <j_4321@protonmail.com>

tkcolorpicker is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

tkcolorpicker is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Example
"""


from .functions import tk, ttk
from . import askcolor


def select_color1():
    print(askcolor(color="sky blue", parent=root))


def select_color2():
    print(askcolor(color=(255, 120, 0, 100), parent=root, alpha=True))


root = tk.Tk()
s = ttk.Style(root)
s.theme_use('clam')
ttk.Label(root, text='Color Selection:').pack(padx=4, pady=4)
ttk.Button(root, text='solid color',
           command=select_color1).pack(fill='x', padx=4, pady=4)
ttk.Button(root, text='with alpha channel',
           command=select_color2).pack(fill='x', padx=4, pady=4)
root.mainloop()
