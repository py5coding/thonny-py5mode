"""about thonny-py5mode window
accessed via the menu: py5 > about thonny-py5mode
"""

import sys
import platform
import tkinter as tk
import webbrowser
from jpype._jvmfinder import JVMNotFoundException
from tkinter import ttk
from thonny import get_version, get_workbench, ui_utils
from thonny.common import get_python_version_string
from thonny.languages import tr
from ._version import __version__


_PY5_VERSION = "version details in Tools > Manage plug-ins"


def get_os_word_size_guess() -> None:
    """check whether system is 34 or 64-bit"""
    if "32" in platform.machine() and "64" not in platform.machine():
        return "(32-bit)"
    elif "64" in platform.machine() and "32" not in platform.machine():
        return "(64-bit)"
    else:
        return ""


class AboutDialog(ui_utils.CommonDialog):
    def __init__(self, master):
        super().__init__(master)
        # window/frame
        main_frame = ttk.Frame(self)
        main_frame.grid(sticky=tk.NSEW, ipadx=15, ipady=15)
        main_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        self.title(tr("About thonny-py5mode"))
        self.resizable(height=tk.FALSE, width=tk.FALSE)
        self.protocol("WM_DELETE_WINDOW", self._ok)
        # heading
        heading_font = tk.font.nametofont("TkHeadingFont").copy()
        heading_font.configure(size=14, weight="bold")
        heading_label = ttk.Label(
            main_frame,
            text="thonny-py5mode\n" + __version__,
            font=heading_font,
            justify="center",
        )
        heading_label.grid()
        # thonny-py5mode url
        url = "https://github.com/py5coding/thonny-py5mode"
        url_font = tk.font.nametofont("TkDefaultFont").copy()
        url_font.configure(underline=1)
        url_label = ttk.Label(
            main_frame, text=url, style="Url.TLabel", cursor="hand2", font=url_font
        )
        url_label.grid(pady=(0, 20))
        url_label.bind("<Button-1>", lambda _: webbrowser.open(url))
        # os/distro check
        if sys.platform == "linux":
            try:
                import distro

                system_desc = distro.name(True)
            except ImportError:
                system_desc = "Linux"
            if "32" not in system_desc and "64" not in system_desc:
                system_desc += " " + get_os_word_size_guess()
        else:
            system_desc = (
                platform.system()
                + " "
                + platform.release()
                + " "
                + get_os_word_size_guess()
            )
        # list system description and versions of python, py5, thonny
        platform_label = ttk.Label(
            main_frame,
            justify=tk.CENTER,
            text=system_desc
            + "\n Python "
            + get_python_version_string()
            + "\n py5 "
            + _PY5_VERSION
            + "\n Thonny "
            + get_version(),
        )
        platform_label.grid()
        # credits
        credits_label = ttk.Label(
            main_frame,
            text=tr("Built with py5"),
            style="Url.TLabel",
            cursor="hand2",
            font=url_font,
            justify="center",
        )
        credits_label.grid()
        credits_label.bind(
            "<Button-1>",
            lambda _: webbrowser.open("https://py5coding.org/"),
        )
        credits_label.grid(pady=20)
        # buttons
        ok_button = ttk.Button(
            main_frame, text=tr("OK"), command=self._ok, default="active"
        )
        ok_button.grid(pady=(0, 15))
        ok_button.focus_set()
        self.bind("<Return>", self._ok, True)
        self.bind("<Escape>", self._ok, True)

    def _ok(self, event=None) -> None:
        """call when closing window, responsible for handling all cleanup"""
        self.destroy()


def open_about_plugin() -> None:
    """call to display about thonny-py5mode window"""
    ui_utils.show_dialog(AboutDialog(get_workbench()))


def add_about_py5mode_command(group: int) -> None:
    """add about thonny-py5mode to py5 menu"""
    get_workbench().add_command(
        "about_thonny-py5mode",
        "py5",
        tr("About thonny-py5mode"),
        open_about_plugin,
        group=group,
    )
