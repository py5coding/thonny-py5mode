'''thonny-py5mode JDK installer.
Checks for JDK and, if not found, installs it to Thonny's user directory.'''

import re, shutil, jdk

from pathlib import Path, PurePath
from threading import Thread

from os import environ as env, scandir, rename, PathLike
from os.path import islink, realpath

from typing import Any, Callable, Literal, TypeAlias
from collections.abc import Iterable, Iterator

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

from thonny import get_workbench, ui_utils, THONNY_USER_DIR
from thonny.languages import tr

StrPath: TypeAlias = str | PathLike[str]
'''A type representing string-based filesystem paths.'''

PathAction: TypeAlias = Callable[[StrPath], Any]
'''Represents an action applied to a single path-like object.'''

JDK_PATTERN = re.compile(r"""
    (?:java|jdk)    # Match 'java' or 'jdk' (non-capturing group)
    -?              # Match optional hyphen '-'
    (\d+)           # Capture JDK major version number as group(1)
""", re.IGNORECASE | re.VERBOSE)
'''Captures the major version number from strings like "java-17" or "jdk21".'''

REQUIRE_JDK, VERSION_JDK = 17, '17'
'''JDK minimum required version to run Processing.'''

DOWNLOAD_JDK = '21'
'''JDK version to download.'''

JDK_DIR = 'jdk-' + DOWNLOAD_JDK
'''JDK install subfolder name.'''

THONNY_USER_PATH = Path(THONNY_USER_DIR)
'''Thonny user folder's full path string.'''

JDK_PATH = THONNY_USER_PATH / JDK_DIR
'''Path for JDK installation subfolder.'''

JDK_HOME = str(JDK_PATH)
'''JDK install subfolder's full path string.'''

WORKBENCH = get_workbench()
'''Thonny's workbench singleton instance.'''

def install_jdk() -> None: # Module's main entry-point function
    '''Call this function from where this module is imported.'''

    if is_java_home_set(): return # JAVA_HOME already points to required version

    # Set a local JAVA_HOME to the detected JDK found in THONNY_USER_DIR:
    if path := get_thonny_jdk_install(): set_java_home(path)

    # Otherwise, if Thonny doesn't have a proper JDK version...
    else: ui_utils.show_dialog(JdkDialog()) # ... ask permission to download 1.


def is_java_home_set() -> bool:
    '''Check system for existing JDK that meets the py5 version requirements.'''

    if java_home := env.get('JAVA_HOME'): # Check if JAVA_HOME is already set
        system_jdk = 'TBD' # JDK version To-Be-Determined

        if islink(java_home):
            java_home = realpath(java_home) # If symlink, resolve actual path

        if match := JDK_PATTERN.search(java_home):
            system_jdk = match.group(1) # Get JDK version from 1st match group

        if is_valid_jdk_version(system_jdk) and is_valid_jdk_path(java_home):
            return True # Version is numeric and meets the minimum requirement

    return False # No JAVA_HOME pointing to a required JDK was found


def get_thonny_jdk_install() -> PurePath | Literal['']:
    '''Check Thonny's user folder for a JDK installation subfolder
    and return its path. Otherwise, return an empty string.'''

    for subfolder in get_all_thonny_folders(): # Loop over each subfolder name
        # Use regexp to check if subfolder contains a valid JDK name: 
        if match := JDK_PATTERN.search(subfolder):
            # Check JDK major version from 1st match group:
            if is_valid_jdk_version(match.group(1)):
                # Create a full path by joining THONNY_USER_DIR + folder name:
                jdk_path = adjust_jdk_path(THONNY_USER_PATH / subfolder)

                # Check and return a valid JDK subfolder in THONNY_USER_DIR:
                if is_valid_jdk_path(jdk_path): return jdk_path

    return '' # No JDK with required version found in THONNY_USER_DIR


