import streamlit as st
import base64
import os
from fpdf import FPDF

st.set_page_config(page_title="Cryptarithmetic Solver", layout="wide")

# ---------- Session State ----------
if "solutions" not in st.session_state:
    st.session_state.solutions = None
    st.session_state.attempts = 0

# ---------- Background ----------
def set_bg_image(image_file):
    if not os.path.exists(image_file):
        return
    with open(image_file, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .stApp::before {{
            content: "";
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.6);
            z-index: -1;
        }}
        </style>
    """, unsafe_allow_html=True)

set_bg_image("bg.png")

# ---------- UI ----------
st.title("🔐 Cryptarithmetic Puzzle Solver")

first = st.text_input("First Word", "SEND").upper()
second = st.text_input("Second Word", "MORE").upper()
result = st.text_input("Result Word", "MONEY").upper()

# ---------- CSP Solver ----------
@st.cache_data
def solve_csp(first, second, result):
    unique_letters = set(first + second + result)
    if len(unique_letters) > 10:
        return None, "Too many unique letters!", 0

    letters = []
    max_len = max(len(first), len(second), len(result))
    for i in range(1, max_len + 1):
        for word in [first, second, result]:
            if i <= len(word):
                c = word[-i]
                if c not in letters:
                    letters.append(c)

    assignment = {}
    used_digits = set()
    attempts = 0
    solutions = []

    def word_to_num(word):
        return int("".join(str(assignment[c]) for c in word))

    def is_valid_partial():
        carry = 0
        for i in range(1, max_len + 1):
            f = first[-i] if i <= len(first) else None
            s = second[-i] if i <= len(second) else None
            r = result[-i] if i <= len(result) else None

            if all(x is None or x in assignment for x in [f, s, r]):
                total = carry
                if f: total += assignment[f]
                if s: total += assignment[s]

                expected = total % 10
                carry = total // 10

                if r and assignment[r] != expected:
                    return False
            else:
                break
        return True

    def backtrack(index):
        nonlocal attempts

        if index == len(letters):
            n1 = word_to_num(first)
            n2 = word_to_num(second)
            n3 = word_to_num(result)

            if n1 + n2 == n3:
                solutions.append(assignment.copy())
            return

        letter = letters[index]

        for digit in range(10):
            attempts += 1

            if digit in used_digits:
                continue

            if digit == 0 and (letter == first[0] or letter == second[0] or letter == result[0]):
                continue

            assignment[letter] = digit
            used_digits.add(digit)

            if is_valid_partial():
                backtrack(index + 1)

            used_digits.remove(digit)
            del assignment[letter]

    backtrack(0)

    if solutions:
        return solutions, attempts
    return None, attempts

# ---------- PDF ----------
def generate_pdf(first, second, result, solutions):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Cryptarithmetic Solution", ln=True, align='C')
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"{first} + {second} = {result}", ln=True)

    for i, sol in enumerate(solutions, 1):
        pdf.ln(5)
        pdf.cell(200, 10, txt=f"Solution {i}:", ln=True)

        for k, v in sol.items():
            pdf.cell(200, 8, txt=f"{k} = {v}", ln=True)

        n1 = int("".join(str(sol[c]) for c in first))
        n2 = int("".join(str(sol[c]) for c in second))
        n3 = int("".join(str(sol[c]) for c in result))

        pdf.cell(200, 8, txt=f"{n1} + {n2} = {n3}", ln=True)

    return pdf.output(dest="S").encode("latin-1")

# ---------- Solve Button ----------
if st.button("🚀 Solve Puzzle"):

    if first and second and result:

        with st.spinner("Solving..."):
            result_data = solve_csp(first, second, result)

        if isinstance(result_data, tuple) and len(result_data) == 3:
            st.error(result_data[1])
            st.session_state.solutions = None

        elif result_data[0]:
            st.session_state.solutions = result_data[0]
            st.session_state.attempts = result_data[1]

        else:
            st.session_state.solutions = None
            st.session_state.attempts = result_data[1]

    else:
        st.warning("⚠️ Fill all fields")

# ---------- Output ----------
if st.session_state.solutions:

    solutions = st.session_state.solutions
    attempts = st.session_state.attempts

    total = len(solutions)
    limit = 10

    if total > limit:
        st.success(f"✅ {total} Solutions Found (Showing top {limit})")
        show_all = st.checkbox("Show all solutions")
    else:
        st.success(f"✅ {total} Solution(s) Found")
        show_all = True

    display = solutions if show_all else solutions[:limit]

    for idx, mapping in enumerate(display, 1):

        seen = set()
        ordered = {}
        for c in first + second + result:
            if c not in seen:
                ordered[c] = mapping[c]
                seen.add(c)

        n1 = int("".join(str(mapping[c]) for c in first))
        n2 = int("".join(str(mapping[c]) for c in second))
        n3 = int("".join(str(mapping[c]) for c in result))

        st.markdown(f"### 🔢 Solution {idx}")
        st.write(ordered)

        st.markdown("### 📐 Equation")
        st.write(f"{n1} + {n2} = {n3}")

    st.caption(f"Computed in {attempts} attempts")

    pdf_data = generate_pdf(first, second, result, display)

    st.download_button(
        label="📄 Download PDF",
        data=pdf_data,
        file_name="solution.pdf",
        mime="application/pdf"
    )

elif st.session_state.solutions is None and st.session_state.attempts > 0:
    st.error("❌ No solution found")
    st.caption(f"Tried {st.session_state.attempts} assignments")