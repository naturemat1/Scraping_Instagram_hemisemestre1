# Instagram Followers Scraper

Este proyecto utiliza Python y [Selenium](http://www.seleniumhq.org/) para scrapear seguidores, seguidos, biografía y descripción de cuentas de Instagram, enfocándose en la cuenta @nayeli.nxx. Incluye análisis de patrones y estrategias para un scraping eficiente y robusto.

## Tabla de Contenidos

- [Respuestas a Preguntas Clave](#respuestas-a-preguntas-clave)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Estrategia de Desarrollo](#estrategia-de-desarrollo)
- [TODO](#todo)

## Respuestas a Preguntas Clave

### 1. Scrapear con los métodos revisados los seguidores de la cuenta @nayeli.nxx

Para scrapear los seguidores de @nayeli.nxx, el proyecto utiliza Selenium WebDriver para automatizar la navegación en Instagram. Los pasos incluyen:

- Crear un entorno virtual y activarlo.
- Instalar dependencias con `pip install -r requirements.txt`.
- Colocar cookies válidas de sesión en `cookies.json` (formato: `{"sessionid": "valor", "csrftoken": "valor"}`).
- Ejecutar `python main.py`.
- Ingresar `nayeli.nxx` como usuario objetivo.
- El script navega al perfil, abre el diálogo de seguidores, realiza scroll automático para cargar todos los usuarios, y extrae la lista completa.
- Maneja inactividad y límites para evitar bucles infinitos.

### 2. Recuperar: Seguidores, Seguidos, Biografía, Description

El script recupera:
- **Seguidores**: Número de seguidores del perfil objetivo (extraído de enlaces con `href='/followers'`).
- **Seguidos**: Número de seguidos (extraído de enlaces con `href='/following'`).
- **Biografía**: Texto de la biografía del perfil (usando XPath para elementos de biografía).
- **Descripción**: Meta descripción de la página (atributo `content` de `<meta name='description'>`).

Estos datos se muestran en consola y se guardan en `nayeli.nxx_profile.json`. Además, se genera una lista de seguidores en `nayeli.nxx_followers.xlsx` y opcionalmente seguidos en `nayeli.nxx_following.xlsx`.

### 3. Que estrategia realizaría en la creación de su software en base a los patrones encontrados

Basado en patrones de Instagram (XPath dinámicos, diálogos emergentes, scroll infinito, detección anti-bot), la estrategia incluye:

- **Uso de Selenium**: Para contenido dinámico, con WebDriverWait para estabilidad.
- **Manejo de Sesiones**: Priorizar cookies sobre login manual para evitar bloqueos.
- **Scroll Inteligente**: Detectar fin de lista por inactividad, con límites de seguridad.
- **Modularización**: Clases separadas (Scraper, utils) para mantenibilidad.
- **Anti-Detección**: Ocultar webdriver, delays aleatorios, headers realistas.
- **Manejo de Errores**: Excepciones para elementos faltantes, reintentos.
- **Exportación Estructurada**: Usar pandas para Excel con encabezados, JSON para metadatos.
- **Optimización**: Evitar sobrecarga visitando perfiles solo cuando necesario.

## Requisitos

- Python 3.7+ instalado.
- PIP para instalar dependencias.
- Google Chrome instalado (Selenium usa `chromedriver.exe` en `drivers/`).
- Cookies válidas de Instagram en `cookies.json` (exportadas de navegador para evitar login manual).

## Instalación

1. Clona o descarga el repositorio:
   ```bash
   git clone https://github.com/tu-repo/instagram-followers-scraper.git
   cd instagram-followers-scraper
   ```

2. Crea un entorno virtual:
   ```bash
   python -m venv venv
   ```

3. Activa el entorno:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. Coloca tus cookies en `cookies.json` (ejemplo: `{"sessionid": "abc123", "csrftoken": "def456"}`).

2. Ejecuta el script:
   ```bash
   python main.py
   ```

3. Ingresa `nayeli.nxx` como usuario objetivo.

4. Si las cookies fallan, proporciona usuario y contraseña de Instagram.

5. El script mostrará info del perfil y guardará archivos en el directorio raíz.

## Estrategia de Desarrollo

El software se basa en patrones de Instagram para scraping eficiente:
- Navegación programática con Selenium.
- Extracción de datos con XPath y regex.
- Scroll automático con detección de cambios.
- Evitación de detección mediante stealth techniques.
- Modularidad para extensiones futuras (e.g., análisis de Benford).

## TODO

- Optimizar velocidad de scraping (actualmente lento por delays necesarios).
- Mejorar manejo de credenciales inválidas.
- Agregar proxy support para mayor robustez.
- Implementar análisis de patrones en listas (e.g., detección de bots).

[![Run on Repl.it](https://repl.it/badge/github/tonoli/instagram-followers-scraper)](https://repl.it/github/tonoli/instagram-followers-scraper)