def set_java_home(jdk_path: StrPath) -> None:
    '''Add JDK path to config file (tools > options > general > env vars).'''

    jdk_path = str(adjust_jdk_path(jdk_path)) # Platform-adjusted path
    env['JAVA_HOME'] = jdk_path # Python's process points to Thonny's JDK too

    jdk_path_entry = create_java_home_entry_from_path(jdk_path)
    env_vars: set[str] = set(WORKBENCH.get_option('general.environment'))

    if jdk_path_entry not in env_vars:
        entries = [*drop_all_java_home_entries(env_vars)]
        entries.append(jdk_path_entry)
        WORKBENCH.set_option('general.environment', entries)
        showinfo('JAVA_HOME', jdk_path, parent=WORKBENCH)


def adjust_jdk_path(jdk_path: StrPath) -> PurePath:
    '''Adjust JDK path for the specificity of current platform.'''

    jdk_path = PurePath(jdk_path)

    # if MacOS, append "/Contents/Home/" to form the actual JDK path for it:
    if jdk.OS is jdk.OperatingSystem.MAC and jdk_path.name != 'Home':
        jdk_path = jdk_path / 'Contents' / 'Home'

    return jdk_path


def create_java_home_entry_from_path(jdk_path: StrPath) -> str:
    '''Prefix JDK path with "JAVA_HOME=" to form a Thonny environment entry.'''
    return f'JAVA_HOME={jdk_path}'


def drop_all_java_home_entries(entries: Iterable[str]) -> Iterator[str]:
    '''Filter out existing entries which start with "JAVA_HOME=".'''
    return filter(_non_java_home_predicate, entries)


def _non_java_home_predicate(entry: str) -> bool:
    '''Check if the entry doesn't start with "JAVA_HOME=".'''
    return not entry.startswith('JAVA_HOME=')


def is_valid_jdk_version(jdk_version: str) -> bool:
    '''Check if JDK version meets minimum version requirement.'''
    return jdk_version.isdigit() and int(jdk_version) >= REQUIRE_JDK


def is_valid_jdk_path(jdk_path: StrPath) -> bool:
    '''Check if the given path points to a JDK install with a usable Java.'''
    java_compiler = jdk._IS_WINDOWS and 'javac.exe' or 'javac'
    return Path(jdk_path, 'bin', java_compiler).is_file()


def get_all_thonny_folders() -> list[str]:
    """Return reverse-sorted names of subfolders within Thonny's user folder."""
    with scandir(THONNY_USER_DIR) as entries:
        return sorted((e.name for e in entries if e.is_dir()), reverse=True)


