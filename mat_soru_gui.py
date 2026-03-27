"""
Matematik Soru Hazırlayıcı - Tkinter GUI
TYT/AYT seviyesinde matematik soruları üretip PDF olarak kaydetme aracı.
"""
from __future__ import annotations

import random
import math
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Any, Callable, Dict, List, Tuple, Union

try:
    from fpdf import FPDF  # type: ignore[import]
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "fpdf2"])
    from fpdf import FPDF  # type: ignore[import]


# ═══════════════════════════════════════════════
#  SORU ÜRETİCİ FONKSİYONLAR (Konu Bazlı)
# ═══════════════════════════════════════════════

def _fmt(text: str) -> str:
    """Türkçe karakter temizleme ve görsel düzeltmeler."""
    text = text.replace("+ (-", "- (").replace("+ -", "- ").replace("- -", "+ ")
    tr_map = {
        'ı': 'i', 'ğ': 'g', 'ü': 'u', 'ş': 's', 'ö': 'o', 'ç': 'c',
        'İ': 'I', 'Ğ': 'G', 'Ü': 'U', 'Ş': 'S', 'Ö': 'O', 'Ç': 'C'
    }
    for tr_c, en_c in tr_map.items():
        text = text.replace(tr_c, en_c)
    return text


# ── Temel İşlemler ──────────────────────────────
def _temel_islemler(q_num: int) -> Tuple[str, int, str]:
    typ = random.randint(1, 4)
    if typ == 1:
        a, b = random.randint(10, 999), random.randint(10, 999)
        ans = a + b
        q = f"{q_num}) {a} + {b} isleminin sonucu kactir?"
        sol = f"{a} + {b} = {ans}"
        return q, ans, sol
    elif typ == 2:
        a = random.randint(50, 999)
        b = random.randint(10, a)
        ans = a - b
        q = f"{q_num}) {a} - {b} isleminin sonucu kactir?"
        sol = f"{a} - {b} = {ans}"
        return q, ans, sol
    elif typ == 3:
        a, b = random.randint(2, 30), random.randint(2, 30)
        ans = a * b
        q = f"{q_num}) {a} x {b} isleminin sonucu kactir?"
        sol = f"{a} x {b} = {ans}"
        return q, ans, sol
    else:
        b = random.randint(2, 12)
        ans = random.randint(2, 50)
        a = b * ans
        q = f"{q_num}) {a} / {b} isleminin sonucu kactir?"
        sol = f"{a} / {b} = {ans}"
        return q, ans, sol


# ── Sayılar ─────────────────────────────────────
def _sayilar(q_num: int) -> Tuple[str, int, str]:
    typ = random.randint(1, 3)
    if typ == 1:
        x = random.randint(10, 50)
        y = random.randint(1, x - 1)
        a, b = x + y, x - y
        q = f"{q_num}) Toplamlari {a} ve farklari {b} olan iki sayidan buyuk olani kactir?"
        sol = f"x + y = {a}\nx - y = {b}\nToplarsak: 2x = {a + b}\nx = {(a + b) // 2} (Buyuk sayi)"
        return q, x, sol
    elif typ == 2:
        n = random.choice([3, 5, 7])
        x = random.randint(10, 40)
        s = sum(range(x, x + n))
        term_sum = sum(range(n))
        q = f"{q_num}) Ardisik {n} tam sayinin toplami {s} olduguna gore, en kucuk sayi kactir?"
        sol = f"Sayilar: x, x+1, ..., x+{n - 1}\nToplam = {n}x + {term_sum} = {s}\n{n}x = {s - term_sum}\nx = {x}"
        return q, x, sol
    else:
        a = random.randint(2, 8)
        x = random.randint(-10, 20)
        b = random.randint(-15, 20)
        c = a * x + b
        fazla = f"{b} fazlasi" if b >= 0 else f"{abs(b)} eksigi"
        op = "+" if b >= 0 else "-"
        q = f"{q_num}) Hangi sayinin {a} katinin {fazla} {c} olur?"
        sol = f"Sayi x olsun.\n{a}x {op} {abs(b)} = {c}\n{a}x = {c} - ({b})\n{a}x = {c - b}\nx = {x}"
        return q, x, sol


