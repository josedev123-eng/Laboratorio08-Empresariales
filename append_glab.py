"""Append the development section, the screenshots annex and the conclusions to the GLAB."""
import os

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from docx.text.paragraph import Paragraph
from PIL import Image

PATH = r"D:\Descargas\GLAB-S08-MMONTGOMERY-2026-02 (1).docx"
CAPTURAS = os.path.join("docs", "capturas")

FIGURAS = [
    ("00_estructura_proyecto.png", "A.1", "Estructura del proyecto en el editor (Visual Studio Code)",
     "Carpeta src con config, quiz, docs, templates, library, media, movies y news."),
    ("01_api_root.png", "A.2", "Raíz de la API - GET /quiz/ (200 OK)",
     "Raíz de la API con los enlaces a exams, questions y choices."),
    ("02_exams_list.png", "A.3", "Listado de exámenes - GET /quiz/exams/ (200 OK)",
     "Listado paginado de exámenes con sus preguntas anidadas."),
    ("03_questions_list.png", "A.4", "Listado de preguntas - GET /quiz/questions/ (200 OK)",
     "Preguntas con sus opciones de respuesta anidadas."),
    ("04_choices_list.png", "A.5", "Listado de opciones - GET /quiz/choices/ (200 OK)",
     "Listado de opciones de respuesta."),
    ("05_exam_detail.png", "A.6", "Detalle de un examen - GET /quiz/exams/4/ (200 OK)",
     "Detalle del examen con sus preguntas y opciones anidadas."),
    ("11_post_create.png", "A.7", "Crear examen - POST /quiz/exams/ (201 Created)",
     "Examen creado desde la API navegable; el servidor responde 201."),
    ("12_patch_update.png", "A.8", "Modificar parcialmente - PATCH /quiz/exams/18/ (200 OK)",
     "Descripción actualizada mediante PATCH; el servidor responde 200."),
    ("13_delete.png", "A.9", "Eliminar examen - DELETE /quiz/exams/18/ (204 No Content)",
     "Examen eliminado; el servidor responde 204."),
    ("14_filter_exam.png", "A.10", "Filtrado por examen - GET /quiz/questions/?exam=6 (200 OK)",
     "Solo se devuelve la pregunta del examen 6."),
    ("06_search_python.png", "A.11", "Búsqueda por texto - GET /quiz/questions/?search=Python (200 OK)",
     "Solo se devuelve la pregunta cuyo enunciado contiene 'Python'."),
    ("07_pagination.png", "A.12", "Paginación, página 1 - GET /quiz/exams/?page=1 (200 OK)",
     "13 resultados, 10 por página y enlace next a la página 2 (datos de prueba)."),
    ("15_pagination_page2.png", "A.13", "Paginación, página 2 - GET /quiz/exams/?page=2 (200 OK)",
     "Últimos 3 resultados y enlace previous a la página 1 (datos de prueba)."),
    ("08_error_missing_title.png", "A.14", "Error 400 - campo obligatorio ausente",
     "Error 400: 'This field is required.' al enviar un examen sin title."),
    ("09_error_wrong_type.png", "A.15", "Error 400 - tipo de dato incorrecto",
     "Error 400: 'Not a valid string.' al enviar title como objeto."),
    ("10_error_two_correct.png", "A.16", "Error 400 - pregunta sin exactamente una opción correcta",
     "Error 400: 'Exactly one choice must be marked as correct.'"),
]

