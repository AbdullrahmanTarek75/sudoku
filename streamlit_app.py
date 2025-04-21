import streamlit as st
import random
import time
import copy
from solver_algorithms import solve_backtracking, solve_backtracking_mrv, a_star_sudoku_solver

# 🎲 Functions to shuffle Sudoku rows and columns safely
def shuffle_sudoku(board):
    board = copy.deepcopy(board)

    def shuffle_rows(board):
        for band in range(3):
            rows = list(range(band * 3, (band + 1) * 3))
            random.shuffle(rows)
            board[band*3:(band+1)*3] = [board[r] for r in rows]

    def shuffle_cols(board):
        board_T = list(map(list, zip(*board)))  # transpose
        for stack in range(3):
            cols = list(range(stack * 3, (stack + 1) * 3))
            random.shuffle(cols)
            board_T[stack*3:(stack+1)*3] = [board_T[c] for c in cols]
        return [list(r) for r in zip(*board_T)]

    shuffle_rows(board)
    board = shuffle_cols(board)
    return board

# 📊 Grid display
def display_sudoku_grid(board):
    def cell_html(val):
        return f"<td style='border: 1px solid #333; width: 30px; height: 30px; text-align: center; font-size: 16px; background-color:#F8F8F8'>{val if val != 0 else ''}</td>"

    table_html = "<table style='border-collapse: collapse;'>"
    for i in range(9):
        table_html += "<tr>"
        for j in range(9):
            table_html += cell_html(board[i][j])
            if (j + 1) % 3 == 0 and j != 8:
                table_html += "<td style='width:5px'></td>"
        table_html += "</tr>"
        if (i + 1) % 3 == 0 and i != 8:
            table_html += "<tr style='height:5px'></tr>"
    table_html += "</table>"
    st.markdown(table_html, unsafe_allow_html=True)

# Streamlit UI
st.set_page_config(page_title="Sudoku Solver AI", layout="wide")
st.title("🎲 Random Sudoku Shuffle & Solve")

# Default puzzle
default_board = [
    [5,3,0,0,7,0,0,0,0],
    [6,0,0,1,9,5,0,0,0],
    [0,9,8,0,0,0,0,6,0],
    [8,0,0,0,6,0,0,0,3],
    [4,0,0,8,0,3,0,0,1],
    [7,0,0,0,2,0,0,0,6],
    [0,6,0,0,0,0,2,8,0],
    [0,0,0,4,1,9,0,0,5],
    [0,0,0,0,8,0,0,7,9]
]

# Solve button
if st.button("🧠 Shuffle & Solve"):
    shuffled_board = shuffle_sudoku(default_board)
    
    st.subheader("🧩 Shuffled Puzzle")
    display_sudoku_grid(shuffled_board)

    # Algorithms to solve with
    algorithms = {
        "Backtracking": solve_backtracking,
        "MRV": solve_backtracking_mrv,
        "A* Search": a_star_sudoku_solver
    }

    results = []

    for name, func in algorithms.items():
        st.markdown(f"---\n### 🧩 Solving with **{name}** Algorithm")
        board_copy = copy.deepcopy(shuffled_board)

        start = time.time()
        solved_board = func(board_copy)
        end = time.time()
        elapsed = end - start

        if solved_board:
            st.success(f"✅ Solved in {elapsed:.4f} seconds")
            display_sudoku_grid(solved_board)
        else:
            st.error(f"⚠️ No solution found by {name}")
        
        results.append((name, elapsed, solved_board is not None))

    # 📊 Summary Table for comparison
    st.markdown("---\n## ⏱️ Summary of Results")
    st.table({
        "Algorithm": [r[0] for r in results],
        "Solved": ["✅" if r[2] else "❌" for r in results],
        "Time (s)": [f"{r[1]:.4f}" for r in results]
    })
