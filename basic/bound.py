class Node:
    pass

class Var(Node):
    def __init__(self, name):
        self.name = name

class Quantifier(Node):
    """Lượng tử: 'forall' hoặc 'exists'"""
    def __init__(self, q_type, var_name, body):
        self.q_type = q_type      # 'forall' hoặc 'exists'
        self.var_name = var_name  # Biến bị ràng buộc, ví dụ 'x'
        self.body = body          # Biểu thức bên trong scope

class BinaryOp(Node):
    """Phép nối lôgíc: 'AND', 'OR', 'IMPLIES'"""
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class Predicate(Node):
    """Vị tự: P(x), Q(x), S(x, y)"""
    def __init__(self, name, args):
        self.name = name
        self.args = args  # Danh sách các Term/Var


# ---------------------------------------------------------------------
# Hàm thuật toán tìm các Biến Tự Do (Free Variables)
# ---------------------------------------------------------------------
def get_free_variables(node, bound_vars=set()):
    """
    Thuật toán duyệt cây đệ quy:
    - Trả về tập hợp các biến tự do (Free Variables) trong công thức.
    """
    if isinstance(node, Var):
        # Nếu biến không nằm trong tập bound_vars -> Là biến tự do
        if node.name not in bound_vars:
            return {node.name}
        return set()

    elif isinstance(node, Predicate):
        free_vars = set()
        for arg in node.args:
            free_vars.update(get_free_variables(arg, bound_vars))
        return free_vars

    elif isinstance(node, BinaryOp):
        left_free = get_free_variables(node.left, bound_vars)
        right_free = get_free_variables(node.right, bound_vars)
        return left_free.union(right_free)

    elif isinstance(node, Quantifier):
        # Khi đi qua một lượng tử (ví dụ ∀x), thêm biến 'x' vào bound_vars
        new_bound = bound_vars.union({node.var_name})
        return get_free_variables(node.body, new_bound)

    return set()

# =====================================================================
# DỰNG CÂY CHO CÔNG THỨC TRONG SLIDE: ∀x ((P(x) → Q(x)) ∧ S(x, y))
# =====================================================================
tree = Quantifier(
    q_type='forall',
    var_name='x',
    body=BinaryOp(
        op='AND',
        left=BinaryOp(
            op='IMPLIES',
            left=Predicate('P', [Var('x')]),
            right=Predicate('Q', [Var('x')])
        ),
        right=Predicate('S', [Var('x'), Var('y')])
    )
)

print("Tập biến tự do (Free Variables):", get_free_variables(tree))
# Đầu ra: {'y'}