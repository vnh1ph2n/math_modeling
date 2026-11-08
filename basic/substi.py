class Node:
    pass

class Var(Node):
    def __init__(self, name):
        self.name = name

class Term(Node):
    """Mô tả Term phức hợp như f(x, y)"""
    def __init__(self, name, args):
        self.name = name
        self.args = args

class Predicate(Node):
    def __init__(self, name, args):
        self.name = name
        self.args = args

class Quantifier(Node):
    def __init__(self, q_type, var_name, body):
        self.q_type = q_type
        self.var_name = var_name
        self.body = body

class BinaryOp(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


def substitute(node, var_to_replace, new_term, bound_vars=set()):
    """
    Thực hiện phép thế [var_to_replace => new_term] trên cây AST.
    Chỉ thế các biến KHÔNG nằm trong bound_vars.
    """
    if isinstance(node, Var):
        # Nếu trùng tên biến cần thế VÀ biến này đang TỰ DO -> Thế bằng new_term
        if node.name == var_to_replace and node.name not in bound_vars:
            return new_term
        return node

    elif isinstance(node, Predicate):
        new_args = [substitute(arg, var_to_replace, new_term, bound_vars) for arg in node.args]
        return Predicate(node.name, new_args)

    elif isinstance(node, BinaryOp):
        new_left = substitute(node.left, var_to_replace, new_term, bound_vars)
        new_right = substitute(node.right, var_to_replace, new_term, bound_vars)
        return BinaryOp(node.op, new_left, new_right)

    elif isinstance(node, Quantifier):
        # Khi gặp lượng tử, thêm biến bị ràng buộc vào bound_vars
        new_bound = bound_vars.union({node.var_name})
        new_body = substitute(node.body, var_to_replace, new_term, new_bound)
        return Quantifier(node.q_type, node.var_name, new_body)

    return node