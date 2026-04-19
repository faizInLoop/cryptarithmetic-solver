# 🔐 Cryptarithmetic Puzzle Solver (AI Project)

A web-based Cryptarithmetic Puzzle Solver built using **Python**, **Streamlit**, and **Constraint Satisfaction Problem (CSP)** techniques.
This project solves puzzles like:

```
SEND
+ MORE
------
MONEY
```

by assigning unique digits to letters such that the equation holds true.

---

## 🚀 Features

* 🧠 **CSP + Backtracking Solver** (optimized)
* 🔍 **Carry-aware constraint checking** (accurate results)
* 🔢 **Multiple solutions support**
* 📊 Displays **total solutions found**
* 🎯 Shows **top 10 solutions** (with option to view all)
* 📄 **Download solutions as PDF**
* 🎨 Clean UI with background styling
* ⚡ Fast and optimized performance
* 🌐 Deployable via Streamlit Cloud

---

## 🧠 How It Works

This problem is modeled as a **Constraint Satisfaction Problem (CSP)**:

* **Variables:** Letters in the puzzle
* **Domain:** Digits (0–9)
* **Constraints:**

  * Each letter maps to a unique digit
  * Leading letters cannot be zero
  * Arithmetic equation must be valid

The solver uses:

* **Backtracking** to explore possible assignments
* **Constraint pruning** to eliminate invalid paths early
* **Column-wise (carry-aware) validation** for correctness

---

## 🖥️ Tech Stack

* **Python**
* **Streamlit**
* **FPDF (PDF generation)**

---

## 📦 Project Structure

```
cryptarithmetic-solver/
│
├── app.py
├── bg.png
├── requirements.txt
└── README.md
```

---

## ▶️ Run Locally

1. Clone the repository:

```bash
git clone https://github.com/your-username/cryptarithmetic-solver.git
cd cryptarithmetic-solver
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
streamlit run app.py
```

---

## 🌐 Deployment

This project is deployed using **Streamlit Cloud**.

👉 Live App: *https://cryptarithmetic-solver.streamlit.app/*

---

## 🧪 Example Input

```
First Word: SEND
Second Word: MORE
Result Word: MONEY
```

### ✅ Output

```
SEND = 9567
MORE = 1085
MONEY = 10652
```

---

## ⚠️ Limitations

* Maximum **10 unique letters** (digits 0–9)
* Performance depends on puzzle complexity
* No advanced heuristics (MRV, forward checking) implemented

---

## 🔮 Future Improvements

* Add CSP heuristics (MRV, LCV)
* Visualize solving steps
* Support more operations (multiplication, division)
* Improve UI/UX with animations
* Performance optimization

---

## 🧠 AI Concepts Used

* Constraint Satisfaction Problem (CSP)
* Backtracking Algorithm
* Constraint Propagation
* Search Optimization

---

## 🙌 Author

**Faiz Hassan**

---

## ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub!

---
