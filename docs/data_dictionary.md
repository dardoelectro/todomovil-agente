# Diccionario de Datos — TodoMovil Agente CRM

## Tabla: productos

| Campo | Tipo | Descripción | Ejemplo |
|-------|------|-------------|---------|
| id | VARCHAR(50) | Identificador único del producto | `crp239` |
| nombre | VARCHAR(200) | Nombre comercial | `CRP239` |
| marca | VARCHAR(100) | Fabricante | `Launch` |
| tipo | VARCHAR(50) | Tipo de herramienta: scanner, medicion, programacion, accesorio | `scanner` |
| gamma | VARCHAR(50) | Segmento: entrada, media, alta | `entrada` |
| precio_lista | FLOAT | Precio de lista en ARS | `450000` |
| sistemas_cobertura | JSONB | Lista de sistemas que cubre | `["Motor", "ABS", "SRS", "Transmisión"]` |
| funciones_especiales | JSONB | Lista de funciones especiales | `["Reset aceite", "EPB"]` |
| semaforo_default | VARCHAR(20) | Semáforo por defecto | `verde` |
| notas | TEXT | Notas adicionales | `Gama entrada. IMMO = AMARILLO.` |

## Tabla: compatibilidades

| Campo | Tipo | Descripción | Ejemplo |
|-------|------|-------------|---------|
| id | SERIAL | ID auto-incremental | `1` |
| producto_id | VARCHAR(50) | FK a productos | `crp239` |
| marca_vehiculo | VARCHAR(100) | Marca del vehículo | `Peugeot` |
| modelo_vehiculo | VARCHAR(100) | Modelo del vehículo | `208` |
| anio_inicio | INTEGER | Año inicio cobertura | `2013` |
| anio_fin | INTEGER | Año fin cobertura | `2025` |
| motor | VARCHAR(100) | Motorización | `1.6 VTi` |
| variante | VARCHAR(200) | Arquitectura eléctrica (VARIANTE) | `V1 ECU Bosch` |
| sistema | VARCHAR(100) | Sistema del vehículo | `Motor` |
| nivel_acceso | VARCHAR(50) | Nivel: lee_codigos, interactua, funciones_especiales | `interactua` |
| semaforo | VARCHAR(20) | verde, amarillo, rojo, no_aplica | `verde` |
| certezza | VARCHAR(20) | Alta, Media, Baja | `Alta` |
| tipo_fuente | VARCHAR(50) | oficial_fabricante, verificacion_manual, web_search, feedback_vendedor | `oficial_fabricante` |
| codigo_falla | VARCHAR(100) | Link a herramienta de medición | `P0171 → osciloscopio O2` |
| notas | TEXT | Notas adicionales | `Cobertura confirmada.` |
| chunk_id | VARCHAR(100) | Referencia al chunk en ChromaDB | `crp239_peugeot_208_motor` |

## Semáforo — Reglas de Negocio

| Color | Significado | Acción del vendedor |
|-------|------------|-------------------|
| 🟢 verde | Producto compatible, datos verificados | Ofrecer con confianza |
| 🟡 amarillo | Producto compatible con limitaciones | Ofrecer CON advertencia explícita |
| 🔴 rojo | Incompatibilidad confirmada | NO ofrecer para ese uso |
| ⚪ no_aplica | Fuera de cobertura de gama | Explicar que no es incompatibilidad, es fuera de alcance |

### IMMO = AMARILLO siempre
La función IMMO en TODOS los equipos no es confiable. Solo ofrecer con advertencia explícita.
DS900 tiene mejores resultados que MX900 y CRP239, pero sigue siendo AMARILLO.

### BSI fuera de cobertura = NO APLICA (no es ROJO)
Si un escáner de gama entrada no cubre BSI, es "no_aplica" — fuera de alcance del producto.
No es una incompatibilidad, es una limitación de gama.

## Certeza — Niveles

| Nivel | Criterio | tipo_fuente |
|-------|----------|------------|
| Alta | Datos de fabricante o verificación manual, todos los campos completos | oficial_fabricante, verificacion_manual |
| Media | Datos parciales, web search, o sin variante | web_search, sin variante |
| Baja | Sin datos, solo feedback de vendedor, o datos contradictorios | feedback_vendedor, sin datos |

## Capas RAG

| Capa | Fuente | Certeza máx | Citación |
|------|--------|------------|----------|
| 1 | Base curada (ChromaDB) | Alta | tipo_fuente + producto |
| 2 | Web search controlado | Media | URL siempre visible |
| 3 | LLM (solo forma, nunca contenido) | — | N/A |