# ── 1. Derece Denklemler ────────────────────────
def _birinci_derece(q_num: int) -> Tuple[str, int, str]:
    typ = random.randint(1, 5)
    if typ == 1:
        a = random.randint(2, 10)
        x = random.randint(-10, 15)
        b = random.randint(-20, 20)
        c = a * x + b
        q = f"{q_num}) {a}x + ({b}) = {c} denkleminde x kactir?"
        sol = f"{a}x + ({b}) = {c}\n{a}x = {c} - ({b})\n{a}x = {c - b}\nx = {x}"
        return q, x, sol
    elif typ == 2:
        a = random.randint(1, 10)
        c_val = random.randint(1, 10)
        while a == c_val:
            c_val = random.randint(1, 10)
        x = random.randint(-15, 15)
        b = random.randint(-20, 20)
        d = a * x + b - c_val * x
        q = f"{q_num}) {a}x + ({b}) = {c_val}x + ({d}) esitligini saglayan x degeri kactir?"
        sol = f"{a}x + ({b}) = {c_val}x + ({d})\n{a - c_val}x = {d - b}\nx = {x}"
        return q, x, sol
    elif typ == 3:
        a = random.randint(2, 6)
        c_val = random.randint(2, 6)
        b = random.randint(-5, 10)
        d = random.randint(-10, 5)
        x = random.randint(-10, 10)
        e = a * (x - b) + c_val * (x - d)
        q = f"{q_num}) {a}(x - {b}) + {c_val}(x - {d}) = {e} denklemini saglayan x kactir?"
        sol = f"{a}x - {a * b} + {c_val}x - {c_val * d} = {e}\n{a + c_val}x - {a * b + c_val * d} = {e}\n{a + c_val}x = {e + a * b + c_val * d}\nx = {x}"
        return q, x, sol
    elif typ == 4:
        b = random.choice([2, 3, 4, 5])
        c = random.randint(-5, 15)
        a = random.randint(-10, 10)
        x = b * c - a
        q = f"{q_num}) (x + {a}) / {b} = {c} denkleminde x kactir?"
        sol = f"x + {a} = {b} * {c}\nx + {a} = {b * c}\nx = {b * c} - {a}\nx = {x}"
        return q, x, sol
    else:
        a = random.choice([2, 3, 4])
        b = random.choice([3, 4, 5, 6])
        while a == b:
            b = random.choice([3, 4, 5, 6])
        x = (a * b) * random.randint(1, 5)
        c = int(x / a + x / b)
        q = f"{q_num}) (x/{a}) + (x/{b}) = {c} denklemini saglayan x degeri kactir?"
        sol = f"({b}x + {a}x) / {a * b} = {c}\n{a + b}x / {a * b} = {c}\n{a + b}x = {c * a * b}\nx = {x}"
        return q, x, sol


