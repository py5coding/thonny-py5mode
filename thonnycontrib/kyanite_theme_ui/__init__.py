'''kyanite ui theme
   theme inspired by processing 4.0b3 default theme, kyanite'''

from thonny import get_workbench
from thonny.plugins.clean_ui_themes import clean

def load_plugin() -> None:
    """Registers the 'Kyanite UI' theme with Thonny's workbench.

    This theme is inspired by Processing 4.0b3's default aesthetic and builds on
    Thonny's 'Clean Sepia' theme, using soft blues and ivory tones for a clean,
    modern look."""

    get_workbench().add_ui_theme('Kyanite UI', 'Clean Sepia', clean(
        frame_background=STEEL_BLUE,
        text_background=IVORY,
        normal_detail=LIGHT_SKY_BLUE,
        high_detail=POWDER_BLUE,
        low_detail=LIGHT_BLUE,
        normal_foreground=MIDNIGHT_BLUE,
        high_foreground=MIDNIGHT_BLUE,
        low_foreground=NAVY,
        custom_menubar=0))


__all__ = 'load_plugin',

STEEL_BLUE      = '#6BA0C7'
IVORY           = '#FFFFF2'
LIGHT_SKY_BLUE  = '#C4E9FF'
POWDER_BLUE     = '#B4D9EF'
LIGHT_BLUE      = '#A4C9DF'
MIDNIGHT_BLUE   = '#002233'
NAVY            = '#000066'
