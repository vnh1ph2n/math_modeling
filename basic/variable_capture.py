class Node:
    pass

class Var(Node):
    def __init__(self, name):
        self.name = name

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


def get_vars_in_term(term_node):
    """Lấy danh sách các biến có trong term t."""
    if isinstance(term_node, Var):
        return {term_node.name}
    elif isinstance(term_node, Predicate):
        vars_set = set()
        for arg in term_node.args:
            vars_set.update(get_vars_in_term(arg))
        return vars_set
    return set()


def substitute_safe(node, var_to_replace, new_term, bound_vars=set(), fresh_counter=[0]):
    """
    Phép thế an toàn (Capture-avoiding substitution):
    Tự động rename bound variable nếu trùng với biến trong new_term.
    """
    if isinstance(node, Var):
        if node.name == var_to_replace and node.name not in bound_vars:
            return new_term
        return node

    elif isinstance(node, Predicate):
        new_args = [substitute_safe(arg, var_to_replace, new_term, bound_vars, fresh_counter) for arg in node.args]
        return Predicate(node.name, new_args)

    elif isinstance(node, BinaryOp):
        new_left = substitute_safe(node.left, var_to_replace, new_term, bound_vars, fresh_counter)
        new_right = substitute_safe(node.right, var_to_replace, new_term, bound_vars, fresh_counter)
        return BinaryOp(node.op, new_left, new_right)

    elif isinstance(node, Quantifier):
        term_vars = get_vars_in_term(new_term)
        q_var = node.var_name
        
        # KIỂM TRA NGUY CƠ CAPTURE:
        # Nếu biến của lượng tử (node.var_name) nằm trong danh sách biến của new_term
        if q_var in term_vars:
            # Tạo tên biến mới hoàn toàn (ví dụ: z_1, z_2, ...)
            fresh_counter[0] += 1
            new_q_var = f"z_{fresh_counter[0]}"
            
            # Đổi tên biến q_var thành new_q_var trong body của lượng tử
            renamed_body = substitute_safe(node.body, q_var, Var(new_q_var), bound_vars, fresh_counter)
            
            # Tiếp tục thế var_to_replace trên body đã được rename
            new_bound = bound_vars.union({new_q_var})
            new_body = substitute_safe(renamed_body, var_to_replace, new_term, new_bound, fresh_counter)
            return Quantifier(node.q_type, new_q_var, new_body)
        else:
            new_bound = bound_vars.union({q_var})
            new_body = substitute_safe(node.body, var_to_replace, new_term, new_bound, fresh_counter)
            return Quantifier(node.q_type, q_var, new_body)

    return node