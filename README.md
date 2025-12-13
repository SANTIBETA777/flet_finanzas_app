📘 README – Sistema de Gestión de Finanzas Personales
📌 Descripción del Proyecto
El Sistema de Gestión de Finanzas Personales es una aplicación desarrollada en Python, utilizando Flet para la interfaz gráfica y SQLite como base de datos local. Permite registrar ingresos, gastos, administrar categorías, visualizar transacciones, generar reportes y analizar información mediante un dashboard interactivo.

El proyecto está diseñado con una arquitectura modular, validaciones profesionales y una interfaz moderna.

🛠 Tecnologías Utilizadas
Python 3.10+

Flet (UI moderna tipo Flutter)

SQLite (base de datos local)

openpyxl (exportación a Excel)

reportlab (exportación a PDF)

datetime (validaciones)

📂 Estructura del Proyecto
Código
/ui
   /screens
      dashboard_screen.py
      ingresos_screen.py
      gastos_screen.py
      categorias_screen.py
      transacciones_screen.py
   components.py

/models.py
/database.py
/validators.py
/reports.py
/main.py
📦 Instalación
Sigue estos pasos para instalar y ejecutar el proyecto en tu equipo.

✅ 1. Clonar o descargar el proyecto
Si usas Git:

Código
git clone https://github.com/tu-repo/finanzas.git
cd finanzas
O simplemente descarga el ZIP y descomprímelo.

✅ 2. Crear un entorno virtual (opcional pero recomendado)
Windows:
Código
python -m venv venv
venv\Scripts\activate
Linux / WSL / Mac:
Código
python3 -m venv venv
source venv/bin/activate
✅ 3. Instalar dependencias
Ejecuta:

Código
pip install flet openpyxl reportlab
Si tienes un archivo requirements.txt, también puedes usar:

Código
pip install -r requirements.txt
✅ 4. Ejecutar la aplicación
En la raíz del proyecto:

Código
python main.py
La aplicación se abrirá automáticamente en una ventana Flet.

▶️ Uso de la Aplicación
1. Dashboard
Muestra totales de ingresos, gastos y saldo.

Gráficos de distribución y evolución mensual.

Últimas transacciones.

2. Gestión de Categorías
Crear, editar y eliminar categorías.

Validación de nombres.

Evita eliminar categorías en uso.

3. Registro de Ingresos
Formulario con validación.

Selección de categoría.

Tabla con historial.

Exportación a Excel y PDF.

4. Registro de Gastos
Formulario con DatePicker profesional.

Validación completa.

Tabla con historial.

Eliminación de registros.

5. Historial de Transacciones
Filtros avanzados:

Descripción

Tipo

Categoría

Fecha desde / hasta

Tabla profesional con acciones.

🗄 Base de Datos
Tabla: categorias
Campo	Tipo
id	INTEGER PK
nombre	TEXT UNIQUE
Tabla: transacciones
Campo	Tipo
id	INTEGER PK
tipo	TEXT
monto	REAL
fecha	TEXT
descripcion	TEXT
categoria_id	INTEGER FK
📊 Reportes
La aplicación permite exportar:

✔ Excel
Generado con openpyxl.

✔ PDF
Generado con reportlab.

Ambos incluyen:

Fecha

Tipo

Monto

Categoría

Descripción

🧠 Conclusiones
El proyecto cumple con los requisitos académicos.

La arquitectura modular facilita el mantenimiento.

La interfaz con Flet ofrece una experiencia moderna.

SQLite garantiza persistencia real.

Los reportes y gráficos agregan valor profesional.

👤 Autor
Santiago Proyecto académico – 2025

🔗 Enlace de Presentación
https://www.canva.com/design/DAG7bBh6Gpw/eg838NbQ8un1z93WOIMyGQ/edit?utm_content=DAG7bBh6Gpw&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton

presentacion en vidyard
https://share.vidyard.com/watch/zPmZK3rn9oEfiTrRXNx9dH