TABLA_API = [
    ("Recurso", "Dirección", "Método", "Cuerpo de ejemplo", "Respuesta esperada"),
    ("Exámenes", "/quiz/exams/", "GET", "-", "200 OK - lista paginada"),
    ("Exámenes", "/quiz/exams/{id}/", "GET", "-", "200 OK - detalle con preguntas anidadas"),
    ("Exámenes", "/quiz/exams/", "POST", '{"title": "Nuevo", "description": "..."}', "201 Created"),
    ("Exámenes", "/quiz/exams/{id}/", "PATCH", '{"description": "Actualizada"}', "200 OK"),
    ("Exámenes", "/quiz/exams/{id}/", "DELETE", "-", "204 No Content"),
    ("Preguntas", "/quiz/questions/", "GET", "-", "200 OK - preguntas con opciones anidadas"),
    ("Preguntas", "/quiz/questions/?exam=6", "GET", "-", "200 OK - preguntas del examen 6"),
    ("Preguntas", "/quiz/questions/?search=Python", "GET", "-", "200 OK - coincidencias del enunciado"),
    ("Preguntas", "/quiz/questions/", "POST",
     '{"statement": "...", "exam": 1, "score": 2, "choices": [...]}', "201 Created"),
    ("Preguntas", "/quiz/questions/{id}/", "DELETE", "-", "204 No Content"),
    ("Opciones", "/quiz/choices/", "GET", "-", "200 OK - lista de opciones"),
    ("Opciones", "/quiz/choices/", "POST", '{"text": "Opción", "is_correct": true}', "201 Created"),
    ("Raíz API", "/quiz/", "GET", "-", "200 OK - enlaces a los tres recursos"),
]

TABLA_CASOS = [
    ("Caso de prueba", "Método", "URL", "Código real"),
    ("Raíz de la API", "GET", "/quiz/", "200"),
    ("Listar exámenes", "GET", "/quiz/exams/", "200"),
    ("Listar preguntas", "GET", "/quiz/questions/", "200"),
    ("Listar opciones", "GET", "/quiz/choices/", "200"),
    ("Ver detalle", "GET", "/quiz/exams/4/", "200"),
    ("Crear examen", "POST", "/quiz/exams/", "201"),
    ("Modificar parcialmente", "PATCH", "/quiz/exams/18/", "200"),
    ("Eliminar examen", "DELETE", "/quiz/exams/18/", "204"),
    ("Filtrar por examen", "GET", "/quiz/questions/?exam=6", "200"),
    ("Buscar por texto", "GET", "/quiz/questions/?search=Python", "200"),
    ("Paginación, página 1", "GET", "/quiz/exams/?page=1", "200"),
    ("Paginación, página 2", "GET", "/quiz/exams/?page=2", "200"),
    ("Campo obligatorio ausente", "POST", "/quiz/exams/", "400"),
    ("Tipo de dato incorrecto", "POST", "/quiz/exams/", "400"),
    ("Pregunta sin una sola opción correcta", "POST", "/quiz/questions/", "400"),
]

CODIGO_SERIALIZER = """class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = ["id", "statement", "exam", "score", "choices"]

    def validate(self, data):
        choices = data.get("choices", [])
        correct = sum(1 for choice in choices if choice.get("is_correct"))
        if correct != 1:
            raise serializers.ValidationError(
                {"choices": "Exactly one choice must be marked as correct."}
            )
        return data"""

CODIGO_VIEWS = """class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        exam = self.request.query_params.get("exam")
        search = self.request.query_params.get("search")
        if exam:
            queryset = queryset.filter(exam_id=exam)
        if search:
            queryset = queryset.filter(statement__icontains=search)
        return queryset"""

CONCLUSIONES = [
    "1. Django REST Framework permitió exponer los modelos Exam, Question y Choice como "
    "un servicio web REST reutilizando los modelos y las validaciones ya existentes en el "
    "proyecto, con muy poco código adicional.",
    "2. Los ModelSerializer mantienen las relaciones del modelo: las opciones viajan anidadas "
    "dentro de la pregunta y el examen se referencia por identificador. La validación propia "
    "de QuestionSerializer impide guardar una pregunta que no tenga exactamente una opción "
    "correcta.",
    "3. El DefaultRouter publicó los tres recursos de forma navegable y las pruebas con un "
    "cliente HTTP externo confirmaron los códigos esperados: 200 al consultar, 201 al crear, "
    "204 al eliminar y 400 ante datos inválidos. Los mensajes devueltos ('This field is "
    "required.', 'Not a valid string.' y 'Exactly one choice must be marked as correct.') "
    "describen con claridad el error.",
    "4. La paginación con PAGE_SIZE = 10, la búsqueda por texto y el filtrado por examen dejan "
    "la API lista para ser consumida por un cliente externo, y la API navegable facilita su "
    "verificación durante el desarrollo.",
]


