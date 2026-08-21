# 🛒 RetailStock Control: Sistema de Gestión de Inventario para Retail
**Escuela Bancaria y Comercial (EBC) - Campus Toluca**  
**Asignatura:** Aplicaciones Web II  
**Proyecto Final - Fase 2: Diseño**

---

## 👥 Integrantes del Equipo
* Estefania Moncada Cabrera
* Sergio Alberto Salcedo Parra
* **Docente:** Ph.D. Yuritsa Páez

---

## 📋 Descripción del Proyecto
Este proyecto consiste en el diseño y desarrollo de una aplicación web corporativa basada en la arquitectura MVT y el framework Django. Su objetivo principal es solucionar el control inadecuado de niveles de inventario en el sector retail, mitigando desabastos y mermas a través de un monitoreo automatizado de existencias críticas.

### 🧩 Componente Reutilizable e Integrado
*   **Capa Intermedia de Persistencia (Patrón DAO):** Módulo centralizado y reutilizable (`articulos/dao/inventariodao.py`) diseñado para aislar las consultas y escrituras SQL del motor de datos de la interfaz de usuario, garantizando un código mantenible y escalable.

---

## 🏗️ Estructura de la Arquitectura (Django)
El proyecto está organizado de la siguiente manera:

*   `inventarioretail/`: Núcleo de configuración global del servidor web (URLs, Settings, WSGI/ASGI).
*   `articulos/`: Aplicación operativa del sistema (Modelos de retail, vistas lógicas de control y formularios).
*   `articulos/templates/mainvista/`: Pantallas de interfaz de usuario optimizadas para computadoras de escritorio.

---

## ⚙️ Stack Tecnológico Utilizado
*   **Framework Principal:** Django (Python v3.x)
*   **Base de Datos Relacional:** SQLite (`db.sqlite3`)
*   **Motor de Interfaces / Estilos:** HTML5, CSS Nativos y componentes estilizados de alta velocidad.

---

## 🚀 Próximos Pasos (Fase 3)
*   Implementación completa de relaciones entre entidades (Categorías, Productos, Proveedores).
*   Inyección de datos dinámicos mediante formularios CRUD hacia la base de datos relacional local.
