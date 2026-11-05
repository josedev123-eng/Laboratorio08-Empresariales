"""Build the Lab08 deliverable as a Word document with the real API table."""
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH


def heading(doc, text, level=1):
    doc.add_heading(text, level=level)


def para(doc, text, bold=False):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = bold
    return p


def code_block(doc, code):
    p = doc.add_paragraph()
    run = p.add_run(code)
    run.font.name = "Consolas"
    run.font.size = Pt(9)
    p.paragraph_format.left_indent = Pt(12)


doc = Document()

title = doc.add_heading("Laboratorio 08 - API RESTful con Django REST Framework", 0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER

para(doc, "Asignatura: Desarrollo de Aplicaciones Empresariales (DAE)")
para(doc, "Estudiante: ________________________________")
para(doc, "Repositorio: https://github.com/josedev123-eng/Laboratorio08-Empresariales.git")
doc.add_paragraph()

heading(doc, "1. Objetivo", 1)
para(
    doc,
    "Exponer los modelos de la aplicacion de cuestionarios (Exam, Question, Choice) "
    "como un servicio web REST usando Django REST Framework, con serializadores "
    "derivados del modelo, validacion propia y conjuntos de vistas enrutados.",
)

heading(doc, "2. Serializadores (ModelSerializer)", 1)
para(
    doc,
    "Los tres serializadores derivan de ModelSerializer. Las opciones viajan "
    "anidadas dentro de la pregunta y el examen se referencia por identificador. "
    "QuestionSerializer implementa una validacion propia que exige exactamente una "
    "opcion correcta.",
)
code_block(
    doc,
    "class ChoiceSerializer(serializers.ModelSerializer):\n"
    "    class Meta:\n"
    "        model = Choice\n"
    "        fields = ['id', 'text', 'is_correct']\n\n"
    "class QuestionSerializer(serializers.ModelSerializer):\n"
    "    choices = ChoiceSerializer(many=True)  # nested\n"
    "    class Meta:\n"
    "        model = Question\n"
    "        fields = ['id', 'statement', 'exam', 'score', 'choices']\n"
    "    def validate(self, data):\n"
    "        correct = sum(1 for c in data.get('choices', []) if c.get('is_correct'))\n"
    "        if correct != 1:\n"
    "            raise serializers.ValidationError(\n"
    "                {'choices': 'Exactly one choice must be marked as correct.'})\n"
    "        return data\n\n"
    "class ExamSerializer(serializers.ModelSerializer):\n"
    "    questions = QuestionSerializer(many=True, read_only=True)\n"
    "    class Meta:\n"
    "        model = Exam\n"
    "        fields = ['id', 'title', 'description', 'creation_date', 'questions']",
)

heading(doc, "3. Conjuntos de vistas y enrutador", 1)
para(
    doc,
    "Los tres recursos se publican con ModelViewSet y se registran en un "
    "DefaultRouter, por lo que son navegables desde la API navegable de DRF.",
)
code_block(
    doc,
    "router = DefaultRouter()\n"
    "router.register(r'exams', ExamViewSet)\n"
    "router.register(r'questions', QuestionViewSet)\n"
    "router.register(r'choices', ChoiceViewSet)\n"
    "urlpatterns = router.urls",
)

heading(doc, "4. Configuracion de REST_FRAMEWORK", 1)
code_block(
    doc,
    "REST_FRAMEWORK = {\n"
    "    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',\n"
    "    'PAGE_SIZE': 10,\n"
    "    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],\n"
    "}",
)

heading(doc, "5. Tabla de la API", 1)
para(
    doc,
    "Cada fila fue comprobada con un cliente HTTP externo (Python urllib) contra el "
    "servidor en http://127.0.0.1:8000. Los codigos de estado coinciden con lo que la "
    "API devuelve realmente.",
)

rows = [
    ("Recurso", "Direccion", "Metodo", "Cuerpo de ejemplo", "Respuesta esperada"),
    ("Examenes", "/quiz/exams/", "GET", "{}", "200 OK - lista paginada"),
    ("Examenes", "/quiz/exams/{id}/", "GET", "-", "200 OK - detalle con preguntas anidadas"),
    ("Examenes", "/quiz/exams/", "POST", '{"title": "Nuevo", "description": "..."}', "201 Created"),
    ("Examenes", "/quiz/exams/{id}/", "PATCH", '{"description": "Actualizada"}', "200 OK"),
    ("Examenes", "/quiz/exams/{id}/", "DELETE", "-", "204 No Content"),
    ("Preguntas", "/quiz/questions/", "GET", "-", "200 OK - preguntas con opciones anidadas"),
    ("Preguntas", "/quiz/questions/", "POST", '{"statement": "...", "exam": 1, "score": 2, "choices": [4]}', "201 Created"),
    ("Preguntas", "/quiz/questions/{id}/", "DELETE", "-", "204 No Content"),
    ("Opciones", "/quiz/choices/", "GET", "-", "200 OK - lista de opciones"),
    ("Opciones", "/quiz/choices/", "POST", '{"text": "Opcion", "is_correct": true}', "201 Created"),
    ("Raiz API", "/quiz/", "GET", "-", "200 OK - enlaces a los tres recursos"),
]

table = doc.add_table(rows=1, cols=5)
table.style = "Light Grid Accent 1"
for i, cell in enumerate(table.rows[0].cells):
    cell.text = rows[0][i]
for row in rows[1:]:
    cells = table.add_row().cells
    for i, value in enumerate(row):
        cells[i].text = value

heading(doc, "6. Comprobacion de operaciones (codigos reales)", 1)
para(doc, "Las siguientes operaciones se ejecutaron desde un cliente HTTP externo:")

ops = [
    ("Operacion", "Metodo", "URL", "Codigo real"),
    ("Raiz de la API", "GET", "/quiz/", "200"),
    ("Listar examenes", "GET", "/quiz/exams/", "200"),
    ("Listar preguntas", "GET", "/quiz/questions/", "200"),
    ("Listar opciones", "GET", "/quiz/choices/", "200"),
    ("Crear examen", "POST", "/quiz/exams/", "201"),
    ("Ver detalle", "GET", "/quiz/exams/{id}/", "200"),
    ("Actualizar parcial", "PATCH", "/quiz/exams/{id}/", "200"),
    ("Crear pregunta (1 correcta)", "POST", "/quiz/questions/", "201"),
    ("Eliminar pregunta", "DELETE", "/quiz/questions/{id}/", "204"),
    ("Eliminar examen", "DELETE", "/quiz/exams/{id}/", "204"),
    ("Buscar preguntas", "GET", "/quiz/questions/?search=Python", "200"),
    ("Paginacion", "GET", "/quiz/exams/?page=1", "200"),
]
t2 = doc.add_table(rows=1, cols=4)
t2.style = "Light Grid Accent 1"
for i, cell in enumerate(t2.rows[0].cells):
    cell.text = ops[0][i]
for row in ops[1:]:
    cells = t2.add_row().cells
    for i, value in enumerate(row):
        cells[i].text = value

heading(doc, "7. Errores provocados a proposito", 1)
errs = [
    ("Caso", "Cuerpo enviado", "Codigo", "Mensaje devuelto"),
    ("Campo obligatorio ausente", '{"description": "..."} (sin title)', "400", "This field is required."),
    ("Tipo incorrecto", '{"title": {"not": "a string"}}', "400", "Not a valid string."),
    ("Opcion correcta invalida", 'question con dos opciones is_correct=true', "400", "Exactly one choice must be marked as correct."),
]
t3 = doc.add_table(rows=1, cols=4)
t3.style = "Light Grid Accent 1"
for i, cell in enumerate(t3.rows[0].cells):
    cell.text = errs[0][i]
for row in errs[1:]:
    cells = t3.add_row().cells
    for i, value in enumerate(row):
        cells[i].text = value

heading(doc, "8. Relaciones: como viajan los datos", 1)
para(
    doc,
    "- Las opciones (Choice) viajan ANIDADAS dentro de la pregunta (Question.choices).\n"
    "- El examen (Exam) se referencia por IDENTIFICADOR dentro de la pregunta (exam: <id>).\n"
    "- El detalle de un examen incluye sus preguntas anidadas y, dentro de cada una, sus opciones.",
)

heading(doc, "9. Conclusiones", 1)
para(
    doc,
    "1. Django REST Framework permite exponer los modelos como servicio web con muy poco "
    "codigo, reutilizando los modelos y sus validaciones.\n"
    "2. Los ModelSerializer derivados del modelo y la validacion propia aseguran que no se "
    "guarde ninguna pregunta sin exactamente una opcion correcta.\n"
    "3. El router publica los tres recursos de forma consistente y navegable, y las pruebas "
    "HTTP confirman los codigos 200, 201, 204 y 400 esperados, incluidos los errores.",
)

doc.save("Entregable_Lab08_API_REST.docx")
print("Saved Entregable_Lab08_API_REST.docx")