# ── 2. Derece Denklemler ────────────────────────
def _ikinci_derece(q_num: int) -> Tuple[str, int, str]:
    typ = random.randint(1, 4)
    if typ == 1:
        x1 = random.randint(-8, 8)
        x2 = random.randint(-8, 8)
        a = 1
        b = -(x1 + x2)
        c = x1 * x2
        q = f"{q_num}) x^2 + ({b})x + ({c}) = 0 denkleminin koklerinin toplami kactir?"
        ans = x1 + x2
        sol = f"x^2 + ({b})x + ({c}) = 0\nKoklerin toplami = -b/a = {-b}/{a} = {ans}"
        return q, ans, sol
    elif typ == 2:
        x1 = random.randint(-8, 8)
        x2 = random.randint(-8, 8)
        a = 1
        b = -(x1 + x2)
        c = x1 * x2
        q = f"{q_num}) x^2 + ({b})x + ({c}) = 0 denkleminin koklerinin carpimi kactir?"
        ans = x1 * x2
        sol = f"x^2 + ({b})x + ({c}) = 0\nKoklerin carpimi = c/a = {c}/{a} = {ans}"
        return q, ans, sol
    elif typ == 3:
        x1 = random.randint(1, 10)
        x2 = random.randint(1, 10)
        while x1 == x2:
            x2 = random.randint(1, 10)
        b = -(x1 + x2)
        c = x1 * x2
        delta = b * b - 4 * c
        q = f"{q_num}) x^2 + ({b})x + {c} = 0 denkleminin diskriminanti (delta) kactir?"
        ans = delta
        sol = f"delta = b^2 - 4ac = ({b})^2 - 4*1*{c} = {b * b} - {4 * c} = {delta}"
        return q, ans, sol
    else:
        x1 = random.randint(-6, 6)
        x2 = random.randint(-6, 6)
        a_coef = random.choice([2, 3])
        b_coef = -a_coef * (x1 + x2)
        c_coef = a_coef * x1 * x2
        ans = x1 + x2
        q = f"{q_num}) {a_coef}x^2 + ({b_coef})x + ({c_coef}) = 0 denkleminin koklerinin toplami kactir?"
        sol = f"Koklerin toplami = -b/a = {-b_coef}/{a_coef} = {ans}"
        return q, ans, sol


# ── Fonksiyonlar ────────────────────────────────
def _fonksiyonlar(q_num: int) -> Tuple[str, Any, str]:
    typ = random.randint(1, 5)
    if typ == 1:
        a = random.randint(1, 5)
        b = random.randint(-10, 10)
        val = random.randint(-5, 10)
        ans = a * val + b
        q = f"{q_num}) f(x) = {a}x + ({b}) ise f({val}) kactir?"
        sol = f"f({val}) = {a}*{val} + ({b}) = {a * val} + ({b}) = {ans}"
        return q, ans, sol
    elif typ == 2:
        a = random.randint(1, 3)
        b = random.randint(-5, 5)
        c = random.randint(1, 3)
        d = random.randint(-5, 5)
        val = random.randint(-3, 5)
        g_val = c * val + d
        ans = a * g_val + b
        q = f"{q_num}) f(x)={a}x+({b}), g(x)={c}x+({d}) ise (fog)({val}) kactir?"
        sol = f"g({val}) = {c}*{val}+({d}) = {g_val}\nf(g({val})) = f({g_val}) = {a}*{g_val}+({b}) = {ans}"
        return q, ans, sol
    elif typ == 3:
        a = random.randint(1, 3)
        b = random.randint(-5, 5)
        c = random.randint(1, 3)
        d = random.randint(-5, 5)
        val = random.randint(-3, 5)
        f_val = a * val + b
        ans = c * f_val + d
        q = f"{q_num}) f(x)={a}x+({b}), g(x)={c}x+({d}) ise (gof)({val}) kactir?"
        sol = f"f({val}) = {a}*{val}+({b}) = {f_val}\ng(f({val})) = g({f_val}) = {c}*{f_val}+({d}) = {ans}"
        return q, ans, sol
    elif typ == 4:
        a = random.randint(1, 5)
        b = random.randint(-10, 10)
        while a == 0:
            a = random.randint(1, 5)
        q = f"{q_num}) f(x) = {a}x + ({b}) fonksiyonunun tersi f^(-1)(x) nedir? f^(-1)(0) kactir?"
        ans_val = -b / a
        if ans_val == int(ans_val):
            ans_val = int(ans_val)
        ans = ans_val
        sol = f"y = {a}x + ({b})\nx = (y - ({b}))/{a}\nf^(-1)(x) = (x - ({b}))/{a}\nf^(-1)(0) = (0 - ({b}))/{a} = {ans}"
        return q, ans, sol
    else:
        a = random.randint(1, 4)
        b = random.randint(-8, 8)
        ans_x = random.randint(-5, 10)
        target = a * ans_x + b
        q = f"{q_num}) f(x) = {a}x + ({b}) ise f(x) = {target} denklemini saglayan x kactir?"
        sol = f"{a}x + ({b}) = {target}\n{a}x = {target} - ({b})\n{a}x = {target - b}\nx = {ans_x}"
        return q, ans_x, sol


