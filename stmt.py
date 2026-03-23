class Stmt:
    pass


class ExpressionStmt(Stmt):
    def __init__(self, expression):
        self.expression = expression


class PrintStmt(Stmt):
    def __init__(self, expression):
        self.expression = expression


class VarStmt(Stmt):
    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer


class BlockStmt(Stmt):
    def __init__(self, statements):
        self.statements = statements


class IfStmt(Stmt):
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch


class WhileStmt(Stmt):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class FunctionStmt(Stmt):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body


class ReturnStmt(Stmt):
    def __init__(self, keyword, value):
        self.keyword = keyword
        self.value = value