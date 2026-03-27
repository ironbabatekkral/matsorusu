import random
import os
try:
    from fpdf import FPDF
except ImportError:
    print("fpdf not found. Please install it with 'pip install fpdf2'")
    exit(1)

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'TYT Matematik: Sayilar ve Denklemler', border=0, new_x='LMARGIN', new_y='NEXT', align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Sayfa {self.page_no()}', border=0, new_x='RIGHT', new_y='TOP', align='C')

def generate_question(q_num):
    q_type = random.randint(1, 8)
    
    if q_type == 1:
        # ax + b = c
        a = random.randint(2, 10)
        x = random.randint(-10, 15)
        b = random.randint(-20, 20)
        c = a * x + b
        
        q = f"{q_num}) {a}x + ({b}) = {c} denkleminde x kactir?"
        sol = f"{a}x + ({b}) = {c}\n{a}x = {c} - ({b})\n{a}x = {c-b}\nx = {x}"
        return q, x, sol
        
    elif q_type == 2:
        # ax + b = cx + d
        a = random.randint(1, 10)
        c_val = random.randint(1, 10)
        while a == c_val:
            c_val = random.randint(1, 10)
        x = random.randint(-15, 15)
        b = random.randint(-20, 20)
        d = a * x + b - c_val * x
        
        q = f"{q_num}) {a}x + ({b}) = {c_val}x + ({d}) esitligini saglayan x degeri kactir?"
        sol = f"{a}x + ({b}) = {c_val}x + ({d})\n{a}x - {c_val}x = {d} - ({b})\n{a-c_val}x = {d-b}\nx = {x}"
        return q, x, sol
        
    elif q_type == 3:
        # "Hangi sayinin a katinin b fazlasi c'dir?"
        a = random.randint(2, 8)
        x = random.randint(-10, 20)
        b = random.randint(-15, 20)
        c = a * x + b
        fazla_eksik = f"{b} fazlasi" if b >= 0 else f"{abs(b)} eksigi"
        
        q = f"{q_num}) Hangi sayinin {a} katinin {fazla_eksik} {c} olur?"
        op = "+" if b >= 0 else "-"
        abs_b = abs(b)
        sol = f"Sayi x olsun.\n{a}x {op} {abs_b} = {c}\n{a}x = {c} - ({b})\n{a}x = {c-b}\nx = {x}"
        return q, x, sol
        
    elif q_type == 4:
        # "a(x - b) + c(x - d) = e"
        a = random.randint(2, 6)
        c_val = random.randint(2, 6)
        b = random.randint(-5, 10)
        d = random.randint(-10, 5)
        x = random.randint(-10, 10)
        e = a * (x - b) + c_val * (x - d)
        
        q = f"{q_num}) {a}(x - {b}) + {c_val}(x - {d}) = {e} denklemini saglayan x kactir?"
        sol = f"{a}x - {a*b} + {c_val}x - {c_val*d} = {e}\n{a+c_val}x - {a*b + c_val*d} = {e}\n{a+c_val}x = {e} + {a*b + c_val*d}\n{a+c_val}x = {e + a*b + c_val*d}\nx = {x}"
        return q, x, sol
        
    elif q_type == 5:
        # "Toplamlari a ve farklari b olan iki sayidan buyuk olani kactir?"
        x = random.randint(10, 50)
        y = random.randint(1, x-1)
        a = x + y
        b = x - y
        
        q = f"{q_num}) Toplamlari {a} ve farklari {b} olan iki sayidan buyuk olani kactir?"
        sol = f"x + y = {a}\nx - y = {b}\nToplarsak: 2x = {a+b}\nx = {(a+b)//2} (Buyuk sayi)"
        return q, x, sol
        
    elif q_type == 6:
        # "Ardisik a tam sayinin toplami b ise en kucuk sayi kactir?"
        a = random.choice([3, 5, 7])
        x = random.randint(10, 40)
        b = sum(range(x, x+a))
        
        q = f"{q_num}) Ardisik {a} tam sayinin toplami {b} olduguna gore, en kucuk sayi kactir?"
        
        # Build explanation
        term_sum = sum(range(a))
        sol = f"Sayilar: x, x+1, ..., x+{a-1}\nToplam = {a}x + {term_sum} = {b}\n{a}x = {b - term_sum}\nx = {x}"
        return q, x, sol
        
    elif q_type == 7:
        # (x+a)/b = c
        b = random.choice([2, 3, 4, 5])
        c = random.randint(-5, 15)
        x_plus_a = b * c
        a = random.randint(-10, 10)
        x = x_plus_a - a
        
        q = f"{q_num}) (x + {a}) / {b} = {c} denkleminde x kactir?"
        sol = f"x + {a} = {b} * {c}\nx + {a} = {b*c}\nx = {b*c} - {a}\nx = {x}"
        return q, x, sol
        
    elif q_type == 8:
        # x/a + x/b = c
        a = random.choice([2, 3, 4])
        b = random.choice([3, 4, 5, 6])
        while a == b:
            b = random.choice([3, 4, 5, 6])
        LCM = a * b
        x_base = LCM
        x = x_base * random.randint(1, 5)
        c = int(x/a + x/b)
        
        q = f"{q_num}) (x/{a}) + (x/{b}) = {c} denklemini saglayan x degeri kactir?"
        sol = f"Payda esitlersek ({b} ile {a}):\n({b}x + {a}x) / {a*b} = {c}\n{a+b}x / {a*b} = {c}\n{a+b}x = {c * a * b}\nx = {x}"
        return q, x, sol