class JdkDialog(ui_utils.CommonDialog):
    '''User-facing dialog prompting install of required JDK for py5 sketches.
    - Presents user with option to proceed or cancel the JDK installation.
    - Displays a horizontal indeterminate-sized progress bar during download.
    - Launches a background thread to handle installation tasks.
    - Shows a success message when installation is complete.'''

    _TITLE = tr('Install JDK ' + DOWNLOAD_JDK + ' for py5')

    _PROGRESS = tr('Downloading and extracting JDK ' + DOWNLOAD_JDK + ' ...')

    _OK, _CANCEL, _DONE = map(tr, ('Proceed', 'Cancel', 'JDK done'))

    _MSG = 'JDK ' + DOWNLOAD_JDK + tr(' extracted to ') + THONNY_USER_DIR + tr(
        '\n\nYou can now run py5 sketches.')

    _INSTALL_JDK = tr(
        "Thonny requires at least JDK " + VERSION_JDK + " to run py5 sketches. "
        "It'll need to download about 180 MB.")

    _PROGRESS_BAR_Y_PADDING = 0, 15

    def __init__(self, master=WORKBENCH, skip_diag_attribs=False, **kw):
        super().__init__(master, skip_diag_attribs, **kw)

        # Set dialog properties: title, fixed size, close button disabled:
        self.title(self._TITLE) # Dialog title for JDK installation
        self.resizable(height=tk.FALSE, width=tk.FALSE) # Prevent its resizing
        self.protocol('WM_DELETE_WINDOW', '{#}') # Disable its close button

        # Window/Frame:
        main_frame = self.main_frame = ttk.Frame(self)
        main_frame.grid(ipadx=15, ipady=15, sticky=tk.NSEW)
        main_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # Display install message:
        message_label = ttk.Label(main_frame, text=self._INSTALL_JDK)
        message_label.grid(pady=0, columnspan=2)

        # OK proceed button:
        ok_button = self.ok_button = ttk.Button(
            main_frame,
            text=self._OK,
            command=self._proceed,
            default=tk.ACTIVE)

        ok_button.grid(row=2, column=0, padx=15, pady=15, sticky=tk.W)
        ok_button.focus_set()

        # Cancel button:
        cancel_button = self.cancel_button = ttk.Button(
            main_frame,
            text=self._CANCEL,
            command=self._close)

        cancel_button.grid(row=2, column=1, padx=15, pady=15, sticky=tk.E)


    def _proceed(self) -> None:
        '''Starts JDK downloader thread.'''

        # Get rid of both OK & Cancel buttons:
        if self.ok_button: self.ok_button.destroy()
        if self.cancel_button: self.cancel_button.destroy()

        # Progress bar label:
        dl_label = ttk.Label(self.main_frame, text=self._PROGRESS)
        dl_label.grid(row=1, columnspan=2, pady=self._PROGRESS_BAR_Y_PADDING)

        # Progress bar:
        progress_bar = ttk.Progressbar(self.main_frame, mode='indeterminate')

        progress_bar.grid(
            row=2, column=0, columnspan=2,
            padx=15, pady=self._PROGRESS_BAR_Y_PADDING,
            sticky=tk.EW)

        # Start progress bar animation + download thread:
        if self.main_frame: self.main_frame.tkraise()

        download_thread = DownloadJDK()
        download_thread.start()
        progress_bar.start(20)

        self._monitor(download_thread, progress_bar)


    def _monitor(self, download: Thread, progress: ttk.Progressbar) -> None:
        '''Animate progress bar while JDK installs and extracts.'''

        if download.is_alive():
            self.after(100, lambda: self._monitor(download, progress))
            return

        # Destroy this JDK dialog instance once download has finished:
        progress.stop()
        self._close()

        showinfo(self._DONE, self._MSG, parent=WORKBENCH)


    def _close(self) -> None:
        '''Fully shutdown the JdkDialog instance.'''
        self.destroy()
        self.main_frame = self.ok_button = self.cancel_button = None



class DownloadJDK(Thread):
    '''Background thread for downloading & installing JDK into Thonny's folder.
    - Removes any preexisting JDK folders matching the expected version.
    - Downloads and extracts the required JDK version.
    - Renames the downloaded folder to the expected format.
    - Sets JAVA_HOME on Thonny configuration.'''

    def run(self) -> None:
        '''Download and setup JDK (installs to Thonny's user directory)'''

        # Delete existing Thonny's JDK subfolders matching jdk-<version##>:
        self.process_match_jdk_dirs(shutil.rmtree)

        # Download and extract JDK subfolder into Thonny's user folder:
        jdk.install(DOWNLOAD_JDK, path=THONNY_USER_DIR)

        # Rename extracted Thonny's JDK subfolder to jdk-<version##>:
        self.process_match_jdk_dirs(self.rename_folder, True)

        set_java_home(JDK_HOME) # Add a Thonny's JAVA_HOME entry for it


    @staticmethod
    def process_match_jdk_dirs(action: PathAction, only_1st=False) -> None:
        '''Apply an action to JDK-matching subfolders in Thonny's folder.'''

        for path in DownloadJDK.get_all_thonny_folder_paths():
            if path.name.startswith(JDK_DIR): # Folder name matches <jdk-##> 
                action(path) # Callback to run on each matching folder path
                if only_1st: break # Stop at 1st match occurrence


    @staticmethod
    def get_all_thonny_folder_paths() -> Iterator[Path]:
        '''Find all subfolder paths within Thonny's user folder'''
        return filter(Path.is_dir, THONNY_USER_PATH.iterdir())


    @staticmethod
    def rename_folder(path: StrPath) -> None:
        '''Rename a JDK subfolder to the expected jdk-<version##> format.'''
        rename(path, JDK_PATH)
