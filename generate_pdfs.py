"""
generate_pdfs.py — Genera PDFs de la documentación técnica y manual de usuario
Ejecutar desde la raíz del proyecto: python generate_pdfs.py
"""
import re
from pathlib import Path
from fpdf import FPDF

# Mapa de caracteres Unicode que Helvetica (Latin-1) no soporta
_REPLACEMENTS = [
    ("—", "-"),   # em dash —
    ("–", "-"),   # en dash –
    ("’", "'"),   # comilla derecha '
    ("‘", "'"),   # comilla izquierda '
    ("“", '"'),   # comilla doble izq "
    ("”", '"'),   # comilla doble der "
    ("→", "->"),  # flecha derecha →
    ("←", "<-"),  # flecha izquierda ←
    ("✔", "[OK]"),# check mark ✔
    ("✓", "[OK]"),# check mark ✓
    ("✗", "[X]"), # cross mark ✗
    ("✕", "[X]"), # cross mark ✕
    ("✖", "[X]"), # cross mark ✖
    ("•", "-"),   # bullet •
    ("›", ">"),   # single angle >
    ("≥", ">="),  # >=
    ("≤", "<="),  # <=
    ("×", "x"),   # multiplication ×
    ("∧", "Y"),   # logical AND ∧
    ("∨", "O"),   # logical OR ∨
    ("¬", "NOT"), # NOT ¬
    ("∀", "para todo "), # forall ∀
    ("∃", "existe "),    # exists ∃
    # Emojis comunes en la documentación
    ("\U0001f4cb", "[Doc]"),
    ("\U0001f4e6", "[Box]"),
    ("\U0001f4c4", "[File]"),
    ("\U0001f4dd", "[Note]"),
    ("\U0001f6e3", "[Road]"),
    ("\U0001f50d", "[Search]"),
    ("⚠", "[!]"),  # warning ⚠
    ("\U0001f6a8", "[!]"),
    ("✅", "[SI]"), # ✅
    ("❌", "[NO]"), # ❌
    ("\U0001f4cc", "[Pin]"),
    ("\U0001f4f6", "[Signal]"),
    ("\U0001f510", "[Lock]"),
    ("\U0001f501", "[Loop]"),
    ("\U0001f6a7", "[Work]"),
    ("\U0001f1e8", ""),  # flag letters
    ("\U0001f1f4", ""),
    ("\U0001f4ca", "[Chart]"),
    ("\U0001f527", "[Tool]"),
    ("ℹ", "[i]"),
    ("✨", "*"),
    ("\U0001f3db", "[Lib]"),
    ("\U0001f3c1", "[Goal]"),
    ("\U0001f4a1", "[Idea]"),
    ("\U0001f6d1", "[Stop]"),
    ("\U0001f916", "[Bot]"),
    ("\U0001f310", "[Web]"),
]

def _sanitize(text: str) -> str:
    """Reemplaza caracteres fuera de Latin-1 por equivalentes ASCII."""
    for uni, asc in _REPLACEMENTS:
        text = text.replace(uni, asc)
    # Eliminar cualquier otro carácter fuera de Latin-1
    return text.encode("latin-1", errors="replace").decode("latin-1")


# ─────────────────────────────────────────────────────────────────────────────
# CLASE PDF PERSONALIZADA
# ─────────────────────────────────────────────────────────────────────────────

class PDF(FPDF):
    def __init__(self, titulo_doc):
        super().__init__()
        self.titulo_doc = titulo_doc
        self.set_margins(20, 20, 20)
        self.set_auto_page_break(auto=True, margin=20)

    def header(self):
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 8, _sanitize(self.titulo_doc), align="L")
        self.cell(0, 8, "Galarza & Solano - Los Libertadores 2026", align="R")
        self.ln(2)
        self.set_draw_color(200, 200, 200)
        self.line(20, self.get_y(), 190, self.get_y())
        self.ln(4)
        self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")
        self.set_text_color(0, 0, 0)

    def cover_page(self, titulo, subtitulo, autores, fecha):
        self.add_page()
        # Franja azul superior
        self.set_fill_color(15, 23, 42)
        self.rect(0, 0, 210, 60, "F")
        self.set_fill_color(29, 78, 216)
        self.rect(0, 58, 210, 6, "F")
        # Institución
        self.set_y(18)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(147, 197, 253)
        self.cell(0, 8, _sanitize("Fundacion Universitaria Los Libertadores"), align="C")
        self.ln(6)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(191, 219, 254)
        self.cell(0, 6, "Inteligencia Artificial II - Proyecto Final", align="C")
        # Título principal
        self.set_y(80)
        self.set_font("Helvetica", "B", 20)
        self.set_text_color(15, 23, 42)
        self.multi_cell(0, 10, _sanitize(titulo), align="C")
        self.ln(4)
        # Subtítulo
        self.set_font("Helvetica", "I", 13)
        self.set_text_color(71, 85, 105)
        self.multi_cell(0, 8, _sanitize(subtitulo), align="C")
        self.ln(14)
        # Línea divisoria
        self.set_draw_color(29, 78, 216)
        self.set_line_width(0.8)
        self.line(40, self.get_y(), 170, self.get_y())
        self.ln(10)
        # Autores
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(30, 41, 59)
        self.cell(0, 7, "Autores:", align="C")
        self.ln(7)
        for autor in autores:
            self.set_font("Helvetica", "", 10)
            self.set_text_color(51, 65, 85)
            self.cell(0, 6, autor, align="C")
            self.ln(6)
        self.ln(8)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(100, 116, 139)
        self.cell(0, 6, fecha, align="C")
        self.set_line_width(0.2)
        self.set_draw_color(0, 0, 0)
        self.set_text_color(0, 0, 0)


