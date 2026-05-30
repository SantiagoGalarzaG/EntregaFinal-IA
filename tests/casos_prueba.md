# Casos de Prueba — Sistema de Diagnóstico DIAN / RNDC
**Autores:** Galarza, Solano — Fundación Universitaria Los Libertadores, 2026

---

## Tabla de validación

| # | Descripción | Hechos iniciales clave | Reglas disparadas | Conclusión esperada | Resultado obtenido | Estado |
|---|---|---|---|---|---|---|
| 1 | DIAN caída — factura correcta rechazada | Factura=Sí, DIAN, FacturableOk, CertVig, ResolVig, NumRango, Rechazado=Sí, SinError, Internet | R1a | DianCaida (90%) | DianCaida ✓ | ✅ |
| 2 | RNDC caído — manifiesto con falla SOAP | Manifiesto, RNDC, FallaSOAP=Sí, entidades OK | R2a | RndcCaida (98%) | RndcCaida ✓ | ✅ |
| 3 | Sin internet al enviar a DIAN | Factura, DIAN, Internet=No | R7a | ProblemaInternet (100%) | ProblemaInternet ✓ | ✅ |
| 4 | Tres errores DIAN simultáneos | Factura, DIAN, CertNoVig, ResolNoVig, NumFuera | R4a + R5a + R5b | ErrorCertificado + ErrorResolucionNumeracion + ErrorNumeroFueraRango | 3 diagnósticos ✓ | ✅ |
| 5 | Error de API — conexión falla con internet activo | Factura, DIAN, ErrorConexion=Sí, Internet=Sí, SinTimeout | R3a | ErrorAPI (90%) | ErrorAPI ✓ | ✅ |
| 6 | Documento duplicado — remesa ya enviada | Remesa, RNDC, Duplicado=Sí | R6 | DocumentoYaProcesado (100%) | DocumentoYaProcesado ✓ | ✅ |
| 7 | Tercero mal diligenciado en remesa | Remesa, RNDC, TerceroOk=No | R11a | TerceroMalDiligenciado (100%) | TerceroMalDiligenciado ✓ | ✅ |
| 8 | Manifiesto exitoso al RNDC | Manifiesto, RNDC, todas entidades OK, Internet, SinSOAP | R15 | EnvioExitosoRNDC (98%) | EnvioExitosoRNDC ✓ | ✅ |
| 9 | Factura exitosa a DIAN — XML tipo 10 | Factura, DIAN, CertVig, ResolVig, NumRango, FacturableOk | R16a → R17b | CufeGenerado + TipoXML10 | CufeGenerado + TipoXML10 ✓ | ✅ |
| 10 | Factura exitosa a DIAN — XML tipo 12 | Factura, DIAN, CertVig, ResolVig, NumRango, FacturableOk, Tipo12=Sí | R16a → R17a | CufeGenerado + TipoXML12 | CufeGenerado + TipoXML12 ✓ | ✅ |
| 11 | NC rechazada — factura ya aceptada | NotaCredito, DIAN, FacturaAceptada=Sí | R13b | ErrorFacturaYaAceptada (100%) | ErrorFacturaYaAceptada ✓ | ✅ |
| 12 | **Sin conclusión** — Factura→RNDC tipo 12 sin errores | Factura, RNDC, Internet, Tipo12=Sí, FacturableConsistente=Sí, SinFallaSOAP | Ninguna | Sin diagnóstico | Sin diagnóstico ✓ | ✅ |

---

## Notas de validación

### Caso 1 — Encadenamiento con diagnóstico conflictivo
También dispara R16a (CufeGenerado) porque todas las condiciones de éxito están presentes.  
El sistema detecta correctamente el conflicto `{DianCaida, CufeGenerado}` y lo reporta como advertencia.  
**Reglas adicionales:** R16a → R17b.

### Caso 4 — Múltiples diagnósticos simultáneos
Demuestra que el motor puede derivar varios diagnósticos en paralelo.  
Las tres reglas se aplican de forma independiente en distintas iteraciones del ciclo.

### Caso 9 y 10 — Encadenamiento en cadena
Demuestra inferencia en dos pasos: R16a genera `CufeGenerado`, y luego R17a o R17b usa ese resultado derivado como condición.

### Caso 12 — Sin conclusión (caso de borde)
Hechos exactos:
```
Factura=True, Documento=True, EnvioRNDC=True,
TieneInternet=True, FallaSOAP=False, DocumentoTipo12=True,
FacturableConsistente=True
```
- R14a requiere `DocumentoTipo12=False` → no cumple.  
- R14c requiere `FacturableConsistente=False` → no cumple.  
- R16a requiere `EnvioDian=True` → no está (solo RNDC).  
- R7b requiere `TieneInternet=False` → no cumple.  
**Resultado:** ninguna regla se dispara → sistema reporta "Sin diagnóstico concluyente".

---

## Cobertura de la base de conocimiento

| Grupo | Reglas | Casos que los ejercitan |
|---|---|---|
| A — Conectividad | R1a, R1b, R2a, R2b, R3a, R3b, R7a, R7b | 1, 2, 3, 5 |
| B — Certificado | R4a, R4b | 4 |
| C — Numeración | R5a, R5b | 4 |
| D — Duplicado | R6 | 6 |
| E — Entidades Manifiesto | R10a–R10e | 8 (exitoso, entidades OK) |
| F — Entidades Remesa | R11a–R11d | 7 |
| G — Factura DIAN | R12 | 9, 10 (FacturableOk=True) |
| H — NC DIAN | R13a, R13b | 11 |
| I — Factura/NC RNDC | R14a–R14d | 12 |
| J — Éxito | R15, R16a, R16b, R17a–R17d | 8, 9, 10 |
