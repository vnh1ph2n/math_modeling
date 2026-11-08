class Node:
    """Nút tổng quát trong cây phân tích cú pháp."""
    def __init__(self, value, left=None, right=None, children=None):
        self.value = value        # Giá trị nút: '∀x', '∧', '→', 'P', 'x', ...
        self.left = left          # Con trái (dành cho phép toán 2 ngôi)
        self.right = right        # Con phải (dành cho phép toán 2 ngôi)
        self.children = children or [] # Danh sách con (dành cho Vị tự/Hàm: P(x, y))

    def print_tree(self, level=0):
        """In cây theo dạng phân cấp thụt lề trực quan."""
        indent = "  " * level
        print(f"{indent}{self.value}")
        if self.left:
            self.left.print_tree(level + 1)
        if self.right:
            self.right.print_tree(level + 1)
        for child in self.children:
            child.print_tree(level + 1)


# =====================================================================
# THUẬT TOÁN PARSER ĐƠN GIẢN (PARSE BẰNG CHUỖI KÝ TỰ)
# =====================================================================

def parse_formula(tokens):
    """
    Xây dựng Parse Tree cho công thức dạng: ∀x ((P(x) → Q(x)) ∧ S(x, y))
    """
    if not tokens:
        return None

    token = tokens.pop(0)

    # 1. Lượng tử (Quantifier): ∀x hoặc ∃x
    if token.startswith(('∀', '∃')):
        body = parse_formula(tokens)
        return Node(value=token, left=body)

    # 2. Mở ngoặc: Phân tích biểu thức con bên trong
    if token == '(':
        left = parse_formula(tokens)
        op = tokens.pop(0)  # Lấy toán tử: ∧, ∨, →
        right = parse_formula(tokens)
        tokens.pop(0)       # Bỏ đóng ngoặc ')'
        return Node(value=op, left=left, right=right)

    # 3. Vị tự (Predicate): P(x), Q(x), S(x, y)
    if token in ['P', 'Q', 'S']:
        tokens.pop(0)  # Bỏ '('
        args = []
        while tokens[0] != ')':
            if tokens[0] != ',':
                args.append(Node(value=tokens.pop(0)))
            else:
                tokens.pop(0)  # Bỏ dấu phẩy ','
        tokens.pop(0)  # Bỏ ')'
        return Node(value=token, children=args)

    return Node(value=token)


# =====================================================================
# VÍ DỤ CHẠY MÃ VỚI CÔNG THỨC TRONG SLIDE
# Công thức: ∀x ((P(x) → Q(x)) ∧ S(x, y))
# =====================================================================

# Tách biểu thức thành danh sách các token
expression_tokens = [
    '∀x', '(', '(', 'P', '(', 'x', ')', '→', 'Q', '(', 'x', ')', ')',
    '∧',
    'S', '(', 'x', ',', 'y', ')', ')'
]

# Dựng cây
parse_tree = parse_formula(expression_tokens)

# In cây cú pháp ra màn hình
print("--- PARSE TREE ---")
parse_tree.print_tree()