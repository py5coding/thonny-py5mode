'''kyanite syntax theme
   theme inspired by processing 4.0b3 default theme, kyanite'''

from thonny import get_workbench, workbench

def load_plugin() -> None:
    """Registers the 'Kyanite Syntax' theme with Thonny's workbench.

    This theme is inspired by the default Processing 4.0b3 theme and builds upon
    Thonny's 'Default Light' syntax theme. It customizes foreground & background
    colors for various syntax elements to create a soft, readable aesthetic."""

    get_workbench().add_syntax_theme(
        'Kyanite Syntax', 'Default Light', KYANITE_SYNTAX)


__all__ = 'load_plugin',

DEFAULT_BG   = '#FFFFF2' # Ivory
DEFAULT_FG   = '#111155' # Dark Indigo
LIGHT_FG     = '#94A4AF' # Light Slate Gray
STRING_FG    = '#7D4793' # Deep Orchid
OPEN_STR_BG  = '#E2E7E1' # Light Gray Green
GUTTER_BG    = '#E2E7E1' # Light Gray Green
GUTTER_FG    = '#A4B4BF' # Pale Steel Blue

PALE_CYAN    = '#D9FAFF'
M_TEAL_BLUE  = '#006699'
LIGHT_BEIGE  = '#F5ECD7'
SEA_GREEN    = '#33997E'
BURNT_ORANGE = '#B04600'
CRIMSON_RED  = '#CC0000'
ROYAL_BLUE   = '#3A66DD'

KYANITE_SYNTAX: workbench.SyntaxThemeSettings = {
    'TEXT': {
        'foreground': DEFAULT_FG,
        'insertbackground': DEFAULT_FG,
        'background': DEFAULT_BG
    },

    'GUTTER': { 'foreground': GUTTER_FG, 'background': GUTTER_BG },

    'breakpoint': { 'foreground': 'crimson' },
    'current_line': { 'background': PALE_CYAN },
    'definition': { 'foreground': M_TEAL_BLUE, 'font': 'BoldEditorFont' },
    'string': { 'foreground': STRING_FG },

    'string3': {
        'foreground': STRING_FG,
        'background': False,
        'font': 'EditorFont'
    },

    'open_string': { 'foreground': STRING_FG, 'background': OPEN_STR_BG },

    'open_string3': {
        'foreground': STRING_FG,
        'background': OPEN_STR_BG,
        'font': 'EditorFont'
    },

    'tab': { 'background': LIGHT_BEIGE },
    'keyword': { 'foreground': SEA_GREEN, 'font': 'EditorFont' },
    'builtin': { 'foreground': M_TEAL_BLUE },
    'number': { 'foreground': BURNT_ORANGE },
    'comment': { 'foreground': LIGHT_FG },
    'welcome': { 'foreground': LIGHT_FG },
    'magic': { 'foreground': LIGHT_FG },
    'prompt': { 'foreground': STRING_FG, 'font': 'BoldEditorFont' },
    'stdin': { 'foreground': 'Blue' },
    'stdout': { 'foreground': 'Black' },
    'stderr': { 'foreground': CRIMSON_RED }, # same as ANSI red
    'value': { 'foreground': 'DarkBlue' },
    'hyperlink': { 'foreground': ROYAL_BLUE, 'underline': True }
}
'''Based on default_light (see thonny > plugins > base_syntax_themes)'''
