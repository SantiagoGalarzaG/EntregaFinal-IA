# Manual de Usuario
## Sistema de Diagnóstico de Envíos DIAN / RNDC

**Versión:** 1.0  
**Autores:** Galarza, Solano — Fundación Universitaria Los Libertadores, 2026

---

## 1. Instalación

### 1.1 Requisitos del sistema

| Requisito | Mínimo |
|---|---|
| Sistema operativo | Windows 10/11, macOS 12+, Ubuntu 20.04+ |
| Python | 3.8 o superior |
| Navegador | Chrome, Edge o Firefox (versión reciente) |
| Conexión a internet | No requerida para ejecutar localmente |

### 1.2 Pasos de instalación

**Paso 1 — Instalar Python** (si no lo tiene):  
Descargue Python desde https://www.python.org/downloads/ y marque "Add Python to PATH" durante la instalación.

**Paso 2 — Verificar Python:**
```bash
python --version
# Debe mostrar Python 3.8 o superior
```

**Paso 3 — Instalar dependencias:**
```bash
pip install -r requirements.txt
```

### 1.3 Cómo ejecutar la aplicación

Abra una terminal en la carpeta del proyecto y ejecute:

```bash
streamlit run src/app.py
```

El navegador se abrirá automáticamente en `http://localhost:8501`.  
Si no abre solo, copie esa dirección en su navegador.

Para detener la aplicación presione `Ctrl + C` en la terminal.

---

## 2. Uso de la interfaz

### 2.1 Descripción general de la pantalla

La aplicación tiene dos secciones principales:

**Barra lateral izquierda (sidebar):**
- Ejemplos rápidos precargados para pruebas
- Botón para reiniciar el formulario
- Información sobre el sistema

**Área principal:**
- Barra de progreso con 4 pasos
- Formulario de entrada (columna izquierda)
- Panel de resultados (columna derecha)

### 2.2 Paso 1 — Seleccionar el tipo de documento

Haga clic en el tipo de documento que estaba enviando cuando ocurrió el error:

| Opción | Cuándo usarla |
|---|---|
| 📄 Factura electrónica | Cuando enviaba una factura de venta a la DIAN |
| 📝 Nota crédito | Cuando emitía una nota crédito sobre una factura |
| 🚛 Remesa | Cuando registraba una remesa de transporte en el RNDC |
| 📦 Manifiesto de carga | Cuando enviaba un manifiesto de carga al RNDC |

### 2.3 Paso 2 — Seleccionar el destino del envío

Marque hacia qué entidad se enviaba el documento:
- **🏛️ DIAN:** Para facturas electrónicas y notas crédito
- **🗂️ RNDC:** Para remesas y manifiestos de carga

> **Nota:** Es posible seleccionar ambos si el documento se envía a las dos entidades.

### 2.4 Paso 3 — Indicar los síntomas

Responda las preguntas sobre lo que observó durante el envío. Las preguntas se organizan en secciones:

#### 🌐 Conectividad e internet

| Pregunta | Respuesta esperada |
|---|---|
| ¿Tiene conexión a internet? | Marcado = SÍ tiene internet · Desmarcado = NO tiene |
| ¿Hubo error de conexión al servicio? | Marcar si el sistema mostró un mensaje de error de conexión |
| ¿El envío venció el tiempo de espera? | Marcar si el proceso no terminó y se cortó por timeout |
| ¿El RNDC respondió con falla SOAP? | Marcar si el mensaje de error menciona SOAP (solo RNDC) |

#### 📬 Estado del envío

| Pregunta | Respuesta esperada |
|---|---|
| ¿El servicio rechazó el documento? | Marcar si recibió un mensaje de rechazo explícito |
| ¿Este documento ya había sido enviado antes? | Marcar si el sistema indica que ya existe un registro previo |

#### 🔏 Certificado y numeración (solo facturas/notas crédito a DIAN)