# ── Mutlak Değer ────────────────────────────────
def _mutlak_deger(q_num: int) -> Tuple[str, Any, str]:
    typ = random.randint(1, 3)
    if typ == 1:
        a = random.randint(1, 5)
        b = random.randint(-10, 10)
        c = random.randint(1, 20)
        x1 = (c - b) / a
        x2 = (-c - b) / a
        if x1 == int(x1):
            x1 = int(x1)
        if x2 == int(x2):
            x2 = int(x2)
        ans = 2
        q = f"{q_num}) |{a}x + ({b})| = {c} denkleminin kac cozumu vardir?"
        sol = f"|{a}x + ({b})| = {c}\n{a}x + ({b}) = {c} => x = {x1}\n{a}x + ({b}) = -{c} => x = {x2}\n2 cozum vardir."
        return q, ans, sol
    elif typ == 2:
        a = random.randint(1, 5)
        b = random.randint(-10, 10)
        c = random.randint(1, 20)
        x1 = (c - b) / a
        x2 = (-c - b) / a
        if x1 == int(x1):
            x1 = int(x1)
        if x2 == int(x2):
            x2 = int(x2)
        total = x1 + x2
        if isinstance(x1, int) and isinstance(x2, int):
            ans: Any = int(total)
        else:
            ans = round(float(total), 2)
        q = f"{q_num}) |{a}x + ({b})| = {c} => koklerin toplami kactir?"
        sol = f"x1 = {x1}, x2 = {x2}\nToplam = {x1} + {x2} = {ans}"
        return q, ans, sol
    else:
        val = random.randint(-20, 20)
        ans = abs(val)
        q = f"{q_num}) |{val}| ifadesinin degeri kactir?"
        sol = f"|{val}| = {ans}"
        return q, ans, sol


# ── Üslü İfadeler ──────────────────────────────
def _uslu_ifadeler(q_num: int) -> Tuple[str, int, str]:
    typ = random.randint(1, 4)
    if typ == 1:
        base = random.randint(2, 5)
        exp = random.randint(2, 6)
        ans = base ** exp
        q = f"{q_num}) {base}^{exp} kactir?"
        sol = f"{base}^{exp} = {ans}"
        return q, ans, sol
    elif typ == 2:
        base = random.randint(2, 5)
        e1 = random.randint(2, 5)
        e2 = random.randint(1, 3)
        ans = e1 + e2
        q = f"{q_num}) {base}^{e1} * {base}^{e2} ifadesini {base}^n seklinde yazarsak n kactir?"
        sol = f"{base}^{e1} * {base}^{e2} = {base}^({e1}+{e2}) = {base}^{ans}\nn = {ans}"
        return q, ans, sol
    elif typ == 3:
        base = random.randint(2, 5)
        e1 = random.randint(4, 8)
        e2 = random.randint(1, 3)
        ans = e1 - e2
        q = f"{q_num}) {base}^{e1} / {base}^{e2} ifadesini {base}^n seklinde yazarsak n kactir?"
        sol = f"{base}^{e1} / {base}^{e2} = {base}^({e1}-{e2}) = {base}^{ans}\nn = {ans}"
        return q, ans, sol
    else:
        base = random.randint(2, 4)
        e1 = random.randint(2, 4)
        e2 = random.randint(2, 3)
        ans = e1 * e2
        q = f"{q_num}) ({base}^{e1})^{e2} ifadesini {base}^n seklinde yazarsak n kactir?"
        sol = f"({base}^{e1})^{e2} = {base}^({e1}*{e2}) = {base}^{ans}\nn = {ans}"
        return q, ans, sol


