'''thonny-py5mode JDK installer
   checks for JDK and, if not found, installs it to the Thonny config directory
'''

import re
import shutil
import jdk

from pathlib import Path
from threading import Thread

from os import environ as env, scandir, rename
from os.path import islink, realpath

from collections.abc import Generator, Iterator

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

from thonny import get_workbench, ui_utils, THONNY_USER_DIR
from thonny.languages import tr

_JDK_PATTERN = re.compile(r"""
    (?:java|jdk)    # Match 'java' or 'jdk' (non-capturing group)
    -?              # Match optional hyphen '-'
    (\d+)           # Capture JDK major version number as group(1)
""", re.IGNORECASE | re.VERBOSE)

_REQUIRE_JDK, _VERSION_JDK = 17, '17'
_JDK_DIR = 'jdk-' + _VERSION_JDK

_THONNY_USER_PATH = Path(THONNY_USER_DIR)
_JDK_PATH = _THONNY_USER_PATH / _JDK_DIR
_JDK_HOME = str(_JDK_PATH)

def install_jdk(): # Module's main entry-point function
    '''Call this function from where this module is imported.'''
    if is_java_home_set(): return # JAVA_HOME points to a required JDK version

    if not jdk_install_exists(): # If Thonny doesn't have a proper JDK version
        ui_utils.show_dialog(JdkDialog(get_workbench())) # ask to download it...


def is_java_home_set() -> bool:
    '''Check system for existing JDK that meets the py5 version requirements.'''
    if (java_home := env.get('JAVA_HOME')): # Check if JAVA_HOME is set
        system_jdk = 'TBD' # JDK version To-Be-Determined

        if islink(java_home):
            java_home = realpath(java_home) # If symlink, resolve actual path

        if (match := _JDK_PATTERN.search(java_home)):
            system_jdk = match.group(1) # Get JDK version from 1st match group

        if system_jdk.isdigit() and int(system_jdk) >= _REQUIRE_JDK and\
            is_valid_jdk_path(java_home):
            return True # Version is numeric and meets the minimum requirement

    return False # No JAVA_HOME pointing to a required JDK was found


def jdk_install_exists() -> bool:
    '''Check Thonny's user folder for a JDK installation subfolder'''
    for subfolder in get_all_thonny_folders():
        if (match := _JDK_PATTERN.search(subfolder)):
            jdk_version = match.group(1) # Get JDK version from 1st match group
            jdk_path = _THONNY_USER_PATH / subfolder

            if jdk_version.isdigit() and int(jdk_version) >= _REQUIRE_JDK and\
                is_valid_jdk_path(jdk_path):
                # Set a local JAVA_HOME to the detected JDK in THONNY_USER_DIR:
                set_java_home(jdk_path)

                return True # Found a valid JDK subfolder in THONNY_USER_DIR

    return False # Neither existing JAVA_HOME nor any JDK in THONNY_USER_DIR


def set_java_home(jdk_path: Path | str):
    '''Add JDK path to config file (tools > options > general > env vars).'''
    jdk_path = get_platform_specific_jdk_path(jdk_path)
    workbench = get_workbench()
    env_vars: list[str] = workbench.get_option('general.environment')

    if jdk_path not in env_vars:
        env_vars.append(jdk_path)
        workbench.set_option('general.environment', env_vars)
        showinfo('JAVA_HOME', jdk_path, master=workbench)


def is_valid_jdk_path(path: Path | str) -> bool:
    '''Check if the given path points to a JDK install with a usable Java.'''
    return Path(path, 'bin', 'java').is_file()


def get_platform_specific_jdk_path(path: Path | str) -> str:
    '''Return properly formatted JAVA_HOME string based on platform.'''
    path = Path(path)

    # if Mac ARM system, add "/Contents/Home/" to JDK path:
    if jdk.OS == jdk.OperatingSystem.MAC and jdk.ARCH == jdk.Architecture.ARM:
        path = path / 'Contents' / 'Home'

    return f'JAVA_HOME={path}'


def get_all_thonny_folders() -> Generator[str]:
    '''Yield subfolder names within Thonny's user folder'''
    with scandir(THONNY_USER_DIR) as entries:
        yield from (e.name for e in entries if e.is_dir())


def get_all_thonny_folder_paths() -> Iterator[Path]:
    '''Find all subfolder paths within Thonny's user folder'''
    return filter(Path.is_dir, _THONNY_USER_PATH.iterdir())


