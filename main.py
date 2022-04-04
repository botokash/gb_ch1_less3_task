
class Operators:

    __map = {
        '+': (1, lambda x, y: x + y),
        '-': (1, lambda x, y: x - y),
        '*': (2, lambda x, y: x * y),
        '/': (2, lambda x, y: x / y),
    }

    @staticmethod
    def valid(value):
        return value in Operators.__map

    @staticmethod
    def grade(value):
        return Operators.__map[value][0]

    @staticmethod
    def compute(value, x, y):
        return Operators.__map[value][1](x, y)


class CharParser:

    def __init__(self, decimal_separator):
        self.decimal_separator = decimal_separator

    def __check_type(self, char):
        if char.isdigit() or char == self.decimal_separator:
            return 'digit'
        elif char == '(':
            return 'open_bracket'
        elif char == ')':
            return 'close_bracket'
        elif Operators.valid(char):
            return 'operator'
        else:
            return 'error'

    def parse(self, char):
        _type = self.__check_type(char)
        if _type == 'error':
            raise ValueError(f'Parse error, char: {char}')
        else:
            return Lexeme(char, _type)


class Lexeme:

    def __init__(self, char, type):
        self._value = char
        self._type = type

    @property
    def type(self):
        return self._type

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value += value

    @property
    def is_digit(self):
        return self._type == 'digit'

    @property
    def is_open_bracket(self):
        return self._type == 'open_bracket'

    @property
    def is_close_bracket(self):
        return self._type == 'close_bracket'

    @property
    def is_operator(self):
        return self._type == 'operator'

    def to_digit(self):
        self._type = 'digit'


def sorting_yard(expression, parser):
    result_stack = []
    operator_stack = []
    last_lexeme = None

    for char in expression:
        lexeme = parser.parse(char)

        if lexeme.is_digit:
            if last_lexeme and last_lexeme.is_digit:
                result_stack[-1].value = char
            else:
                result_stack.append(lexeme)

        elif lexeme.is_open_bracket:
            operator_stack.append(lexeme)

        elif lexeme.is_close_bracket:
            while operator_stack:
                operator = operator_stack.pop()
                if operator.is_open_bracket:
                    break
                else:
                    result_stack.append(operator)

        elif lexeme.is_operator:
            if (lexeme.value == '-' or lexeme.value == '+')\
                    and (not result_stack or (last_lexeme and
                                              (last_lexeme.is_operator or last_lexeme.is_open_bracket))):
                lexeme.to_digit()
                result_stack.append(lexeme)
            else:
                if operator_stack and Operators.valid(operator_stack[-1].value)\
                        and (Operators.grade(char) <= Operators.grade(operator_stack[-1].value)):
                    result_stack.append(operator_stack.pop())
                operator_stack.append(lexeme)

        last_lexeme = lexeme

    while operator_stack:
        result_stack.append(operator_stack.pop())

    return result_stack


def polish_repr(data):
    tokens = []
    for el in data:
        tokens.append(el.value)
    return ' '.join(tokens)


def calc(stack):
    buff_stack = []
    for lexeme in stack:
        if lexeme.is_operator:
            if len(buff_stack) < 2:
                raise ValueError('Formula incorrect')
            y, x = buff_stack.pop(), buff_stack.pop()
            buff_stack.append(Operators.compute(lexeme.value, x, y))
        else:
            if not lexeme.is_digit:
                raise ValueError('Formula incorrect')
            buff_stack.append(float(lexeme.value))
    return buff_stack[0]


if __name__ == '__main__':

    parser = CharParser('.')

    raw = input()
    raw = raw.replace(' ', '')

    try:
        exp_stack = sorting_yard(raw, parser)
        print(polish_repr(exp_stack))
        result = calc(exp_stack)
        print(result)
    except ValueError as err:
        print(err)