# ─────────────────────────────────────────────────────────────────────────────
# PARSER DE MARKDOWN → INSTRUCCIONES PDF
# ─────────────────────────────────────────────────────────────────────────────

def md_to_pdf(pdf: PDF, md_text: str):
    """Convierte Markdown a llamadas FPDF. Soporta: H1-H4, párrafos, listas,
    bloques de código, tablas, negrita, cursiva y separadores."""

    lines = md_text.split("\n")
    i = 0
    in_code = False
    code_buf = []

    def flush_code(buf):
        if not buf:
            return
        pdf.set_fill_color(241, 245, 249)
        pdf.set_draw_color(203, 213, 225)
        pdf.set_font("Courier", "", 8)
        pdf.set_text_color(30, 41, 59)
        content = "\n".join(buf)
        # Calcular altura del bloque
        line_h = 5
        n_lines = content.count("\n") + 1
        box_h = n_lines * line_h + 6
        x0 = pdf.get_x()
        y0 = pdf.get_y()
        if y0 + box_h > pdf.h - pdf.b_margin:
            pdf.add_page()
            y0 = pdf.get_y()
        pdf.rect(x0, y0, 170, box_h, "FD")
        pdf.set_xy(x0 + 3, y0 + 3)
        for ln in buf:
            safe = _sanitize(ln.replace("\x00", ""))
            pdf.cell(164, line_h, safe[:110])
            pdf.ln(line_h)
        pdf.ln(3)
        pdf.set_text_color(0, 0, 0)
        pdf.set_draw_color(0, 0, 0)

    def write_inline(text: str, base_size: int = 10):
        """Escribe texto con negrita e itálica inline."""
        # Dividir por ** y *
        parts = re.split(r'(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)', text)
        for part in parts:
            if not part:
                continue
            if part.startswith("**") and part.endswith("**"):
                pdf.set_font("Helvetica", "B", base_size)
                pdf.write(6, _sanitize(part[2:-2].replace("\x00","")))
            elif part.startswith("*") and part.endswith("*"):
                pdf.set_font("Helvetica", "I", base_size)
                pdf.write(6, _sanitize(part[1:-1].replace("\x00","")))
            elif part.startswith("`") and part.endswith("`"):
                pdf.set_font("Courier", "", base_size - 1)
                pdf.set_text_color(99, 63, 175)
                pdf.write(6, _sanitize(part[1:-1].replace("\x00","")))
                pdf.set_text_color(0, 0, 0)
            else:
                pdf.set_font("Helvetica", "", base_size)
                pdf.write(6, _sanitize(part.replace("\x00","")))
        pdf.set_font("Helvetica", "", base_size)

    while i < len(lines):
        line = lines[i]

        # ── Bloques de código ──────────────────────────────────────────────
        if line.strip().startswith("```"):
            if not in_code:
                in_code = True
                code_buf = []
            else:
                in_code = False
                flush_code(code_buf)
                code_buf = []
            i += 1
            continue

        if in_code:
            code_buf.append(line)
            i += 1
            continue

        # ── Separador horizontal ───────────────────────────────────────────
        if re.match(r'^---+$', line.strip()):
            pdf.ln(2)
            pdf.set_draw_color(200, 200, 200)
            pdf.line(20, pdf.get_y(), 190, pdf.get_y())
            pdf.ln(4)
            pdf.set_draw_color(0, 0, 0)
            i += 1
            continue

        # ── Tablas ────────────────────────────────────────────────────────
        if line.strip().startswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                if not re.match(r'^\|[-| :]+\|$', lines[i].strip()):
                    table_lines.append(lines[i])
                i += 1
            if table_lines:
                _render_table(pdf, table_lines)
            continue

        # ── Encabezados ────────────────────────────────────────────────────
        if line.startswith("#### "):
            pdf.ln(2)
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(71, 85, 105)
            pdf.cell(0, 7, _sanitize(line[5:].replace("\x00","")))
            pdf.ln(7)
            pdf.set_text_color(0, 0, 0)
        elif line.startswith("### "):
            pdf.ln(3)
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(30, 41, 59)
            pdf.cell(0, 8, _sanitize(line[4:].replace("\x00","")))
            pdf.ln(8)
            pdf.set_draw_color(219, 234, 254)
            pdf.line(20, pdf.get_y(), 190, pdf.get_y())
            pdf.set_draw_color(0, 0, 0)
            pdf.ln(1)
            pdf.set_text_color(0, 0, 0)
        elif line.startswith("## "):
            pdf.ln(5)
            pdf.set_fill_color(239, 246, 255)
            pdf.set_font("Helvetica", "B", 13)
            pdf.set_text_color(29, 78, 216)
            pdf.cell(0, 9, _sanitize(line[3:].replace("\x00","")), fill=True)
            pdf.ln(9)
            pdf.set_text_color(0, 0, 0)
            pdf.ln(1)
        elif line.startswith("# "):
            pdf.add_page()
            pdf.ln(4)
            pdf.set_font("Helvetica", "B", 16)
            pdf.set_text_color(15, 23, 42)
            pdf.cell(0, 10, _sanitize(line[2:].replace("\x00","")))
            pdf.ln(10)
            pdf.set_draw_color(29, 78, 216)
            pdf.set_line_width(0.8)
            pdf.line(20, pdf.get_y(), 190, pdf.get_y())
            pdf.set_line_width(0.2)
            pdf.set_draw_color(0, 0, 0)
            pdf.ln(4)
            pdf.set_text_color(0, 0, 0)

        # ── Listas ─────────────────────────────────────────────────────────
        elif re.match(r'^(\s*[-*]|\s*\d+\.) ', line):
            indent = len(line) - len(line.lstrip())
            bullet = "-" if re.match(r'\s*[-*] ', line) else ">"
            content = _sanitize(re.sub(r'^\s*([-*]|\d+\.)\s+', '', line))
            x = pdf.get_x() + indent * 0.5 + 4
            pdf.set_x(x)
            pdf.set_font("Helvetica", "", 9)
            pdf.cell(5, 6, bullet, border=0)
            pdf.set_x(x + 5)
            write_inline(content, 9)
            pdf.ln(6)

        # ── Párrafos normales ──────────────────────────────────────────────
        elif line.strip():
            pdf.set_font("Helvetica", "", 10)
            write_inline(_sanitize(line.strip()), 10)
            pdf.ln(6)
        else:
            if i > 0 and lines[i-1].strip():
                pdf.ln(2)

        i += 1

    if in_code and code_buf:
        flush_code(code_buf)


