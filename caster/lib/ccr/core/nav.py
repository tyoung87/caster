'''
Created on Sep 1, 2015

@author: synkarius
'''
from dragonfly import Repeat, Function, Key, Dictation, Choice, Mouse, MappingRule

from caster.lib import context, navigation, alphanumeric, textformat
from caster.lib import control
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.merge.ccrmerger import CCRMerger
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.actions import AsynchronousAction, ContextSeeker
from caster.lib.dfplus.state.actions2 import UntilCancelled
from caster.lib.dfplus.state.short import L, S, R
from dragonfly.actions.action_mimic import Mimic
from caster.lib.ccr.standard import SymbolSpecs

_NEXUS = control.nexus()

class NavigationNon(MappingRule):
    mapping = {
        "<direction> <time_in_seconds>":    AsynchronousAction([L(S(["cancel"], Key("%(direction)s"), consume=False))], 
                                                               repetitions=1000, blocking=False ),
        "erase multi clipboard":            R(Function(navigation.erase_multi_clipboard, nexus=_NEXUS), 
                                              rdescript="Erase Multi Clipboard"),
        "find":                             R(Key("c-f"), rdescript="Find"),
        "find next [<n>]":                  R(Key("f3"), rdescript="Find Next") * Repeat(extra="n"),
        "find prior [<n>]":                 R(Key("s-f3"), rdescript="Find Prior") * Repeat(extra="n"),
        "find everywhere":                  R(Key("cs-f"), rdescript="Find Everywhere"),
        "replace":                          R(Key("c-h"), rdescript="Replace"),
        "(F to | F2)":                      R(Key("f2"), rdescript="Key: F2"),
        "(F six | F6)":                     R(Key("f6"), rdescript="Key: F6"),
        "(F nine | F9)":                    R(Key("f9"), rdescript="Key: F9"),
        
        "[show] context menu":              R(Key("s-f10"), rdescript="Context Menu"),
        
        'kick':                             R(Function(navigation.kick, nexus=_NEXUS), rdescript="Mouse: Left Click"),
        'kick mid':                         R(Function(navigation.kick_middle, nexus=_NEXUS), rdescript="Mouse: Middle Click"),
        'psychic':                          R(Function(navigation.kick_right, nexus=_NEXUS), rdescript="Mouse: Right Click"),
        '(kick double|double kick)':        R(Function(navigation.kick, nexus=_NEXUS) * Repeat(2), rdescript="Mouse: Double Click"),
        "shift right click":                R(Key("shift:down") + Mouse("right") + Key("shift:up"), rdescript="Mouse: Shift + Right Click"),
        "curse <direction> [<direction2>] [<nnavi500>] [<dokick>]": R(Function(navigation.curse), rdescript="Curse"),
        "scree <direction> [<nnavi500>]":   R(Function(navigation.wheel_scroll), rdescript="Wheel Scroll"),
        
        "dug":                              R(Mouse("left:down"), rdescript="Start Mouse Drag"),
        "lego":                            R(Mouse("left:up") + Key("shift:up") + Key("alt:up") + Key("control:up") + Key("win:up"), rdescript="Release Held Keys"),
        
        "colic":                            R(Key("control:down") + Mouse("left") + Key("control:up"), rdescript="Mouse: Ctrl + Left Click"),
        "garb [<nnavi500>]":                R(Mouse("left")+Mouse("left")+Key("c-c")+Function(navigation.clipboard_to_file, nexus=_NEXUS), rdescript="Highlight @ Mouse + Copy"),
        "drop [<nnavi500>]":                R(Mouse("left")+Mouse("left")+Function(navigation.drop, nexus=_NEXUS), rdescript="Highlight @ Mouse + Paste"),
        "fun one":                          R(Key("f1"), rdescript="F1"),
        "fun two":                          R(Key("f2"), rdescript="F2"),
        "fun three":                        R(Key("f3"), rdescript="F3"),
        "fun four":                         R(Key("f4"), rdescript="F4"),
        "fun five":                         R(Key("f5"), rdescript="F5"),
        "fun six":                          R(Key("f6"), rdescript="F6"),
        "fun seven":                        R(Key("f7"), rdescript="F7"),
        "fun eight":                        R(Key("f8"), rdescript="F8"),
        "fun nine":                         R(Key("f9"), rdescript="F9"),
        "fun ten":                          R(Key("f10"), rdescript="F10"),
        "fun eleven":                       R(Key("f11"), rdescript="F11"),
        "fun twelve":                       R(Key("f12"), rdescript="F12"),
        
        "sure stoosh":                      R(Key("c-c"), rdescript="Simple Copy"),
        "sure cut":                         R(Key("c-x"), rdescript="Simple Cut"),
        "sure spark":                       R(Key("c-v"), rdescript="Simple Paste"),
        
        "undo [<n>]":                       R(Key("c-z"), rdescript="Undo") * Repeat(extra="n"),
        "redo [<n>]":                       R(Key("c-y"), rdescript="Redo") * Repeat(extra="n"),

        "refresh":                          R(Key("c-r"), rdescript="Refresh"),
        
        "maxiwin":                          R(Key("w-up"), rdescript="Maximize Window"),
        "move window":                      R(Key("a-space, r, a-space, m"), rdescript="Move Window"),
        "window (left | lease) [<n>]":      R(Key("w-left"), rdescript="Window Left") * Repeat(extra="n"),
        "window (right | ross) [<n>]":      R(Key("w-right"), rdescript="Window Right") * Repeat(extra="n"),
        "monitor (left | lease) [<n>]":     R(Key("sw-left"), rdescript="Monitor Left") * Repeat(extra="n"),
        "monitor (right | ross) [<n>]":     R(Key("sw-right"), rdescript="Monitor Right") * Repeat(extra="n"),
        "(next | prior) window":            R(Key("ca-tab, enter"), rdescript="Next Window"),
        "switch (window | windows)":        R(Key("ca-tab"), rdescript="Switch Window") * Repeat(extra="n"),
        
        "next tab [<n>]":                   R(Key("c-pgdown"), rdescript="Next Tab") * Repeat(extra="n"),
        "prior tab [<n>]":                  R(Key("c-pgup"), rdescript="Previous Tab") * Repeat(extra="n"),
        "close tab [<n>]":                  R(Key("c-w/20"), rdescript="Close Tab") * Repeat(extra="n"),
        
        "elite translation <text>":         R(Function(alphanumeric.elite_text), rdescript="1337 Text"),
        
          }

    extras   = [
              Dictation("text"),
              Dictation("mim"),
              IntegerRefST("n", 1, 50),
              IntegerRefST("nnavi500", 1, 500),
              Choice("time_in_seconds",
                {"super slow": 5, "slow": 2, "normal": 0.6, "fast": 0.1, "superfast": 0.05
                }),
              navigation.get_direction_choice("direction"),
              navigation.get_direction_choice("direction2"),
              navigation.TARGET_CHOICE, 
              Choice("dokick",
                {"kick": 1, "psychic": 2
                }),
              Choice("wm",
                {"ex": 1, "tie": 2
                }),
           ]
    defaults = {
            "n": 1, "mim":"", "nnavi500": 1, "direction2":"", "dokick": 0, "text": "", "wm": 2
           }


