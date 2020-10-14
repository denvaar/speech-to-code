from dragonfly import (Grammar, CompoundRule, Dictation, Text, Key, AppContext, MappingRule, Choice)

class TypeScriptEnabler(CompoundRule):
    spec = "Enable type script"

    def _process_recognition(self, node, extras):
        typescript_bootstrap.disable()
        typescript_grammar.enable()

        print("TypeScript grammar enabled")

class TypeScriptDisabler(CompoundRule):
    spec = "switch language"

    def _process_recognition(self, node, extras):
        typescript_grammar.disable()
        typescript_bootstrap.enable()

        print("TypeScript grammar disabled")

class TypeScript(MappingRule):
    mapping = {
        "new react component": Key("f, c, tab"),
    }

    extras = []

typescript_bootstrap = Grammar("TypeScript bootstrap")
typescript_bootstrap.add_rule(TypeScriptEnabler())
typescript_bootstrap.load()

typescript_grammar = Grammar("TypeScript grammar")
typescript_grammar.add_rule(TypeScriptDisabler())
typescript_grammar.add_rule(TypeScript())
typescript_grammar.load()
typescript_grammar.disable()

def unload():
    global typescript_grammar
    if typescript_grammar: typescript_grammar.unload()
    typescript_grammar = None