def preparar(p, before=0, after=0, align=None, keep_next=False):
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = 1.08
    pf.left_indent = 0
    pf.first_line_indent = 0
    pf.keep_with_next = keep_next
    if align is not None:
        p.alignment = align
    return p


def escribir(p, texto, size=11, bold=False, italic=False, color=None, font="Arial"):
    run = p.add_run(texto)
    run.font.name = font
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = RGBColor.from_string(color)
    return run


doc = Document(PATH)

conclusiones = None
for p in doc.paragraphs:
    if p.text.strip().lower().startswith("conclusiones"):
        conclusiones = p
if conclusiones is None:
    raise SystemExit("No se encontró la sección Conclusiones")

# The original document ends with an empty numbered item that renders a stray "1.".
next_el = conclusiones._p.getnext()
trailing_p = Paragraph(next_el, conclusiones._parent) if next_el is not None else None


def titulo(texto, page_break=False, size=11, before=10):
    p = preparar(conclusiones.insert_paragraph_before(), before=before, after=6, keep_next=True)
    if page_break:
        p.paragraph_format.page_break_before = True
    escribir(p, texto, size=size, bold=True)
    return p


def parrafo(texto, size=11, after=6, align=WD_ALIGN_PARAGRAPH.JUSTIFY, italic=False,
            color=None, keep_next=False):
    p = preparar(conclusiones.insert_paragraph_before(), after=after, align=align,
                 keep_next=keep_next)
    escribir(p, texto, size=size, italic=italic, color=color)
    return p


def codigo(texto):
    p = preparar(conclusiones.insert_paragraph_before(), before=2, after=8)
    p.paragraph_format.left_indent = Inches(0.12)
    p.paragraph_format.line_spacing = 0.98
    p.paragraph_format.keep_together = True
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), "F2F2F2")
    p._p.get_or_add_pPr().append(shd)
    lineas = texto.split("\n")
    for i, linea in enumerate(lineas):
        run = p.add_run(linea)
        run.font.name = "Consolas"
        run.font.size = Pt(8)
        if i < len(lineas) - 1:
            run.add_break()
    return p


def tabla(filas, anchos, size=8.5):
    t = doc.add_table(rows=len(filas), cols=len(filas[0]))
    try:
        t.style = "Table Grid"
    except KeyError:
        pass
    t.autofit = False
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    t._tbl.tblPr.append(layout)
    for c_idx, ancho in enumerate(anchos):
        t.columns[c_idx].width = Inches(ancho)
    for r_idx, fila in enumerate(filas):
        for c_idx, valor in enumerate(fila):
            cell = t.cell(r_idx, c_idx)
            cell.width = Inches(anchos[c_idx])
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.line_spacing = 1.0
            run = p.add_run(str(valor))
            run.font.name = "Arial"
            run.font.size = Pt(size)
            run.bold = r_idx == 0
            if r_idx == 0:
                shd = OxmlElement("w:shd")
                shd.set(qn("w:fill"), "CFE2F3")
                cell._tc.get_or_add_tcPr().append(shd)
    # repeat the header row when the table spans more than one page
    tr_pr = t.rows[0]._tr.get_or_add_trPr()
    cabecera = OxmlElement("w:tblHeader")
    tr_pr.append(cabecera)
    conclusiones._p.addprevious(t._tbl)
    return t


# ============ 1. Desarrollo del laboratorio ================================
titulo("Desarrollo del laboratorio", page_break=True, size=12, before=0)

