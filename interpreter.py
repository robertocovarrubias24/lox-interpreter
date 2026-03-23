from expr import Binary, Grouping, Literal, Unary, Variable, Assign, Logical, Call
from stmt import (
    ExpressionStmt,
    PrintStmt,
    VarStmt,
    BlockStmt,
    IfStmt,
    WhileStmt,
    FunctionStmt,
    ReturnStmt,
)


class ReturnException(Exception):
    def __init__(self, value):
        self.value = value


class Environment:
    def __init__(self, enclosing=None):
        self.values = {}
        self.enclosing = enclosing

    def define(self, name, value):
        self.values[name] = value

    def get(self, name):
        if name.lexeme in self.values:
            return self.values[name.lexeme]

        if self.enclosing is not None:
            return self.enclosing.get(name)

        raise RuntimeError(f"Undefined variable '{name.lexeme}'.")

    def assign(self, name, value):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return

        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return

        raise RuntimeError(f"Undefined variable '{name.lexeme}'.")


class LoxFunction:
    def __init__(self, declaration, closure):
        self.declaration = declaration
        self.closure = closure

    def call(self, interpreter, arguments):
        environment = Environment(self.closure)

        for i in range(len(self.declaration.params)):
            param_name = self.declaration.params[i].lexeme
            environment.define(param_name, arguments[i])

        try:
            interpreter.execute_block(self.declaration.body, environment)
        except ReturnException as ret:
            return ret.value

        return None

    def arity(self):
        return len(self.declaration.params)

    def __str__(self):
        return f"<fn {self.declaration.name.lexeme}>"


class Interpreter:
    def __init__(self):
        self.environment = Environment()

    def interpret(self, statements):
        try:
            for stmt in statements:
                self.execute(stmt)
        except RuntimeError as e:
            print(e)

    def execute(self, stmt):
        if isinstance(stmt, ExpressionStmt):
            self.evaluate(stmt.expression)

        elif isinstance(stmt, PrintStmt):
            value = self.evaluate(stmt.expression)
            print(self.stringify(value))

        elif isinstance(stmt, VarStmt):
            value = None
            if stmt.initializer is not None:
                value = self.evaluate(stmt.initializer)
            self.environment.define(stmt.name.lexeme, value)

        elif isinstance(stmt, BlockStmt):
            self.execute_block(stmt.statements, Environment(self.environment))

        elif isinstance(stmt, IfStmt):
            if self.is_truthy(self.evaluate(stmt.condition)):
                self.execute(stmt.then_branch)
            elif stmt.else_branch is not None:
                self.execute(stmt.else_branch)

        elif isinstance(stmt, WhileStmt):
            while self.is_truthy(self.evaluate(stmt.condition)):
                self.execute(stmt.body)

        elif isinstance(stmt, FunctionStmt):
            function = LoxFunction(stmt, self.environment)
            self.environment.define(stmt.name.lexeme, function)

        elif isinstance(stmt, ReturnStmt):
            value = None
            if stmt.value is not None:
                value = self.evaluate(stmt.value)
            raise ReturnException(value)

    def execute_block(self, statements, environment):
        previous = self.environment
        try:
            self.environment = environment
            for stmt in statements:
                self.execute(stmt)
        finally:
            self.environment = previous

    def evaluate(self, expr):
        if isinstance(expr, Literal):
            return expr.value

        elif isinstance(expr, Grouping):
            return self.evaluate(expr.expression)

        elif isinstance(expr, Unary):
            right = self.evaluate(expr.right)
            t = expr.operator.type.name

            if t == "MINUS":
                return -right
            if t == "BANG":
                return not self.is_truthy(right)

        elif isinstance(expr, Binary):
            left = self.evaluate(expr.left)
            right = self.evaluate(expr.right)
            t = expr.operator.type.name

            if t == "PLUS":
                return left + right
            if t == "MINUS":
                return left - right
            if t == "STAR":
                return left * right
            if t == "SLASH":
                return left / right
            if t == "GREATER":
                return left > right
            if t == "GREATER_EQUAL":
                return left >= right
            if t == "LESS":
                return left < right
            if t == "LESS_EQUAL":
                return left <= right
            if t == "EQUAL_EQUAL":
                return left == right
            if t == "BANG_EQUAL":
                return left != right

        elif isinstance(expr, Variable):
            return self.environment.get(expr.name)

        elif isinstance(expr, Assign):
            value = self.evaluate(expr.value)
            self.environment.assign(expr.name, value)
            return value

        elif isinstance(expr, Logical):
            left = self.evaluate(expr.left)

            if expr.operator.type.name == "OR":
                if self.is_truthy(left):
                    return left
            else:
                if not self.is_truthy(left):
                    return left

            return self.evaluate(expr.right)

        elif isinstance(expr, Call):
            callee = self.evaluate(expr.callee)
            arguments = []

            for argument in expr.arguments:
                arguments.append(self.evaluate(argument))

            if not hasattr(callee, "call"):
                raise RuntimeError("Can only call functions.")

            if len(arguments) != callee.arity():
                raise RuntimeError(
                    f"Expected {callee.arity()} arguments but got {len(arguments)}."
                )

            return callee.call(self, arguments)

    def is_truthy(self, value):
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        return True

    def stringify(self, value):
        if value is None:
            return "nil"

        if isinstance(value, float):
            if value.is_integer():
                return str(int(value))
            return str(value)

        return str(value)