# ── Köklü İfadeler ──────────────────────────────
def _koklu_ifadeler(q_num: int) -> Tuple[str, int, str]:
    typ = random.randint(1, 4)
    if typ == 1:
        val = random.randint(1, 15)
        sq = val * val
        q = f"{q_num}) sqrt({sq}) kactir?"
        sol = f"sqrt({sq}) = {val}"
        return q, val, sol
    elif typ == 2:
        a = random.randint(2, 6)
        b = random.randint(2, 6)
        sq = a * a * b
        q = f"{q_num}) sqrt({sq}) ifadesini sadelesiniz. (a*sqrt(b) seklinde, a kactir?)"
        sol = f"sqrt({sq}) = sqrt({a * a}*{b}) = {a}*sqrt({b})\na = {a}"
        return q, a, sol
    elif typ == 3:
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        ans = a + b
        a_sq = a * a
        b_sq = b * b
        q = f"{q_num}) sqrt({a_sq}) + sqrt({b_sq}) kactir?"
        sol = f"sqrt({a_sq}) + sqrt({b_sq}) = {a} + {b} = {ans}"
        return q, ans, sol
    else:
        a = random.randint(2, 8)
        b = random.randint(2, 8)
        ans = a * b
        q = f"{q_num}) sqrt({a * a}) * sqrt({b * b}) kactir?"
        sol = f"sqrt({a * a}) * sqrt({b * b}) = {a} * {b} = {ans}"
        return q, ans, sol


# ═══════════════════════════════════════════════
#  KONU HARİTASI
# ═══════════════════════════════════════════════

TOPICS: Dict[str, Callable[[int], Tuple[str, Any, str]]] = {
    "Temel Islemler":        _temel_islemler,
    "Sayilar":               _sayilar,
    "1. Derece Denklemler":  _birinci_derece,
    "2. Derece Denklemler":  _ikinci_derece,
    "Fonksiyonlar":          _fonksiyonlar,
    "Mutlak Deger":          _mutlak_deger,
    "Uslu Ifadeler":         _uslu_ifadeler,
    "Koklu Ifadeler":        _koklu_ifadeler,
}


# ═══════════════════════════════════════════════
#  PDF SINIFI
# ═══════════════════════════════════════════════

class MathPDF(FPDF):  # type: ignore[misc]
    def __init__(self, title: str = "Matematik Soru Bankasi") -> None:
        super().__init__()
        self._title = title
        try:
            self.add_font("Arial", "", "C:\\Windows\\Fonts\\arial.ttf")
            self.add_font("Arial", "B", "C:\\Windows\\Fonts\\arialbd.ttf")
            self.add_font("Arial", "I", "C:\\Windows\\Fonts\\ariali.ttf")
            self._font_name = "Arial"
        except Exception:
            self._font_name = "Helvetica"

    def header(self):
        self.set_font(self._font_name, 'B', 14)
        self.cell(0, 10, _fmt(self._title), border=0, new_x='LMARGIN', new_y='NEXT', align='C')
        self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font(self._font_name, 'I', 8)
        self.cell(0, 10, f'Sayfa {self.page_no()}', border=0, new_x='RIGHT', new_y='TOP', align='C')


# ═══════════════════════════════════════════════
#  PDF ÜRETME
# ═══════════════════════════════════════════════

def generate_questions(selected_topics: List[str], count: int) -> Tuple[List[str], List[Any], List[str]]:
    """Seçili konulardan belirtilen sayıda soru üret."""
    funcs: List[Callable[[int], Tuple[str, Any, str]]] = [TOPICS[t] for t in selected_topics if t in TOPICS]
    if not funcs:
        return [], [], []

    questions, answers, solutions = [], [], []
    for i in range(1, count + 1):
        fn = random.choice(funcs)
        q, ans, sol = fn(i)
        questions.append(_fmt(q))
        answers.append(ans)
        solutions.append(_fmt(sol))
    return questions, answers, solutions