parrafo(
    "Alumno: Michael Montgomery Rosell.  Título del desarrollo: Implementación de "
    "Servicios Web con Django.",
    after=4,
)
parrafo(
    "Sobre el proyecto de cuestionarios se añadió Django REST Framework y se publicaron los "
    "tres recursos del dominio (exámenes, preguntas y opciones) con ModelViewSet y un "
    "DefaultRouter. Las relaciones se resolvieron de forma mixta: las opciones viajan "
    "anidadas dentro de la pregunta y el examen se referencia por su identificador. El "
    "serializador de pregunta valida que haya exactamente una opción correcta, y los "
    "conjuntos de vistas incorporan filtrado por examen (?exam=) y búsqueda de texto "
    "(?search=) sobre el enunciado.",
    after=6,
)

# ============ 2. Tabla de la API ==========================================
titulo("1. Tabla de la API")
parrafo(
    "Cada fila se comprobó contra el servidor en http://127.0.0.1:8000 con la API navegable "
    "de DRF y con un cliente HTTP externo que envía el cuerpo en JSON. Los códigos de estado "
    "coinciden con lo que la API devuelve realmente.",
    after=6,
)
tabla(TABLA_API, [0.85, 1.9, 0.6, 1.75, 1.4], size=8)
parrafo("", after=4)

# ============ 3. Código principal ========================================
titulo("2. Código principal")
parrafo(
    "Validación de la pregunta en quiz/serializers.py: se rechaza cualquier pregunta que no "
    "tenga exactamente una opción marcada como correcta.",
    after=2,
)
codigo(CODIGO_SERIALIZER)
parrafo(
    "Filtrado por examen y búsqueda por texto en quiz/views.py: se leen los parámetros de la "
    "consulta y se aplican sobre el queryset del conjunto de vistas.",
    after=2,
)
codigo(CODIGO_VIEWS)

# ============ 4. Casos de prueba =========================================
titulo("3. Casos de prueba")
parrafo(
    "Operaciones ejecutadas contra la API y código de estado devuelto en cada una. Las "
    "capturas de la sección siguiente muestran la respuesta del servidor.",
    after=6,
)
tabla(TABLA_CASOS, [2.35, 0.75, 2.35, 0.85], size=8)
parrafo("", after=4)

# ============ 5. Anexo de capturas ======================================
titulo("Anexo. Capturas de pantalla", page_break=True, size=12, before=0)

parrafo(
    "Las siguientes capturas se tomaron directamente del servidor real en "
    "http://127.0.0.1:8000, sobre la API navegable de Django REST Framework. "
    "Cada imagen muestra el código de estado HTTP devuelto por el servidor. "
    "Las pruebas de filtrado y paginación usan datos temporales de apoyo "
    "(un segundo examen y exámenes de paginación).",
    keep_next=True,
)

for filename, numero, titulo_fig, pie in FIGURAS:
    path = os.path.join(CAPTURAS, filename)

    sub = preparar(conclusiones.insert_paragraph_before(), before=8, after=4, keep_next=True)
    escribir(sub, f"{numero} {titulo_fig}", size=11, bold=True)

    with Image.open(path) as image:
        w_px, h_px = image.size
    width_in = 6.2
    if width_in * h_px / w_px > 6.4:
        width_in = 6.4 * w_px / h_px

    pic_p = preparar(
        conclusiones.insert_paragraph_before(),
        after=2,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        keep_next=True,
    )
    pic_p.add_run().add_picture(path, width=Inches(width_in))

    cap = preparar(
        conclusiones.insert_paragraph_before(),
        after=6,
        align=WD_ALIGN_PARAGRAPH.CENTER,
    )
    escribir(cap, f"Figura {numero}. {pie}", size=9, italic=True, color="595959")

# ============ 6. Conclusiones ===========================================
target = trailing_p if trailing_p is not None else conclusiones
for texto in CONCLUSIONES:
    p = preparar(target.insert_paragraph_before(), after=6, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
    escribir(p, texto)

# Remove the empty numbered paragraph so no stray "1." is rendered.
if trailing_p is not None:
    trailing_p._p.getparent().remove(trailing_p._p)

doc.save(PATH)
print("Documento guardado:", PATH)
print("párrafos:", len(doc.paragraphs), "imágenes:", len(doc.inline_shapes), "tablas:", len(doc.tables))
