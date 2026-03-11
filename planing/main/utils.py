def load_matrix_from_post(post_data):
    
    n = int(post_data.get("n_jobs", 3))
    m = int(post_data.get("m_machines", 3))
    matrix = []

    for i in range(n):
        row = []
        for j in range(m):
            key = f"cell_{i}_{j}"
            val = int(post_data.get(key, 0))
            row.append(val)
        matrix.append(row)
    return matrix


