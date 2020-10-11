from dragonfly import (Grammar, AppContext, MappingRule, Dictation, Integer,
                       Key, Function, Text, Choice, CompoundRule, IntegerRef)

from utils.format import (snake_case, pascal_case, kebab_case, camel_case)

class VimContext(AppContext):
    def matches(self, executable, title, handle):
        return title == "Default (nvim)"

class Movement(MappingRule):
    mapping = {
        "[<n>] (down | jay | J)": Text("%(n)dj"),
        "[<n>] (up | kay | K)": Text("%(n)dk"),
        "[<n>] (left | h)": Text("%(n)dh"),
        "[<n>] (right | el | l)": Text("%(n)dl"),

        "[<n>] (word | dub | W)": Text("%(n)dw"),
        "[<n>] big (word | dub | W)": Text("%(n)dW"),

        "[<n>] (bee | B | be)": Text("%(n)db"),
        "[<n>] big (bee | B | be)": Text("%(n)dB"),

        "dollar": Key("$"),
    }

    extras = [
        IntegerRef("n", 1, 900),
    ]

    defaults = {
        "n": 1,
    }

class Editing(MappingRule):
    mapping = {
        "undo": Key("u"),
        "redo": Key("c-r"),

        "(yank | copy | why | Y)": Key("y"),
        "(paste | pea | pee | P)": Key("p"),

        "(delete | D | dee)": Key("d"),

        "repeat [<n> times]": Text("%(n)d."),

        "[<n>] tilda": Text("%(n)d~"),

        "replace <replace_text>": Key("colon, percent, s, slash") + Text("%(replace_text)s/"),
        "with <replace_text>": Text("%(replace_text)s/gc"),
        "yes": Key("y"),
        "no": Key("n"),
        "all": Key("a"),
        "(q | cancel)": Key("q"),
    }

    extras = [
        Dictation("replace_text"),
        IntegerRef("n", 1, 900),
    ]

    defaults = {
        "n": 1,
    }

class Misc(MappingRule):
    mapping = {
        "insert mode": Key("i"),
        "normal mode": Key("escape"),
        "escape": Key("escape"),
        "save": Text(":w\n"),
        "save quit": Text(":wq\n"),
    }

    extras = []

    defaults = {}

def search(text_transform, search_term):
    transformation_functions = {
        'snake': snake_case,
        'pascal': pascal_case,
        'kebab': kebab_case,
        'camel': camel_case,
    }

    transformation = transformation_functions.get(text_transform,
            lambda default: default)(search_term)

    return Text(f'{transformation}').execute()

class Searching(MappingRule):
    mapping = {
        "search [<text_transform> case] <search_term>": Text("/") + Function(search) + Key("enter"),
        "search this word": Text("#"),
        "no (highlight | H L)": Text(":nohl\n"),

        "next": Key("n"),
        "previous": Key("N"),
    }

    extras = [
        Dictation("search_term"),
        Choice("text_transform", {
                "snake": "snake",
                "pascal": "pascal",
                "kebab": "kebab",
                "camel": "camel",
            }, default="")
    ]

vim_context = VimContext(executable="vim")
grammar = Grammar("vim", context=vim_context)

grammar.add_rule(Misc())
grammar.add_rule(Movement())
grammar.add_rule(Editing())
grammar.add_rule(Searching())

grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None