def _render_table(pdf: PDF, rows: list):
    """Renderiza una tabla Markdown simple."""
    pdf.ln(2)
    parsed = []
    for row in rows:
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        parsed.append(cells)

    if not parsed:
        return

    n_cols = max(len(r) for r in parsed)
    col_w  = 168 / n_cols

    for r_idx, row in enumerate(parsed):
        # Cabecera: fondo azul oscuro
        if r_idx == 0:
            pdf.set_fill_color(30, 58, 138)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Helvetica", "B", 8)
        elif r_idx % 2 == 0:
            pdf.set_fill_color(239, 246, 255)
            pdf.set_text_color(30, 41, 59)
            pdf.set_font("Helvetica", "", 8)
        else:
            pdf.set_fill_color(255, 255, 255)
            pdf.set_text_color(30, 41, 59)
            pdf.set_font("Helvetica", "", 8)

        for c_idx in range(n_cols):
            txt = row[c_idx] if c_idx < len(row) else ""
            txt = re.sub(r'\*\*(.+?)\*\*', r'\1', txt)  # quitar negrita
            txt = _sanitize(txt.replace("`", "").replace("\x00",""))
            pdf.cell(col_w, 7, txt[:50], border=1, fill=True)
        pdf.ln()

    pdf.set_text_color(0, 0, 0)
    pdf.set_fill_color(255, 255, 255)
    pdf.ln(3)


# ─────────────────────────────────────────────────────────────────────────────
# GENERADOR PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────

def generate(md_path: str, pdf_path: str, titulo: str, subtitulo: str):
    text = Path(md_path).read_text(encoding="utf-8")
    # Eliminar la línea H1 del markdown (ya va en la portada)
    lines = text.split("\n")
    body_lines = [l for l in lines if not l.startswith("# " + subtitulo.split("—")[0].strip())]
    body = "\n".join(body_lines)

    pdf = PDF(titulo)
    pdf.cover_page(
        titulo=titulo,
        subtitulo=subtitulo,
        autores=["Deyvid Santiago Galarza González", "Jean Paul Solano Hernández"],
        fecha="Mayo 2026",
    )
    pdf.add_page()
    md_to_pdf(pdf, body)
    pdf.output(pdf_path)
    print(f"  ✓ Generado: {pdf_path}")


if __name__ == "__main__":
    base = Path(__file__).parent

    print("Generando PDFs de documentación...")

    generate(
        md_path  = str(base / "docs" / "documentacion_tecnica.md"),
        pdf_path = str(base / "docs" / "documentacion_tecnica.pdf"),
        titulo   = "Documentación Técnica",
        subtitulo= "Sistema Basado en Conocimiento — Diagnóstico DIAN / RNDC",
    )

    generate(
        md_path  = str(base / "docs" / "manual_usuario.md"),
        pdf_path = str(base / "docs" / "manual_usuario.pdf"),
        titulo   = "Manual de Usuario",
        subtitulo= "Sistema de Diagnóstico de Envíos DIAN / RNDC",
    )

    print("\nPDFs generados en docs/")
