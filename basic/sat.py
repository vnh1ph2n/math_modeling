import copy

# =====================================================================
# 1. CÁC HÀM XỬ LÝ CƠ BẢN (CNF & EVALUATION)
# =====================================================================

def eval_literal(literal, assignment):
    """Tính giá trị của 1 literal dựa trên mảng gán assignment."""
    var = abs(literal)
    val = assignment.get(var, None)
    if val is None:
        return None  # Biến chưa được gán (*)
    return val if literal > 0 else not val

def eval_clause(clause, assignment):
    """
    Tính giá trị 1 Clause:
    - True: Ít nhất 1 literal bằng True.
    - False: Tất cả literal đều False (Empty Clause / Violated).
    - None: Chưa chắc chắn (còn literal chưa gán).
    """
    has_unassigned = False
    for literal in clause:
        val = eval_literal(literal, assignment)
        if val is True:
            return True
        if val is None:
            has_unassigned = True
    return None if has_unassigned else False

def simplify(formula, literal):
    """
    Rút gọn CNF khi biết literal là True:
    - Mệnh đề chứa literal -> Bỏ qua (Đã Đúng).
    - Mệnh đề chứa -literal -> Xóa -literal khỏi mệnh đề (Bị Sai).
    """
    new_formula = []
    for clause in formula:
        if literal in clause:
            continue  # Clause thỏa mãn -> Xóa khỏi CNF
        if -literal in clause:
            new_clause = [l for l in clause if l != -literal]
            new_formula.append(new_clause)
        else:
            new_formula.append(clause)
    return new_formula

# =====================================================================
# 2. UNIT CLAUSE PROPAGATION (LAN TRUYỀN MỆNH ĐỀ ĐƠN)
# =====================================================================

def unit_propagation(formula, assignment):
    """
    Tìm các mệnh đề chỉ có 1 literal (Unit Clause) và bắt buộc gán giá trị cho nó.
    Lặp lại cho đến khi không còn Unit Clause nào.
    """
    changed = True
    while changed:
        changed = False
        # Tìm mệnh đề có độ dài bằng 1
        unit_clauses = [c for c in formula if len(c) == 1]
        if unit_clauses:
            unit_literal = unit_clauses[0][0]
            var = abs(unit_literal)
            val = True if unit_literal > 0 else False
            
            # Gán giá trị vào assignment
            assignment[var] = val
            # Rút gọn công thức
            formula = simplify(formula, unit_literal)
            changed = True
            
            # Nếu xuất hiện mệnh đề rỗng [] -> Mâu thuẫn (UNSAT)
            if [] in formula:
                break
                
    return formula, assignment

# =====================================================================
# 3. THUẬT TOÁN CHÍNH (DPLL SOLVER WITH BACKTRACKING)
# =====================================================================

def dpll_solver(formula, assignment, num_vars):
    """
    Luồng chạy chính của SAT Solver:
    - Bước 1: Unit Propagation.
    - Bước 2: Kiểm tra điều kiện dừng (SAT / UNSAT).
    - Bước 3: Thử gán biến chưa gán (Try xi = 1, Try xi = 0).
    """
    # 1. Lan truyền mệnh đề đơn
    formula, assignment = unit_propagation(formula, assignment)
    
    # 2. Kiểm tra mâu thuẫn (Nếu chứa mệnh đề rỗng [])
    if [] in formula:
        return False, None
    
    # 3. Nếu công thức rỗng [] -> Tất cả clause đã thỏa mãn -> SAT!
    if not formula:
        # Điền nốt các biến chưa gán (*) bằng True mặc định
        for v in range(1, num_vars + 1):
            if assignment[v] is None:
                assignment[v] = True
        return True, assignment
    
    # 4. Chọn một biến chưa gán (Unassigned variable xi)
    unassigned_vars = [v for v in range(1, num_vars + 1) if assignment[v] is None]
    if not unassigned_vars:
        return False, None
    
    chosen_var = unassigned_vars[0]
    
    # --- NHÁNH (a): THỬ xi = True (+chosen_var) ---
    assignment_try_true = copy.deepcopy(assignment)
    assignment_try_true[chosen_var] = True
    formula_try_true = simplify(formula, chosen_var)
    
    is_sat, result = dpll_solver(formula_try_true, assignment_try_true, num_vars)
    if is_sat:
        return True, result
        
    # --- NHÁNH (b): THỬ xi = False (-chosen_var) ---
    assignment_try_false = copy.deepcopy(assignment)
    assignment_try_false[chosen_var] = False
    formula_try_false = simplify(formula, -chosen_var)
    
    return dpll_solver(formula_try_false, assignment_try_false, num_vars)

# =====================================================================
# 4. HÀM CHẠY KIỂM THỬ
# =====================================================================

def solve_sat(cnf_formula, num_vars):
    # Khởi tạo Partial Assignment: sigma = *^n
    initial_assignment = {i: None for i in range(1, num_vars + 1)}
    
    is_sat, final_assignment = dpll_solver(cnf_formula, initial_assignment, num_vars)
    
    if is_sat:
        print("RESULT: SATISFIABLE (SAT)")
        print("Valuation (Assignment):", final_assignment)
    else:
        print("RESULT: UNSATISFIABLE (UNSAT)")