# Análisis de calidad con SonarQube

El proyecto está configurado para analizarse con SonarQube de dos formas. Ambas
comparten la misma configuración (`sonar-project.properties`) y los mismos
reportes de cobertura.

| | Servidor local | SonarQube Cloud |
|---|---|---|
| Cuándo corre | Cuando lo lanzas a mano | Solo, en cada push y PR |
| Quién lo puede activar | Cualquiera del equipo | El dueño del repo en GitHub |
| Estado | Listo para usar | Falta el secreto `SONAR_TOKEN` |

---

## Opción A — Servidor local con Docker

### 1. Levantar SonarQube

**Antes que nada, revisa si ya tienes una instancia corriendo.** Una misma
instancia de SonarQube aloja varios proyectos, así que si la usas en otro ramo no
necesitas levantar una segunda:

```bash
docker ps --filter "publish=9000" --format "{{.Names}} {{.Image}} {{.Status}}"
```

Si aparece algo, sáltate este paso y anda directo al punto 2 usando esa
instancia. Si no aparece nada, con Docker Desktop abierto:

```bash
docker compose -f docker-compose.sonar.yml up -d
```

> Ese archivo es **solo** para el análisis de calidad; no tiene nada que ver con
> `docker-compose.yml`, que levanta la aplicación (Postgres + backend) y sí es
> parte del producto. SonarQube no se despliega al cliente.

La primera vez tarda 2-3 minutos. Cuando esté listo, entra a
<http://localhost:9000> con `admin` / `admin`; te va a pedir cambiar la clave.

Para confirmar que arrancó bien:

```bash
curl -s http://localhost:9000/api/system/status
```

Tiene que responder `"status":"UP"`.

### 2. Crear el proyecto y el token

En la interfaz web:

1. **Create project → Manually**
2. Project key: `HIN0_Guia_Digital_AdultoMayor` (tiene que coincidir con
   `sonar-project.properties`)
3. Elige **Locally** cuando pregunte cómo vas a analizar y genera un token.
   Cópialo: no se vuelve a mostrar.

### 3. Generar los reportes de cobertura

Sin esto, Sonar reporta 0% de cobertura.

```bash
cd backend && pytest tests/ --cov --cov-report=xml
```

```bash
cd frontend && npm run test:coverage
```

### 4. Preparar los reportes

```bash
python scripts/preparar_cobertura.py
```

**Este paso no es opcional.** Los dos reportes se generan desde su
subdirectorio, así que sus rutas son relativas a `backend/` y `frontend/`,
mientras que Sonar las resuelve desde la raíz del repositorio. Si te lo saltas,
el análisis corre sin errores pero reporta **0% de cobertura** — el síntoma más
confuso posible, porque parece que los tests no existieran.

El script corrige dos cosas:

- El `lcov.info` del frontend: agrega el prefijo `frontend/` y convierte las
  barras invertidas que Vitest escribe en Windows.
- El `coverage.xml` del backend: reemplaza el `<source>` absoluto de la máquina
  que lo generó (`C:\...\backend`) por la ruta relativa `backend`, que sí existe
  dentro del contenedor del scanner.

Es idempotente: puedes correrlo las veces que quieras.

### 5. Lanzar el análisis

Desde la raíz del repositorio, reemplazando `TU_TOKEN`:

```bash
docker run --rm -v "${PWD}:/usr/src" -e SONAR_HOST_URL=http://host.docker.internal:9000 -e SONAR_TOKEN=TU_TOKEN sonarsource/sonar-scanner-cli:5
```

Al terminar, los resultados quedan en <http://localhost:9000>.

> **Tarda entre 10 y 15 minutos.** No está colgado: el proyecto tiene archivos
> grandes (`lecciones/[leccion_id]/page.tsx` son casi 3.000 líneas) y SonarQube
> 9.9 no es rápido con ellos. Déjalo correr sin interrumpirlo. Si lo cancelas a
> medias queda un lock y el siguiente intento falla con *"Another SonarQube
> analysis is already in progress"*; en ese caso basta con esperar a que no
> quede ningún contenedor del scanner corriendo (`docker ps`) y reintentar.

