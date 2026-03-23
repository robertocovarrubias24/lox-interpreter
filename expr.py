class Expr:
    pass


class Binary(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class Grouping(Expr):
    def __init__(self, expression):
        self.expression = expression


class Literal(Expr):
    def __init__(self, value):
        self.value = value


class Unary(Expr):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right


class Variable(Expr):
    def __init__(self, name):
        self.name = name


class Assign(Expr):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class Logical(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class Call(Expr):
    def __init__(self, callee, paren, arguments):
        self.callee = callee
        self.paren = paren
        self.arguments = arguments