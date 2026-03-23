from expr import Binary, Grouping, Literal, Unary, Variable, Assign, Logical, Call


class AstPrinter:
    def print_expr(self, expr):
        if isinstance(expr, Binary):
            return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)
        if isinstance(expr, Grouping):
            return self.parenthesize("group", expr.expression)
        if isinstance(expr, Literal):
            if expr.value is None:
                return "nil"
            return str(expr.value)
        if isinstance(expr, Unary):
            return self.parenthesize(expr.operator.lexeme, expr.right)
        if isinstance(expr, Variable):
            return expr.name.lexeme
        if isinstance(expr, Assign):
            return self.parenthesize(f"assign {expr.name.lexeme}", expr.value)
        if isinstance(expr, Logical):
            return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)
        if isinstance(expr, Call):
            return self.parenthesize("call", expr.callee, *expr.arguments)

        return "unknown"

    def parenthesize(self, name, *exprs):
        parts = [name]
        for expr in exprs:
            parts.append(self.print_expr(expr))
        return "(" + " ".join(parts) + ")"