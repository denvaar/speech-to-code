from dragonfly import (Grammar, AppContext, MappingRule, Dictation, Integer,
                       Key, Text, Function)

from utils.format import (snake_case, pascal_case, kebab_case, camel_case)

def transform(text, transform_func):
    result = transform_func(text)
    return Text(f'{result}').execute()

grammar = Grammar("general")

class GeneralRule(MappingRule):
    mapping = {
        "tab": Key("tab"),
        "enter": Key("enter"),
        "dictate <text>": Text("%(text)s"),
        "(dictate | type | say) snake [case] <text>": Function(
            lambda text: transform(text, snake_case)),
        "(dictate | type | say) pascal [case] <text>": Function(
            lambda text: transform(text, pascal_case)),
        "(dictate | type | say) kebab [case] <text>": Function(
            lambda text: transform(text, kebab_case)),
        "(dictate | type | say) camel [case] <text>": Function(
            lambda text: transform(text, camel_case)),
    }

    extras = [Dictation("text")]

class SpecialCharacters(MappingRule):
    mapping = {
        "colon [symbol]": Key("colon"),
        "(bang | exclamation) symbol": Key("!"),
        "at symbol": Key("@"),
        "ampersand symbol": Key("&"),
        "(star | asterisk) symbol": Key("*"),
        "(hat | carrot) symbol": Key("^"),
        "question mark symbol": Key("?"),
        "percent (sign | symbol)": Key("percent"),
        "plus (sign | symbol)": Key("+"),
        "(minus | dash) (sign | symbol)": Key("minus"),
        "underscore (sign | symbol)": Key("_"),
        "(pound | hash) (sign | symbol)": Key("#"),
        "tilda (sign | symbol)": Key("~"),
        "dollar (sign | symbol)": Key("$"),
        "equal[s] (sign | symbol)": Key("equal"),
        "space [bar]": Key("space"),

        "(left | open) paren": Key("("),
        "(right | close) paren": Key(")"),
        "parens": Text("()") + Key("left"),

        "(left | open) bracket": Key("["),
        "(right | close) bracket": Key("]"),
        "brackets": Text("[]") + Key("left"),

        "(left | open) brace": Key("{"),
        "(right | close) brace": Key("}"),
        "braces": Text("{}") + Key("left"),

        "single quote": Key("'"),
        "single quotes": Key("singlequote, singlequote, left"),

        "double quote": Key("dquote"),
        "double quotes": Key("dquote, dquote, left"),

        "backticks": Text("``") + Key("left"),

    }

grammar.add_rule(GeneralRule())
grammar.add_rule(SpecialCharacters())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
