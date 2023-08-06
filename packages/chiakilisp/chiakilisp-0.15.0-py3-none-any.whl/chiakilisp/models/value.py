# pylint: disable=fixme
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=missing-module-docstring

from functools import partial
from typing import Any, Callable, Iterable
from chiakilisp.utils import simple_fuzzy_matched  # <- for proposals
from chiakilisp.utils import get_assertion_closure  # to get ASSERT()
from chiakilisp.models.token import Token  # Value needs Token    :*)

_ASSERT: Callable = get_assertion_closure(NameError)  # <---- closure


def _proposals(glossary: Iterable, item: str) -> str:

    """A little wrapper upon simple_fuzzy_matched()"""

    return ', '.join(simple_fuzzy_matched(item, glossary))


class NotFound:  # pylint: disable=too-few-public-methods  # shut up!

    """
    Stub class to display that there is no such a name in environment
    """


class Value:

    """
    Value is the class that encapsulates single Token, and meant to be a part of Expression (but not always)
    """

    _token: Token
    _properties: dict

    def __init__(self, token: Token) -> None:

        """Initialize Value instance"""

        self._token = token
        self._properties = {}

    def dump(self, indent: int) -> None:

        """Dumps a single expression value"""

        value = self.token().value()

        print(' ' * indent, (f'"{value}"'
                             if self.token().is_string()
                             else value))

    def token(self) -> Token:

        """Returns related token"""

        return self._token

    def set_properties(self, _properties: list) -> None:

        """Allows to set a value property (i.e.: (defn ^t:int () 1))"""

        self._properties = dict(map(lambda prop: prop.split(':'), _properties))

    def property(self,
                 name: str, default=None) -> str:

        """Returns the property by its own name"""

        return self._properties.get(name, default)

    def properties(self) -> dict:

        """Returns all the value props"""

        return self._properties

    def lint(self, _: dict, rule: str, storage: dict) -> None:

        """React to the builtin linter visit"""

        if rule == 'UnusedGlobalVariables' and self.token().type() == Token.Identifier:
            name = self.token().value()
            if name in storage:
                storage[name] += 1  # <- if there is such a global variable, increment its referencing count

    def generate(self, dictionary: dict, cfg: dict, inline: bool):         # pylint: disable=unused-argument

        """Generate C++ representation of the single ChiakiLisp value"""

        token = self.token()  # <------------------------------------------- to refer it for multimple times

        representation = ''

        if token.type() == Token.String:
            representation = f'"{token.value()}"'
        if token.type() in [Token.Nil, Token.Number, Token.Boolean, Token.Identifier]:  # return raw val-str
            if token.type() == Token.Identifier:
                # Try to resolve a C++ name from a dictionary first
                raw = token.value()
                found = dictionary.get(raw)
                if found:
                    return found
                # A bit of demangle processing here for LISPy names
                representation = raw\
                    .replace('?', '_QUESTION_MARK')\
                    .replace('!', '_EXCLAMATION_MARK')
                if not token.value() == '-':
                    representation = representation.replace('-', '_DASH_')  # <--- replace '-' with '_DASH_'
                if not token.value() == '/' or not token.value().endswith('/'):  # TODO: !make this smarter!
                    representation = representation.replace('/', '::')  # <-- replace LISP accessor with C++
            else:
                representation = token.value()  # <-- in all the other cases, return raw string token' value

        return f'{representation}{";" if not inline else ""}'  # <- append semicolon character if not inline

    def execute(self, environment: dict, __=False) -> Any:  # pylint: disable=inconsistent-return-statements

        """Execute, here, is the return Python value related to the value: string, number, and vice versa"""

        if self.token().type() == Token.Nil:

            return None

        if self.token().type() == Token.Number:

            return int(self.token().value())

        if self.token().type() == Token.String:

            return self.token().value()

        if self.token().type() == Token.Boolean:

            return self.token().value() == 'true'

        if self.token().type() == Token.Identifier:

            name = self.token().value()
            where = self.token().position_formatted()  # <- assign to pretty formatted token position string

            ASSERT = partial(_ASSERT, where)  # <---- create partial function to simplify ASSERT() func call
            proposals = partial(_proposals, environment.keys())  # <------- simplify proposals function call

            if '/' in name:
                obj_name, member_name, *_ = name.split('/')  # <------ syntax is <object name>/<member name>
                obj_object = environment.get(obj_name, NotFound)  # <------- assign found object or NotFound
                ASSERT(obj_object is not NotFound,
                       f"no '{obj_name}' object/module in this scope. Possibilities: {proposals(obj_name)}")
                member_object = getattr(obj_object, member_name, NotFound)  # <-------- assign member object
                ASSERT(member_object is not NotFound,
                       f"object (or module) named '{obj_name}' has no such a member named '{member_name}'. "
                       f"Possibilities: {_proposals(dir(member_object), member_name)}")  # <--- maybe cache?
                return member_object  # <------------------ thus we return found module/object member object

            found = environment.get(name, NotFound)  # <-- handle case when identifier name is not qualified

            ASSERT(
                found is not NotFound, f"no '{name}' symbol in this scope. Possibilities: {proposals(name)}"
            )

            return found  # <- return found Python 3 value (from the current environment) or raise NameError


Nil = Value(Token(Token.Nil, 'nil', ()))  # predefined Nil value; (useful for empty defn, fn and let bodies)
Zero = Value(Token(Token.Number, '0', ()))  # predefined Zero value, (useful for empty body of the let/defn)
