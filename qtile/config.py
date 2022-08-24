#   _  _   ___
#  | || | | _ )    Hayden Brown (htbrown.com)
#  | __ | | _ \
#  |_||_| |___/    dotfiles > QTILE
#

### IMPORTS ###

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

from random import randrange

import os
import subprocess

### VARIABLES ###

mod = "mod4"
alt = "mod1"
terminal = "alacritty"
browser = "firefox"
fileexplorer = "thunar"

black = "#202020"
grey = "#3d3d3d"
colours = ( "#DE4242", "#E27837", "#E8D73E", "#5FB43F", "#4780CB", "#CE39C9", "#CD0D59" )
theme = colours[randrange(0, len(colours) - 1)]

### KEYBINDS ###
# https://docs.qtile.org/en/latest/manual/config/lazy.html

keys = [
    # Switch between windows
    #Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    #Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    #Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    #Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    
    # DE-like alt+tab functionality
    Key([alt], "Tab", lazy.layout.next(), desc="Focus on next window"),
    Key([alt, "shift"], "Tab", lazy.layout.previous(), desc="Focus on previous window"),

    # Focus on monitors
    Key([mod], "q", lazy.to_screen(0), desc="Focus on monitor 0"),
    Key([mod], "w", lazy.to_screen(1), desc="Focus on monitor 1"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    
    # Growing/shrinking the main window in Spiral
    Key([mod, "control"], "h", lazy.layout.shrink_main(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_main(), desc="Grow window to the right"),
    Key([mod, "control"], "r", lazy.layout.normalize(), desc="Reset all window sizes"),
    
    # Move between layouts
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    
    # Standard keybinds
    Key([mod], "c", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "l", lazy.spawn("i3lock"), desc="Lock screen"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "shift"], "q", lazy.shutdown(), desc="Shutdown Qtile"),

    # Scrot screenshots
    Key([mod], "Print", lazy.spawn("scrot -s '/tmp/%F_%T_$wx$h.png' -e 'xclip -selection clipboard -target image/png -i $f'"), desc="Take screenshot from selection"),
    Key([mod, "shift"], "Print", lazy.spawn("scrot -u -b '/tmp/%F_%T_$wx$h.png' -e 'xclip -selection clipboard -target image/png -i $f'"), desc="Take screenshot from active window"),

    # Programs
    Key([mod], "space", lazy.spawn("rofi -show drun"), desc="Spawn a command using a prompt widget"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Spawn a terminal"),
    Key([mod, alt], "b", lazy.spawn(browser), desc="Spawn a browser"),
    Key([mod, alt], "d", lazy.spawn("discord"), desc="Spawn Discord"),
    Key([mod, alt], "s", lazy.spawn("steam"), desc="Spawn Steam"),
    Key([mod, alt], "j", lazy.spawn("jetbrains-toolbox"), desc="Spawn JetBrains Toolbox"),
    Key([mod, alt], "v", lazy.spawn("code"), desc="Spawn Visual Studio Code"),
    Key([mod, alt], "f", lazy.spawn(fileexplorer), desc="Spawn file explorer"),
]

### GROUPS ###

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = move focused window to group
            Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
                desc="move focused window to group {}".format(i.name)),
        ]
    )

### LAYOUTS ###
# https://docs.qtile.org/en/latest/manual/ref/layouts.html

layouts = [
    layout.Spiral(
        ratio=0.5,
        new_client_position="bottom",
        border_focus=theme,
        border_normal=grey,
        margin=10,
        border_width=4
    ),
    layout.Max(),
]

# Drag floating layouts
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

### PANEL ###
# https://docs.qtile.org/en/latest/manual/ref/widgets.html

widget_defaults = dict(
    font="JetBrains Mono",
    fontsize=14,
    padding=5,
)
extension_defaults = widget_defaults.copy()

bar_widgets = [
    widget.GroupBox(),
    widget.Prompt(),
    widget.WindowName(),
    widget.Systray(),
    widget.Clock(
        format="%a %d %b"
    ),
    widget.Clock(
        format = "%H:%M"
    ),
]

screens = [
    Screen( top=bar.Bar( bar_widgets, 40 ) ),
]

### HOOKS ###
# https://docs.qtile.org/en/latest/manual/config/hooks.html

# Auto floating dialogs
@hook.subscribe.client_new
def floating_dialogs(window):
    dialog = window.window.get_wm_type() == "dialog"
    transient = window.window.get_wm_transient_for()
    if dialog or transient:
        window.floating = True

# Autostart script
@hook.subscribe.startup_once
def autostart():
    script = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.Popen([script])

# Run every time Qtile restarts
@hook.subscribe.startup
def startup():
    subprocess.Popen(['xsetroot', '-cursor_name', 'BreezeX-Light'])

### MISC ###

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"), # GPG key password entry
        Match(wm_class="origin.exe"),
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = False

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "Qtile"