> **Sobre la versión del scanner.** Está fijada en `:5` porque es la
> contemporánea de SonarQube 9.9 LTS. Los scanners más nuevos van dejando de
> soportar servidores antiguos. Si en el futuro actualizan el servidor, pueden
> sacar el `:5` y usar la etiqueta por defecto. Revisa qué versión corre tu
> servidor con:
>
> ```bash
> curl -s http://localhost:9000/api/server/version
> ```

> El scanner corre en un contenedor, así que no necesitas instalar Java ni el
> scanner CLI. `host.docker.internal` es la forma en que un contenedor alcanza
> un puerto del equipo anfitrión en Docker Desktop.

### Apagar el servidor

```bash
docker compose -f docker-compose.sonar.yml down
```

Los datos quedan guardados en volúmenes, así que el historial sobrevive.

---

## Opción B — SonarQube Cloud (CI)

El workflow ([`.github/workflows/ci.yml`](../.github/workflows/ci.yml)) ya tiene
el job `sonarqube`, que corre después de los tests, junta los dos reportes de
cobertura y ejecuta el análisis.

**Mientras no exista el secreto `SONAR_TOKEN`, el job pasa en verde y se salta el
análisis**, así que no rompe el CI.

Para activarlo, el dueño del repositorio en GitHub debe:

1. Entrar a <https://sonarcloud.io> con su cuenta de GitHub e importar el repo.
   Esto instala la GitHub App, y **solo puede hacerlo el dueño de la cuenta**:
   un colaborador no tiene permisos para instalar apps en un repo ajeno.
2. Verificar en **Information → Project Key** que el `projectKey` y la
   `organization` coincidan con `sonar-project.properties` y con el argumento
   `-Dsonar.organization` del workflow.
3. Generar un token en **My Account → Security** y guardarlo en GitHub como
   secreto de repositorio con el nombre exacto `SONAR_TOKEN`
   (*Settings → Secrets and variables → Actions*). Requiere permisos de admin
   sobre el repositorio.

---

## Problemas frecuentes

**El contenedor se reinicia solo o no arranca.** Suele ser Elasticsearch
quedándose sin memoria. SonarQube necesita ~2 GB de RAM disponibles; revisa que
Docker Desktop tenga suficiente asignada en *Settings → Resources*.

**El frontend aparece con 0% de cobertura.** Falta el paso 4, o el análisis se
corrió antes de generar los reportes.

**El backend aparece con 0% de cobertura.** El `coverage.xml` se genera dentro de
`backend/`; verifica que exista antes de lanzar el scanner.

**`Project not found` o error de autorización.** El `projectKey` del dashboard no
coincide con el de `sonar-project.properties`.

**`The container name "/sonarqube" is already in use`.** Ya tienes otra instancia
en la máquina. No la borres: úsala (ver paso 1), porque una misma instancia aloja
varios proyectos.

**`Not authorized` con el token en SonarQube 9.x.** Algunas versiones del scanner
esperan `SONAR_LOGIN` en vez de `SONAR_TOKEN`. Si falla la autenticación, prueba
cambiando esa variable en el comando del scanner.

---

## Qué se analiza y qué no

Las exclusiones están en `sonar-project.properties`. Se dejan fuera del análisis:

- `backend/venv/` y `node_modules/` — dependencias de terceros
- `backend/alembic/` — migraciones autogeneradas
- `backend/seed.py` — ~2.300 líneas de contenido educativo en literales, no
  lógica. Si algún día se le agrega lógica real, conviene sacarlo de las
  exclusiones.
- Los tests se declaran como tests (`sonar.tests`), no como código de producción,
  para que no inflen las métricas.
