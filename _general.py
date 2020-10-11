from dragonfly import (Grammar, AppContext, MappingRule, Dictation, Integer,
                       Key, Text)

grammar = Grammar("general")

class GeneralRule(MappingRule):
    mapping = {
        "tab": Key("tab"),
        "enter": Key("enter"),
        "dictate <text>": Text("%(text)s"),
    }

    extras = [Dictation("text")]


grammar.add_rule(GeneralRule())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