def generate_pdfs():
    pdf_normal = PDF()
    pdf_solved = PDF()
    
    # Fonts
    for pdf in (pdf_normal, pdf_solved):
        try:
            pdf.add_font("Arial", "", "C:\\Windows\\Fonts\\arial.ttf")
            pdf.add_font("Arial", "B", "C:\\Windows\\Fonts\\arialbd.ttf")
            pdf.add_font("Arial", "I", "C:\\Windows\\Fonts\\ariali.ttf")
        except Exception:
            pass
            
        pdf.add_page()
        try:
            pdf.set_font("Arial", size=10)
        except:
            pdf.set_font("Helvetica", size=10)
            
    questions = []
    answers = []
    solutions = []
    
    for i in range(1, 801):
        q, ans, sol = generate_question(i)
        
        # Clean up text
        q = q.replace("+ (-", "- (").replace("+ -", "- ")
        sol = sol.replace("+ (-", "- (").replace("+ -", "- ")
        
        tr_map = {'ı':'i', 'ğ':'g', 'ü':'u', 'ş':'s', 'ö':'o', 'ç':'c', 'İ':'I', 'Ğ':'G', 'Ü':'U', 'Ş':'S', 'Ö':'O', 'Ç':'C'}
        for tr_char, en_char in tr_map.items():
            q = q.replace(tr_char, en_char)
            sol = sol.replace(tr_char, en_char)
            
        questions.append(q)
        answers.append(ans)
        solutions.append(sol)
        
    def build_pdf_content(pdf, include_solutions):
        col_width = 90
        row_height = 35 if not include_solutions else 45
        y_start = pdf.get_y()
        
        for i in range(0, len(questions), 2):
            # Check if we need a new page before drawing the row
            if y_start + row_height > 275:
                pdf.add_page()
                y_start = pdf.get_y()
                
            # Left column
            pdf.set_xy(10, y_start)
            pdf.multi_cell(w=col_width, h=5, text=questions[i])
            if include_solutions:
                pdf.set_xy(10, pdf.get_y() + 2)
                pdf.set_text_color(100, 100, 100) # Gray color for solutions
                pdf.multi_cell(w=col_width, h=5, text=solutions[i])
                pdf.set_text_color(0, 0, 0)
                
            # Right column (if exists)
            if i + 1 < len(questions):
                pdf.set_xy(10 + col_width + 10, y_start)
                pdf.multi_cell(w=col_width, h=5, text=questions[i+1])
                if include_solutions:
                    pdf.set_xy(10 + col_width + 10, pdf.get_y() + 2)
                    pdf.set_text_color(100, 100, 100)
                    pdf.multi_cell(w=col_width, h=5, text=solutions[i+1])
                    pdf.set_text_color(0, 0, 0)
            
            y_start += row_height

        # CEVAP ANAHTARI
        pdf.add_page()
        pdf.set_auto_page_break(auto=False)
        try:
            pdf.set_font("Arial", "B", 14)
        except:
            pass
        pdf.cell(0, 10, 'CEVAP ANAHTARI', border=0, new_x='LMARGIN', new_y='NEXT', align='C')
        pdf.ln(5)
        
        try:
            pdf.set_font("Arial", size=8)
        except:
            pdf.set_font("Helvetica", size=8)

        col_ans_width = 18
        ans_y_start = pdf.get_y()
        
        for ans_idx, ans in enumerate(answers):
            col_idx = ans_idx % 10
            row_idx = (ans_idx % 400) // 10
            
            if ans_idx > 0 and ans_idx % 400 == 0:
                pdf.add_page()
                ans_y_start = pdf.get_y()
                
            x_pos = 10 + (col_idx * col_ans_width)
            y_pos = ans_y_start + (row_idx * 6)
            
            pdf.set_xy(x_pos, y_pos)
            pdf.cell(col_ans_width, 6, f"{ans_idx+1}) {ans}", border=0)
            
        pdf.set_auto_page_break(auto=True, margin=15)
            
    # Build both PDFs
    build_pdf_content(pdf_normal, include_solutions=False)
    pdf_normal.output("TYT_Matematik_800_Soru.pdf")
    print("Successfully created TYT_Matematik_800_Soru.pdf")
    
    build_pdf_content(pdf_solved, include_solutions=True)
    pdf_solved.output("TYT_Matematik_800_Soru_Cozumlu.pdf")
    print("Successfully created TYT_Matematik_800_Soru_Cozumlu.pdf")
    
if __name__ == "__main__":
    generate_pdfs()