def build_pdf(questions: List[str], answers: List[Any], solutions: List[str], filepath: str, include_solutions: bool = False) -> None:
    """PDF oluştur ve kaydet."""
    title = "Matematik Soru Bankasi" + (" (Cozumlu)" if include_solutions else "")
    pdf = MathPDF(title)
    pdf.add_page()
    pdf.set_font(pdf._font_name, size=10)

    col_width = 90
    row_height = 35 if not include_solutions else 50
    y_start = pdf.get_y()

    for i in range(0, len(questions), 2):
        if y_start + row_height > 275:
            pdf.add_page()
            y_start = pdf.get_y()

        # Sol sütun
        pdf.set_xy(10, y_start)
        pdf.multi_cell(w=col_width, h=5, text=questions[i])
        if include_solutions:
            pdf.set_xy(10, pdf.get_y() + 1)
            pdf.set_text_color(80, 80, 80)
            pdf.multi_cell(w=col_width, h=5, text=solutions[i])
            pdf.set_text_color(0, 0, 0)

        # Sağ sütun
        if i + 1 < len(questions):
            pdf.set_xy(10 + col_width + 10, y_start)
            pdf.multi_cell(w=col_width, h=5, text=questions[i + 1])
            if include_solutions:
                pdf.set_xy(10 + col_width + 10, pdf.get_y() + 1)
                pdf.set_text_color(80, 80, 80)
                pdf.multi_cell(w=col_width, h=5, text=solutions[i + 1])
                pdf.set_text_color(0, 0, 0)

        y_start += row_height

    # Cevap Anahtarı
    pdf.add_page()
    pdf.set_auto_page_break(auto=False)
    pdf.set_font(pdf._font_name, "B", 14)
    pdf.cell(0, 10, 'CEVAP ANAHTARI', border=0, new_x='LMARGIN', new_y='NEXT', align='C')
    pdf.ln(5)
    pdf.set_font(pdf._font_name, size=8)

    col_ans_w = 18
    ans_y = pdf.get_y()
    for idx, ans in enumerate(answers):
        col = idx % 10
        row = (idx % 400) // 10
        if idx > 0 and idx % 400 == 0:
            pdf.add_page()
            ans_y = pdf.get_y()
        pdf.set_xy(10 + col * col_ans_w, ans_y + row * 6)
        pdf.cell(col_ans_w, 6, f"{idx + 1}) {ans}", border=0)

    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.output(filepath)


# ═══════════════════════════════════════════════
#  TKINTER GUI
# ═══════════════════════════════════════════════

