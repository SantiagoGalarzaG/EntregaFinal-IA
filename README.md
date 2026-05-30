# Diagnóstico de Envíos DIAN / RNDC
### Sistema Basado en Conocimiento — Proyecto Final IA II

**Autores:** Deyvid Santiago Galarza González · Jean Paul Solano Hernández  
**Institución:** Fundación Universitaria Los Libertadores  
**Asignatura:** Inteligencia Artificial II  
**Fecha:** 2026

---

## Descripción

Sistema experto que diagnostica automáticamente los errores al enviar documentos electrónicos
(facturas, notas crédito, remesas y manifiestos) desde un software de gestión de transporte
hacia la **DIAN** y el **RNDC** (Registro Nacional de Despachos de Carga).

El sistema aplica **encadenamiento hacia adelante** sobre una base de **35 reglas de producción**
formalizadas en lógica de predicados para identificar la causa raíz del problema.

---

## Estructura del proyecto

```
final/
├── README.md                   ← Este archivo
├── requirements.txt            ← Dependencias Python
│
├── src/
│   ├── base_conocimiento.py    ← Predicados, reglas y descripciones
│   ├── motor_inferencia.py     ← Motor de inferencia (encadenamiento adelante)
│   └── app.py                  ← Interfaz web Streamlit
│
├── docs/
│   ├── documentacion_tecnica.md  ← Documentación técnica completa
│   └── manual_usuario.md         ← Manual de usuario con capturas
│
└── tests/
    └── casos_prueba.md          ← Tabla formal de casos de prueba
```

---

## Requisitos del sistema

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

---

## Instalación

```bash
# 1. Clonar o descomprimir el proyecto
cd "IX semestre/Inteligencia artificial II/final"

# 2. (Opcional) Crear entorno virtual
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Instalar dependencias
pip install -r requirements.txt
```

---

## Ejecución

```bash
streamlit run src/app.py
```

El navegador se abrirá automáticamente en `http://localhost:8501`.  
Si no abre solo, copie la URL en Chrome o Edge.

---

## Características principales

| Característica | Detalle |
|---|---|
| Reglas de producción | 35 reglas en 10 grupos temáticos |
| Predicados del dominio | 28 predicados unarios formalizados |
| Diagnósticos posibles | 20 tipos (errores + éxitos) |
| Motor de inferencia | Encadenamiento hacia adelante con CWA |
| Certeza | Combinación probabilística `P(A∨B) = 1−(1−P(A))·(1−P(B))` |
| Explicación | Función `porque()` por diagnóstico individual |
| Logging | Registro completo del proceso de inferencia |
| Interfaz | Streamlit con ejemplos rápidos y barra de progreso |

---

## Demo rápida

En la barra lateral de la aplicación hay **6 ejemplos rápidos** precargados:

- 🔴 **DIAN caída** — Factura correcta rechazada sin falla técnica
- 📶 **Sin internet** — Intento de envío sin conexión
- 🔏 **Certificado vencido** — Certificado digital expirado
- ✅ **Manifiesto exitoso** — Envío correcto al RNDC
- 🚛 **Remesa — tercero inválido** — Datos del tercero incorrectos
- 🔁 **Documento duplicado** — Documento ya enviado anteriormente

---

## Tecnologías utilizadas

- **Python 3.x** — Lenguaje principal
- **Streamlit** — Framework de interfaz web
- **logging** (stdlib) — Registro del proceso de inferencia

---

## Archivos relevantes para la evaluación

| Criterio | Archivo(s) |
|---|---|
| Motor de inferencia | `src/motor_inferencia.py` |
| Base de conocimiento | `src/base_conocimiento.py` |
| Interfaz web | `src/app.py` |
| Documentación técnica | `docs/documentacion_tecnica.md` |
| Manual de usuario | `docs/manual_usuario.md` |
| Casos de prueba | `tests/casos_prueba.md` |