class DownloadJDK(Thread):
    '''Background thread for downloading & installing JDK into Thonny's folder.

    - Removes any preexisting JDK folders matching the expected version.
    - Downloads and extracts the required JDK version.
    - Renames the downloaded folder to the expected format.
    - Sets JAVA_HOME both in system environment and Thonny configuration.
    '''
    def run(self):
        '''Download and setup JDK (installs to Thonny's config directory)'''
        for path in get_all_thonny_folder_paths():
            # Delete existing thonny-py5mode JDK (if one exists):
            if path.name.startswith(_JDK_DIR):
                shutil.rmtree(path)
                break

        # Download and extract JDK:
        jdk.install(_VERSION_JDK, path=THONNY_USER_DIR)

        for path in get_all_thonny_folder_paths():
            # Rename extracted JDK directory to jdk-<version##>:
            if path.name.startswith(_JDK_DIR):
                rename(path, _JDK_PATH)
                break

        # Set JAVA_HOME:
        set_java_home(_JDK_HOME)
        env['JAVA_HOME'] = _JDK_HOME


class JdkDialog(ui_utils.CommonDialog):
    '''User-facing dialog prompting install of required JDK for py5 sketches.

    - Presents user with option to proceed or cancel the JDK installation.
    - Displays an indeterminate progress bar during download.
    - Launches a background thread to handle installation tasks.
    - Shows a success message when installation is complete.
    '''
    _TITLE = tr('Install JDK ' + _VERSION_JDK + ' for py5')

    _PROGRESS = tr(f'Downloading and extracting JDK {_REQUIRE_JDK} ...')

    _OK, _CANCEL, _DONE = map(tr, ('Proceed', 'Cancel', 'JDK done'))

    _MSG = 'JDK ' + _VERSION_JDK + tr(' extracted to ') + THONNY_USER_DIR + tr(
        '\n\nYou can now run py5 sketches.')

    _INSTALL_JDK = tr(
        "Thonny requires JDK " + _VERSION_JDK + " to run py5 sketches. "
        "It'll need to download about 180 MB."
    )

    _PAD = 0, 15

    def __init__(self, master=None, skip_diag_attribs=False, **kw):
        super().__init__(master, skip_diag_attribs, **kw)

        # Window/Frame:
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(ipadx=15, ipady=15, sticky=tk.NSEW)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)

        self.title(self._TITLE)
        self.resizable(height=tk.FALSE, width=tk.FALSE)
        self.protocol('WM_DELETE_WINDOW', '{#}') # No window close button

        # Display install message:
        message_label = ttk.Label(self.main_frame, text=self._INSTALL_JDK)
        message_label.grid(pady=0, columnspan=2)

        # OK button:
        self.ok_button = ttk.Button(
          self.main_frame,
          text=self._OK,
          command=self._proceed,
          default=tk.ACTIVE
        )

        self.ok_button.grid(
            row=2, column=0,
            padx=15, pady=15,
            sticky=tk.W
        )

        self.ok_button.focus_set()

        # Cancel button:
        self.cancel_button = ttk.Button(
          self.main_frame,
          text=self._CANCEL,
          command=self._close
        )

        self.cancel_button.grid(
            row=2, column=1,
            padx=15, pady=15,
            sticky=tk.E
        )


    def _proceed(self):
        '''Starts JDK downloader thread.'''
        # Get rid of both OK & Cancel buttons:
        if self.ok_button: self.ok_button.destroy()
        if self.cancel_button: self.cancel_button.destroy()

        # Progress bar label:
        dl_label = ttk.Label(self.main_frame, text=self._PROGRESS)
        dl_label.grid(row=1, columnspan=2, pady=self._PAD)

        # Progress bar:
        progress_bar = ttk.Progressbar(
            self.main_frame,
            orient=tk.HORIZONTAL,
            mode='indeterminate'
        )

        progress_bar.grid(
            row=2, column=0, columnspan=2,
            padx=15, pady=self._PAD,
            sticky=tk.EW
        )

        # Start progress bar animation and download thread:
        if self.main_frame: self.main_frame.tkraise()

        download_thread = DownloadJDK()
        download_thread.start()
        progress_bar.start(20)

        self._monitor(download_thread, progress_bar)


    def _close(self):
        '''Fully shutdown the JdkDialog instance.'''
        self.destroy()
        self.main_frame = self.ok_button = self.cancel_button = None


    def _monitor(self, download: Thread, progress: ttk.Progressbar):
        '''Animate progress bar while JDK installs and extracts.'''
        if download.is_alive():
            self.after(100, lambda: self._monitor(download, progress))
            return

        progress.stop()
        self._close()

        showinfo(self._DONE, self._MSG, master=get_workbench())