class MatSoruApp:
    BG = "#1a1a2e"
    BG2 = "#16213e"
    ACCENT = "#0f3460"
    ACCENT2 = "#533483"
    HIGHLIGHT = "#e94560"
    TEXT = "#eaeaea"
    TEXT2 = "#a0a0b0"
    SUCCESS = "#2ecc71"

    def __init__(self, root: tk.Tk) -> None:
        self.root: tk.Tk = root
        self.root.title("Matematik Soru Hazırlayıcı")
        self.root.geometry("620x700")
        self.root.resizable(False, False)
        self.root.configure(bg=self.BG)

        # Pre-declare instance attributes for type checker
        self.topic_vars: Dict[str, tk.BooleanVar] = {}
        self.count_var: tk.IntVar = tk.IntVar(value=100)
        self.count_entry: ttk.Entry = ttk.Entry(self.root)
        self.solutions_var: tk.BooleanVar = tk.BooleanVar(value=True)
        self.gen_btn: ttk.Button = ttk.Button(self.root)
        self.status_var: tk.StringVar = tk.StringVar(value="Hazir.")

        # Ana stil
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=self.BG)
        style.configure("TLabel", background=self.BG, foreground=self.TEXT, font=("Segoe UI", 10))
        style.configure("Title.TLabel", background=self.BG, foreground=self.HIGHLIGHT,
                         font=("Segoe UI", 18, "bold"))
        style.configure("Sub.TLabel", background=self.BG, foreground=self.TEXT2, font=("Segoe UI", 9))
        style.configure("TCheckbutton", background=self.BG2, foreground=self.TEXT,
                         font=("Segoe UI", 11), indicatormargin=8)
        style.map("TCheckbutton",
                  background=[("active", self.ACCENT)],
                  foreground=[("active", self.TEXT)])
        style.configure("Accent.TButton", background=self.HIGHLIGHT, foreground="white",
                         font=("Segoe UI", 12, "bold"), padding=(20, 10))
        style.map("Accent.TButton",
                  background=[("active", "#c0392b"), ("disabled", "#555")])
        style.configure("Small.TButton", background=self.ACCENT, foreground=self.TEXT,
                         font=("Segoe UI", 9), padding=(8, 4))
        style.map("Small.TButton", background=[("active", self.ACCENT2)])
        style.configure("TLabelframe", background=self.BG2, foreground=self.HIGHLIGHT,
                         font=("Segoe UI", 11, "bold"))
        style.configure("TLabelframe.Label", background=self.BG2, foreground=self.HIGHLIGHT,
                         font=("Segoe UI", 11, "bold"))
        style.configure("Status.TLabel", background=self.BG, foreground=self.SUCCESS,
                         font=("Segoe UI", 10))

        self._build_ui()

    def _build_ui(self) -> None:
        # Başlık
        ttk.Label(self.root, text="📐 Matematik Soru Hazırlayıcı", style="Title.TLabel").pack(pady=(18, 2))
        ttk.Label(self.root, text="Konu sec, soru sayisini ayarla, PDF olustur!", style="Sub.TLabel").pack(pady=(0, 12))

        # ── Konu Seçimi Frame ─────────────────
        topic_frame = ttk.LabelFrame(self.root, text="  📋 Konu Secimi  ", padding=14)
        topic_frame.pack(fill="x", padx=24, pady=(0, 10))

        self.topic_vars.clear()
        cols = 2
        for idx, topic_name in enumerate(TOPICS):
            var = tk.BooleanVar(value=True)
            self.topic_vars[topic_name] = var
            cb = ttk.Checkbutton(topic_frame, text=topic_name, variable=var)
            cb.grid(row=idx // cols, column=idx % cols, sticky="w", padx=12, pady=5)

        # Tümünü Seç / Temizle butonları
        btn_frame = ttk.Frame(topic_frame)
        btn_frame.grid(row=(len(TOPICS) // cols) + 1, column=0, columnspan=cols, pady=(8, 0))
        ttk.Button(btn_frame, text="✅ Tumunu Sec", style="Small.TButton",
                   command=self._select_all).pack(side="left", padx=6)
        ttk.Button(btn_frame, text="❌ Temizle", style="Small.TButton",
                   command=self._deselect_all).pack(side="left", padx=6)

        # ── Soru Sayısı Frame ─────────────────
        count_frame = ttk.LabelFrame(self.root, text="  🔢 Soru Sayisi  ", padding=14)
        count_frame.pack(fill="x", padx=24, pady=(0, 10))

        inner = ttk.Frame(count_frame)
        inner.pack()

        self.count_var.set(100)

        ttk.Button(inner, text="−10", style="Small.TButton",
                   command=lambda: self._adjust(-10)).pack(side="left", padx=4)
        ttk.Button(inner, text=" − ", style="Small.TButton",
                   command=lambda: self._adjust(-1)).pack(side="left", padx=4)

        self.count_entry = ttk.Entry(inner, textvariable=self.count_var, width=8,
                                     font=("Segoe UI", 16, "bold"), justify="center")
        self.count_entry.pack(side="left", padx=10)

        ttk.Button(inner, text=" + ", style="Small.TButton",
                   command=lambda: self._adjust(1)).pack(side="left", padx=4)
        ttk.Button(inner, text="+10", style="Small.TButton",
                   command=lambda: self._adjust(10)).pack(side="left", padx=4)
        ttk.Button(inner, text="+100", style="Small.TButton",
                   command=lambda: self._adjust(100)).pack(side="left", padx=4)

        ttk.Label(count_frame, text="(10 - 2000 arasi deger girebilirsiniz)",
                  style="Sub.TLabel").pack(pady=(6, 0))

        # ── Çözüm seçeneği ─────────────────
        opt_frame = ttk.LabelFrame(self.root, text="  ⚙️ Secenekler  ", padding=14)
        opt_frame.pack(fill="x", padx=24, pady=(0, 10))

        self.solutions_var.set(True)
        ttk.Checkbutton(opt_frame, text="Cozumlu PDF de olustur",
                        variable=self.solutions_var).pack(anchor="w")

        # ── Üret Butonu ───────────────────────
        self.gen_btn = ttk.Button(self.root, text="🚀  PDF Olustur", style="Accent.TButton",
                                  command=self._generate)
        self.gen_btn.pack(pady=16)

        # ── Durum Çubuğu ─────────────────────
        self.status_var.set("Hazir.")
        ttk.Label(self.root, textvariable=self.status_var, style="Status.TLabel").pack(pady=(0, 10))

    # ── Yardımcı Fonksiyonlar ─────────────────
    def _select_all(self) -> None:
        for v in self.topic_vars.values():
            v.set(True)

    def _deselect_all(self) -> None:
        for v in self.topic_vars.values():
            v.set(False)

    def _adjust(self, delta: int) -> None:
        try:
            val = self.count_var.get()
        except tk.TclError:
            val = 100
        val = max(10, min(2000, val + delta))
        self.count_var.set(val)

    def _generate(self) -> None:
        # Seçili konuları al
        selected = [t for t, v in self.topic_vars.items() if v.get()]
        if not selected:
            messagebox.showwarning("Uyari", "Lutfen en az bir konu secin!")
            return

        try:
            count = self.count_var.get()
            if count < 10 or count > 2000:
                raise ValueError
        except (tk.TclError, ValueError):
            messagebox.showwarning("Uyari", "Soru sayisi 10-2000 arasinda olmalidir!")
            return

        # Dosya kaydetme yeri
        save_dir = filedialog.askdirectory(title="PDF kayit klasoru secin")
        if not save_dir:
            return

        self.gen_btn.state(["disabled"])
        self.status_var.set("Sorular uretiliyor...")
        self.root.update_idletasks()

        try:
            questions, answers, solutions = generate_questions(selected, count)

            # Normal PDF
            normal_path = os.path.join(save_dir, f"Matematik_{count}_Soru.pdf")
            build_pdf(questions, answers, solutions, normal_path, include_solutions=False)
            msg = f"'{normal_path}' olusturuldu."

            # Çözümlü PDF
            if self.solutions_var.get():
                solved_path = os.path.join(save_dir, f"Matematik_{count}_Soru_Cozumlu.pdf")
                build_pdf(questions, answers, solutions, solved_path, include_solutions=True)
                msg += f"\n'{solved_path}' olusturuldu."

            self.status_var.set(f"Basariyla {count} soru uretildi! ✅")
            messagebox.showinfo("Basarili", msg)

        except Exception as e:
            self.status_var.set("Hata olustu! ❌")
            messagebox.showerror("Hata", str(e))
        finally:
            self.gen_btn.state(["!disabled"])


# ═══════════════════════════════════════════════
#  ANA GİRİŞ NOKTASI
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    root = tk.Tk()
    app = MatSoruApp(root)
    root.mainloop()
