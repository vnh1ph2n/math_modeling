class Node:
    """Nút biểu diễn một phần tử trong Parse Tree của Lôgíc mệnh đề."""
    def __init__(self, value, left=None, right=None):
        self.value = value  # 'A', 'B', 'AND', 'OR', 'NOT', 'IMPLIES'
        self.left = left    # Nhánh con trái
        self.right = right  # Nhánh con phải

    def print_tree(self, level=0):
        """In cây cú pháp ra màn hình theo cấp thụt lề trực quan."""
        indent = "  " * level
        print(f"{indent}{self.value}")
        if self.left:
            self.left.print_tree(level + 1)
        if self.right:
            self.right.print_tree(level + 1)


# =====================================================================
# 1. BỘ PHÂN TÍCH CÚ PHÁP (PARSER: CHUỖI TOKENS -> PARSE TREE)
# =====================================================================

def parse_expression(tokens):
    """
    Xây dựng Parse Tree từ danh sách token sử dụng thuật toán phân tích đệ quy.
    Hỗ trợ các dạng:
    - Biến đơn: 'A', 'B', 'C'
    - Phủ định: ['NOT', expr]
    - Phép toán 2 ngôi có ngoặc: ['(', left, OP, right, ')']
    """
    if not tokens:
        return None

    token = tokens.pop(0)

    # Trường hợp 1: Phép phủ định NOT
    if token == 'NOT':
        child = parse_expression(tokens)
        return Node('NOT', left=child)

    # Trường hợp 2: Mở ngoặc -> Biểu thức phức hợp (A OP B)
    if token == '(':
        left_node = parse_expression(tokens)   # Phân tích nhánh trái
        operator = tokens.pop(0)               # Lấy toán tử ('AND', 'OR', 'IMPLIES')
        right_node = parse_expression(tokens)  # Phân tích nhánh phải
        tokens.pop(0)                          # Đóng ngoặc ')'
        return Node(operator, left=left_node, right=right_node)

    # Trường hợp 3: Nút lá (Biến mệnh đề: A, B, C)
    return Node(token)


# =====================================================================
# 2. BỘ ĐÁNH GIÁ NGỮ NGHĨA (EVALUATOR: PARSE TREE -> TRUE/FALSE)
# =====================================================================

def evaluate(node, assignment):
    """
    Duyệt cây đệ quy từ dưới lên để tính giá trị lôgíc của công thức.
    - assignment: Dictionary chứa giá trị gán, ví dụ {'A': True, 'B': False}
    """
    # 1. Nếu là Nút lá (Biến mệnh đề)
    if node.left is None and node.right is None:
        return assignment[node.value]

    # 2. Nếu là phép Phủ định (NOT)
    if node.value == 'NOT':
        return not evaluate(node.left, assignment)

    # 3. Tính giá trị 2 nhánh trái / phải cho toán tử 2 ngôi
    left_val = evaluate(node.left, assignment)
    right_val = evaluate(node.right, assignment)

    if node.value == 'AND':
        return left_val and right_val
    elif node.value == 'OR':
        return left_val or right_val
    elif node.value == 'IMPLIES':
        return (not left_val) or right_val

    raise ValueError(f"Toán tử không hợp lệ: {node.value}")


# =====================================================================
# 3. THUẬT TOÁN BỔ TRỢ: TÌM CÁC BIẾN VÀ TẠO BẢNG CHÂN TRỊ
# =====================================================================

def get_variables(node):
    """Lấy danh sách tất cả các biến mệnh đề độc lập có trong Parse Tree."""
    if node is None:
        return set()
    if node.left is None and node.right is None:
        return {node.value}
    
    vars_set = set()
    if node.left:
        vars_set.update(get_variables(node.left))
    if node.right:
        vars_set.update(get_variables(node.right))
    return vars_set


def generate_truth_table(root_node):
    """Tự động sinh và in toàn bộ Bảng chân trị (Truth Table)."""
    variables = sorted(list(get_variables(root_node)))
    num_vars = len(variables)
    
    print("\n--- BẢNG CHÂN TRỊ (TRUTH TABLE) ---")
    header = " | ".join(variables) + " | Kết quả"
    print(header)
    print("-" * len(header))

    # Duyệt 2^n trường hợp gán True/False
    for i in range(2**num_vars):
        assignment = {}
        for j, var in enumerate(variables):
            # Dùng phép dịch bit để lấy các tổ hợp True/False
            assignment[var] = bool((i >> (num_vars - 1 - j)) & 1)
        
        result = evaluate(root_node, assignment)
        
        row_str = " | ".join(["T" if assignment[v] else "F" for v in variables])
        res_str = "T" if result else "F"
        print(f" {row_str}  |    {res_str}")


# =====================================================================
# 4. CHƯƠNG TRÌNH CHÍNH (DEMO FULL FLOW)
# =====================================================================

if __name__ == "__main__":
    # Xét công thức lôgíc mệnh đề: ((A ∧ B) → ¬C)
    # Tách token thành danh sách biểu diễn chuẩn:
    raw_tokens = [
        '(', '(', 'A', 'AND', 'B', ')', 'IMPLIES', 'NOT', 'C', ')'
    ]

    print("Công thức đầu vào:", " ".join(raw_tokens))

    # Bước 1: Dựng Parse Tree từ danh sách Token
    tree_root = parse_expression(raw_tokens)

    # Bước 2: In cấu trúc Parse Tree
    print("\n--- CAU TRUC PARSE TREE ---")
    tree_root.print_tree()

    # Bước 3: Đánh giá với 1 phép gán cụ thể (A=True, B=True, C=True)
    sample_model = {'A': True, 'B': True, 'C': True}
    sample_result = evaluate(tree_root, sample_model)
    print(f"\nGiá trị biểu thức với gán {sample_model}: {sample_result}")

    # Bước 4: In toàn bộ Bảng chân trị cho tất cả trường hợp
    generate_truth_table(tree_root)