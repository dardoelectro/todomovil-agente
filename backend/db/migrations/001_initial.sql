-- ══════════════════════════════════════════════════════════
-- TodoMovil Agente CRM — Migración inicial
-- Crea tablas y carga datos demo
-- ══════════════════════════════════════════════════════════

-- ── Productos ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS productos (
    id VARCHAR(50) PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    marca VARCHAR(100) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    gamma VARCHAR(50),
    precio_lista FLOAT,
    sistemas_cobertura JSONB DEFAULT '[]',
    funciones_especiales JSONB DEFAULT '[]',
    semaforo_default VARCHAR(20) DEFAULT 'verde',
    notas TEXT,
    fecha_actualizacion TIMESTAMP DEFAULT NOW()
);

-- ── Compatibilidades ─────────────────────────────────────
CREATE TABLE IF NOT EXISTS compatibilidades (
    id SERIAL PRIMARY KEY,
    producto_id VARCHAR(50) NOT NULL REFERENCES productos(id),
    marca_vehiculo VARCHAR(100) NOT NULL,
    modelo_vehiculo VARCHAR(100) NOT NULL,
    anio_inicio INTEGER,
    anio_fin INTEGER,
    motor VARCHAR(100),
    variante VARCHAR(200),
    sistema VARCHAR(100) NOT NULL,
    nivel_acceso VARCHAR(50) NOT NULL,
    semaforo VARCHAR(20) NOT NULL,
    certezza VARCHAR(20) NOT NULL,
    tipo_fuente VARCHAR(50) NOT NULL DEFAULT 'oficial_fabricante',
    codigo_falla VARCHAR(100),
    notas TEXT,
    chunk_id VARCHAR(100)
);

-- ── Vendedores ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS vendedores (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    nombre VARCHAR(200) NOT NULL,
    password_hash VARCHAR(500) NOT NULL,
    rol VARCHAR(50) DEFAULT 'vendedor',
    activo INTEGER DEFAULT 1
);

-- ── Conversaciones ───────────────────────────────────────
CREATE TABLE IF NOT EXISTS conversaciones (
    id SERIAL PRIMARY KEY,
    vendedor_id INTEGER REFERENCES vendedores(id),
    pregunta TEXT NOT NULL,
    respuesta TEXT,
    semaforo VARCHAR(20),
    certezza VARCHAR(20),
    capa_utilizada VARCHAR(50),
    fuentes JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ── Índices ──────────────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_compat_producto ON compatibilidades(producto_id);
CREATE INDEX IF NOT EXISTS idx_compat_marca_modelo ON compatibilidades(marca_vehiculo, modelo_vehiculo);
CREATE INDEX IF NOT EXISTS idx_compat_sistema ON compatibilidades(sistema);
CREATE INDEX IF NOT EXISTS idx_compat_semaforo ON compatibilidades(semaforo);
CREATE INDEX IF NOT EXISTS idx_conv_vendedor ON conversaciones(vendedor_id);
CREATE INDEX IF NOT EXISTS idx_conv_fecha ON conversaciones(created_at);

-- ── Datos demo: 4 escáneres ──────────────────────────────
INSERT INTO productos (id, nombre, marca, tipo, gamma, precio_lista, sistemas_cobertura, funciones_especiales, semaforo_default, notas) VALUES
('crp239', 'CRP239', 'Launch', 'scanner', 'entrada', 450000,
 '["Motor", "Transmisión", "ABS", "SRS"]'::jsonb,
 '["Reset aceite", "Reset frenos", "Batería register"]'::jsonb,
 'verde',
 'Gama entrada. No cubre BSI/Abs windows. IMMO = AMARILLO. 4 sistemas principales.'),

('topscan_pro', 'TopScan Pro', 'TopDon', 'scanner', 'entrada', 350000,
 '["Motor", "ABS", "SRS", "Transmisión"]'::jsonb,
 '["Reset aceite", "EPB reset"]'::jsonb,
 'verde',
 'Gama entrada económica. Funciones especiales limitadas. Opción más accesible.'),

('mx900', 'MaxiDiag MX900', 'Autel', 'scanner', 'media', 650000,
 '["Motor", "Transmisión", "ABS", "SRS", "Dirección", "Carrocería", "Chasis"]'::jsonb,
 '["Reset aceite", "EPB", "SAS", "DPF", "IMMO", "BMS", "TPMS"]'::jsonb,
 'verde',
 'Gama media. IMMO = AMARILLO (no confiable en todas las marcas). Más sistemas y funciones que gama entrada.'),

('ds900', 'MaxiDAS DS900', 'Autel', 'scanner', 'alta', 1200000,
 '["Motor", "Transmisión", "ABS", "SRS", "Dirección", "Carrocería", "Chasis", "Confort", "BSI", "Infotainment"]'::jsonb,
 '["Bi-direccional", "Coding", "Adaptaciones", "IMMO", "EPB", "SAS", "DPF", "BMS", "TPMS", "Injector coding"]'::jsonb,
 'verde',
 'Gama alta. Bi-direccional. IMMO = AMARILLO. BSI coverage amplio. Máxima cobertura.');

-- ── Vendedores demo ──────────────────────────────────────
INSERT INTO vendedores (username, nombre, password_hash, rol) VALUES
('vendedor1', 'Vendedor Demo', 'demo_hash_1', 'vendedor'),
('admin', 'Administrador', 'demo_hash_admin', 'admin'),
('ezequiel', 'Ezequiel', 'demo_hash_eze', 'vendedor_avanzado'),
('mauro', 'Mauro', 'demo_hash_mau', 'vendedor_avanzado');