class Navigation(MergeRule):
    non = NavigationNon
    pronunciation = CCRMerger.CORE[1]
    
    mapping = {
    # "periodic" repeats whatever comes next at 1-second intervals until "cancel" is spoken or 100 tries occur
    "periodic":                     ContextSeeker(forward=[L(S(["cancel"], lambda: None), \
                                                             S(["*"], \
                                                               lambda fnparams: UntilCancelled(Mimic(*filter(lambda s: s != "periodic", fnparams)), 1).execute(), \
                                                               use_spoken=True))]),
    # VoiceCoder-inspired -- these should be done at the IDE level
    "fill <target>":                R(Key("escape, escape, end"), show=False) +
                                    AsynchronousAction([L(S(["cancel"], Function(context.fill_within_line, nexus=_NEXUS)))
                                                   ], time_in_seconds=0.2, repetitions=50, rdescript="Fill" ),
    "jump in":                      AsynchronousAction([L(S(["cancel"], context.nav, ["right", "(~[~{~<"]))
                                                   ], time_in_seconds=0.1, repetitions=50, rdescript="Jump: In" ),
    "jump out":                     AsynchronousAction([L(S(["cancel"], context.nav, ["right", ")~]~}~>"]))
                                                   ], time_in_seconds=0.1, repetitions=50, rdescript="Jump: Out" ),
    "jump back":                    AsynchronousAction([L(S(["cancel"], context.nav, ["left", "(~[~{~<"]))
                                                   ], time_in_seconds=0.1, repetitions=50, rdescript="Jump: Back" ),
    "jump back in":                 AsynchronousAction([L(S(["cancel"], context.nav, ["left", "(~[~{~<"]))
                                                   ], finisher=Key("right"),
                                                      time_in_seconds=0.1, 
                                                      repetitions=50, 
                                                      rdescript="Jump: Back In" ),
    
    # keyboard shortcuts
    'salve':                         R(Key("c-s"), rspec="save", rdescript="Save"),
    'slap [<nnavi50>]':              R(Key("enter"), rspec="slap", rdescript="Enter")* Repeat(extra="nnavi50"),
    'slap up':                       R(Key("escape, up, end, enter"), rspec="slap up", rdescript="Line Above"),
    'slap down':                     R(Key("escape, end, enter"), rspec="slap down", rdescript="Line Below"),
    'curslap':                       R(Key("escape, lbrace, rbrace, left, enter"), rspec="curslap", rdescript="Curly New Line"),
    
    'north':                     R(Key("c-home"), rspec="north", rdescript="Ctrl Home"),
    'south':                     R(Key("c-end"), rspec="south", rdescript="Ctrl End"),
    'east':                     R(Key("end"), rspec="east", rdescript="End"),
    'west':                     R(Key("home"), rspec="west", rdescript="Home"),
    
    'page up':                     R(Key("pgup"), rspec="page up", rdescript="Page Up"),
    'page down':                     R(Key("pgdown"), rspec="page down", rdescript="Page Down"),
    
    "(<mtn_dir> | <mtn_mode> [<mtn_dir>]) [(<nnavi500> | <extreme>)]": R(Function(textformat.master_text_nav), rdescript="Keyboard Text Navigation"),
    "<short_mode> <key> [<nnavi500>]":        R(Function(textformat.master_short), rdescript="Keyboard Shortcut"),
    "<short_mode> <mouse_action>":            R(Function(textformat.master_short_mouse), rdescript="Mouse Shortcut"),
    "hold <short_mode>":                      R(Function(textformat.hold_modifier), rdescript="Hold Modifier"),
    "alt":                          R(Key("alt"), rdescript="Alt"),
    "wind":                         R(Key("win"), rdescript="Win"),
    "null":                         R(Key("n, u, l, l"), rdescript="Null"),
    
    "stoosh [<nnavi500>]":          R(Key("c-c")+Function(navigation.clipboard_to_file, nexus=_NEXUS), rspec="stoosh", rdescript="Copy"),
    "cut [<nnavi500>]":             R(Key("c-x")+Function(navigation.clipboard_to_file, nexus=_NEXUS), rspec="cut", rdescript="Cut"),
    "spark [<nnavi500>]":           R(Function(navigation.drop, nexus=_NEXUS), rspec="spark", rdescript="Paste"),
    
    "deli [<nnavi50>]":             R(Key("del/5"), rspec="deli", rdescript="Delete") * Repeat(extra="nnavi50"),
    "clear [<nnavi50>]":            R(Key("backspace/5:%(nnavi50)d"), rspec="clear", rdescript="Backspace"),
    SymbolSpecs.CANCEL:             R(Key("escape"), rspec="cancel", rdescript="Cancel Action"),
    
    
    "shackle":                      R(Key("home/5, s-end"), rspec="shackle", rdescript="Select Line"),
    "(tell | tau) <semi>":          R(Function(navigation.next_line), rspec="tell dock", rdescript="Complete Line"), 
    "duple [<nnavi50>]":            R(Key("escape, home, s-end, c-c, end, enter, c-v"), rspec="duple", rdescript="Duplicate Line") * Repeat(extra="nnavi50"),
    "Kraken":                       R(Key("c-space"), rspec="Kraken", rdescript="Control Space"),
         
    # text formatting
    "set format (<spacing> <capitalization> | <capitalization> | <spacing>)":  R(Function(textformat.set_text_format), rdescript="Set Text Format"),
    "clear caster formatting":      R(Function(textformat.clear_text_format), rdescript="Clear Caster Formatting"),
    "peek format":                  R(Function(textformat.peek_text_format), rdescript="Peek Format"),
    "camel <textnv>":                        R(Function(textformat.master_format_text_camel), rdescript="Camel Case"),
    "pascal <textnv>":                       R(Function(textformat.master_format_text_pascal), rdescript="Pascal Case"),
    "dock mel <textnv>":                     R(Key("dot")+Function(textformat.master_format_text_camel), rdescript="Dot Camel Case"),
    "(dop|dot) scal <textnv>":                     R(Key("dot")+Function(textformat.master_format_text_pascal), rdescript="Dot Pascal Case"),
    "(<spacing> <capitalization> | <capitalization> | <spacing>) <textnv>":  R(Function(textformat.master_format_text), rdescript="Text Format"), 
    "format <textnv>":              R(Function(textformat.prior_text_format), rdescript="Last Text Format"),
    
    "dredge":                       R(Key("a-tab"), rdescript="Alt-Tab"),

    }

    extras = [
        alphanumeric.get_key_choice("key"),
        Choice("short_mode",
                {"shift": "s", "troll": "c", "alt": "a", "wind": "w", "trot": "ca", "shoal": "cs", "tron": "wc", "shalt": "sa", "walt": "wa", "shin": "ws", "trash": "cas"
                }),
        Choice("mouse_action",
                {"kick": "left", "kick mid": "middle", "psychic": "right", "dub kick": "left:2"
                }),
        
        IntegerRefST("nnavi50", 1, 50),
        IntegerRefST("nnavi500", 1, 500),
        Dictation("textnv"),
        
        Choice("capitalization",
                  {"scream": 1, "scal": 2,"mel": 3,"tense":4, "laws":5
                  }),
        Choice("spacing",
                  {"smash": 1, "spine": 2, "snake":3
                  }),
        Choice("semi",
                    {"dock": ";", "doc": ";", "sink": ""
                    }),
          
          
          
        navigation.TARGET_CHOICE,
        navigation.get_direction_choice("mtn_dir"),
        Choice("mtn_mode",
                {"shin": "s", "queue": "cs", "fly": "c",
                }),
        Choice("extreme",
                {"Wally": "way",
                }),
    ]

    defaults ={
            "nnavi500": 1, "nnavi50": 1, "textnv": "", "capitalization": 0, "spacing":0, 
            "mtn_mode": None, "mtn_dir": "right", "extreme": None 
           }

control.nexus().merger.add_global_rule(Navigation())