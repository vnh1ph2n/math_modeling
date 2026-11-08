class FreshVariableGenerator:
    """Bộ sinh tên biến mới không đụng hàng."""
    def __init__(self, prefix="z"):
        self.prefix = prefix
        self.counter = 0

    def new_var(self, existing_vars=set()):
        """Trả về một fresh variable đảm bảo không nằm trong existing_vars."""
        while True:
            self.counter += 1
            var_name = f"{self.prefix}_{self.counter}"
            if var_name not in existing_vars:
                return var_name

# --- DEMO ---
generator = FreshVariableGenerator(prefix="z")

# Giả sử tập biến đã xuất hiện trong công thức
used_vars = {'x', 'y', 'z_1'}

fresh_1 = generator.new_var(used_vars) # Trả về 'z_2'
fresh_2 = generator.new_var(used_vars) # Trả về 'z_3'

print("Fresh Variable 1:", fresh_1)
print("Fresh Variable 2:", fresh_2)