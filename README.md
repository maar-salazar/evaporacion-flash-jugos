# Simulación de Proceso de Concentración de Jugos por Evaporación Flash a baja presion (Doble efecto)

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![SciPy](https://img.shields.io/badge/SciPy-8CAAE6?style=for-the-badge&logo=scipy&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly&logoColor=white)

> Aplicación web interactiva para el modelado termodinámico y análisis financiero de un proceso de concentración de jugos mediante evaporación flash de doble efecto a baja presión.

---

## Descripción del Proyecto

Este simulador resuelve los balances de materia y energía iterativos para un sistema de separación de fases. El motor termodinámico considera la mezcla de agua-sacarosa como una solución no ideal, asumiendo la calibración de la **Elevación del Punto de Ebullición (BPE)** bajo el modelo NRTL (Non-Random Two-Liquid).

La herramienta no solo se enfoca en las variables operativas, sino que integra un módulo de análisis económico para calcular la rentabilidad operativa del diseño de planta (VPN, Payback y ROI) en tiempo real, facilitando la toma de decisiones basada en datos.

##  Características Principales

* **Resolución Numérica:** Empleo de algoritmos de búsqueda de raíces para el cálculo riguroso del equilibrio de fases en válvulas isentálpicas.
* **Análisis de Sensibilidad:** Visualización dinámica e interactiva del impacto de las caídas de presión y temperaturas de precalentamiento sobre la concentración final (°Brix).
* **Viabilidad Económica:** Tablero interactivo que evalúa costos de insumos industriales (vapor, electricidad, agua de enfriamiento) frente a la producción proyectada.
* **Tutor IA Integrado:** Conexión con modelos de lenguaje para proveer asistencia técnica instantánea sobre los diagramas y resultados del proceso.

---

## Tecnologías y Estructura

La arquitectura del proyecto separa la lógica de la interfaz gráfica del motor de cálculo para mantener un código escalable y ordenado.

* `app.py`: Renderizado web y UI (Streamlit).
* `modelo.py`: Motor de cálculo termodinámico y balances financieros.
* `flash.py`: Desarrollo algorítmico paso a paso.

---

## Instalación y Uso

Sigue estos pasos para desplegar el simulador en un entorno local:

1. **Clona este repositorio:**
   ```bash
   git clone [https://github.com/maar-salazar/evaporacion-flash-jugos.git](https://github.com/maar-salazar/evaporacion-flash-jugos.git)
   cd evaporacion-flash-jugos
