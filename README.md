# ?? Proyecto Integrador: Infraestructura Big Data - Logística

## ?? Autor
**Margot Huaman Quispe**

## ?? Descripción del Proyecto
Este repositorio contiene el diseño y la implementación de una base de datos relacional robusta para la gestión de una flota logística masiva. El objetivo principal fue demostrar la capacidad de procesar y cargar grandes volúmenes de datos (**Big Data**) utilizando un pipeline de ETL en Python.

## ?? Hitos de Carga (Medio Millón de Registros)
Se realizó la carga exitosa de **505,000 registros** verificados en PostgreSQL:
* **Viajes (Trips):** 100,000 registros.
* **Entregas (Deliveries):** 400,000 registros.
* **Mantenimiento (Maintenance):** 5,000 registros.
* **Tablas Maestras:** Conductores, Vehículos y Rutas.

## ??? Tecnologías y Herramientas
* **Base de Datos:** PostgreSQL 15.
* **Lenguaje:** Python 3.14.
* **Librerías ETL:** psycopg2 para conexión y Faker para generación de datos sintéticos.
* **Entorno:** Virtualización con fleet_env.
* **Control de Versiones:** Git y GitHub.

## ?? Proceso de Implementación (Paso a Paso)
1. **Modelado:** Diseño de esquemas relacionales con integridad referencial (Foreign Keys).
2. **Entorno:** Configuración de entorno virtual y gestión de dependencias.
3. **ETL:** Desarrollo de scripts en Python para la limpieza e inserción masiva.
4. **Validación:** Control de calidad mediante consultas de agregación en pgAdmin.
5. **Versionamiento:** Gestión de ciclo de vida del código con Git.

---
*Misión cumplida: Datos listos para la fase de análisis.* ?