| Pregunta | Respuesta esperada |
|---|---|
| ¿El certificado digital está vigente? | Marcado = vigente (normal) · Desmarcado = vencido o no instalado |
| ¿La resolución de numeración está vigente? | Marcado = vigente · Desmarcado = vencida (solo facturas) |
| ¿El número está en el rango autorizado? | Marcado = correcto · Desmarcado = fuera de rango (solo facturas) |

#### 👥 Datos de entidades

Seleccione en el menú desplegable **solamente** las entidades que tienen datos incorrectos o incompletos. Si todos los datos están bien, deje el campo vacío.

#### 🔧 Condiciones especiales

Aparece solo para combinaciones específicas. Complete según corresponda.

### 2.5 Ejecutar el diagnóstico

Haga clic en el botón azul **"🔍 Diagnosticar ahora"** para obtener el resultado.

### 2.6 Interpretar los resultados

El panel derecho mostrará:

**Banner de estado:**
- 🔴 Fondo rojo: se encontraron problemas
- 🟢 Fondo verde: el envío fue procesado correctamente
- ⚠️ Fondo gris: no hay información suficiente

**Métricas:**
- **Problemas:** número de errores detectados
- **Reglas disparadas:** cuántas reglas del sistema se activaron
- **Éxitos:** cuántos diagnósticos positivos se derivaron

**Tarjetas de diagnóstico:**  
Cada diagnóstico muestra:
- El nombre del problema detectado
- El porcentaje de certeza (ej. `98%`)
- La acción recomendada para resolver el problema (en azul)

**Botón ¿Por qué?:**  
Debajo de cada diagnóstico hay un botón expandible que muestra exactamente qué condiciones se evaluaron y cuál regla llevó a esa conclusión.

**Detalle técnico:**  
Al final hay una sección expandible con la lista completa de reglas que se activaron durante la inferencia.

---

## 3. Interpretación de resultados

### 3.1 Cómo leer los diagnósticos

| Diagnóstico | Qué significa | Qué hacer |
|---|---|---|
| **DianCaida** | El servicio DIAN no está disponible | Esperar y reintentar más tarde |
| **RndcCaida** | El servicio RNDC no está disponible | Contactar soporte o reintentar |
| **ErrorAPI** | Falla en la conexión con la API | Verificar configuración del conector |
| **ErrorCertificado** | Certificado digital vencido | Renovar certificado con la entidad certificadora |
| **ErrorResolucionNumeracion** | Resolución de numeración vencida | Gestionar renovación ante la DIAN |
| **ErrorNumeroFueraRango** | Número de documento fuera del rango | Revisar numeración en el sistema |
| **DocumentoYaProcesado** | Documento enviado anteriormente | No reenviar; verificar historial |
| **ProblemaInternet** | Sin conectividad a internet | Verificar red del equipo |
| **[Entidad]MalDiligenciado** | Datos incorrectos en la entidad | Corregir datos en el maestro del sistema |
| **EnvioExitosoRNDC** | Envío al RNDC exitoso | El documento fue aceptado |
| **CufeGenerado** | Factura procesada por la DIAN | El CUFE fue generado correctamente |

### 3.2 Qué hacer con las recomendaciones

Cada tarjeta de diagnóstico incluye una acción recomendada (en el cuadro azul con 💡). Siga esa recomendación y vuelva a intentar el envío.

Si el diagnóstico es **Sin diagnóstico concluyente**, significa que los síntomas ingresados no corresponden a ningún patrón conocido. En ese caso:
1. Verifique que respondió todas las preguntas correctamente.
2. Revise si omitió algún síntoma relevante.
3. Contacte al área de soporte técnico con el detalle del error que mostró el sistema.

### 3.3 Uso de los ejemplos rápidos

En la barra lateral hay 6 ejemplos precargados. Úselos para:
- **Entender cómo funciona el sistema** antes de ingresar un caso real.
- **Demostrar el sistema** a otras personas.
- **Verificar** que la aplicación está funcionando correctamente.

Para cargar un ejemplo haga clic en su nombre. El formulario se llenará automáticamente y podrá hacer clic en "Diagnosticar ahora" para ver el resultado.

Para limpiar el formulario y empezar de cero use el botón **"🔄 Reiniciar formulario"** en la barra lateral.
