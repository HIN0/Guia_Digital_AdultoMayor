# Backend — Guía Digital Adulto Mayor (FastAPI)

Guía completa para alguien que **nunca ha usado FastAPI**.

---

## 1. ¿En qué se diferencia de Spring Boot?

En Spring Boot, el framework te genera muchísimos archivos por defecto y la
estructura "mágica" (anotaciones, inyección automática, etc.). **FastAPI NO
hace nada de eso.** No genera archivos, no hay scaffolding. Tú creas cada
archivo a mano. La buena noticia: es mucho más simple y directo. Un archivo
Python es solo un archivo Python.

La equivalencia mental rápida:

| Spring Boot          | Aquí (FastAPI)         |
|----------------------|------------------------|
| `@RestController`    | `controller.py` (router) |
| `@Service`           | `service.py`           |
| `@Repository`        | `repository.py`        |
| `@Entity` (JPA)      | `entity.py` (SQLAlchemy) |
| DTO                  | `schema.py` (Pydantic) |
| `application.properties` | `.env` + `config.py` |

---

## 2. Las 5 capas de cada módulo (y qué hace cada una)

Cada carpeta dentro de `modules/` tiene los mismos 5 archivos. Esto es solo
una convención para mantener orden — FastAPI no la exige, pero ayuda mucho.
El flujo de una petición va de arriba hacia abajo:

```
Petición HTTP del frontend
        ↓
controller.py   → recibe la request, define la URL y el método (GET/POST)
        ↓
service.py      → la lógica de negocio (las reglas, los cálculos)
        ↓
repository.py   → habla con la base de datos (queries)
        ↓
entity.py       → define cómo es la tabla en PostgreSQL
```

Y aparte:

```
schema.py       → define la forma de los datos que entran y salen (JSON)
```

### Explicación archivo por archivo

- **`entity.py`** — Define las **tablas** de la base de datos como clases
  Python. Cada clase = una tabla. Cada `Column` = una columna. Esto es el
  equivalente a `@Entity` en JPA. SQLAlchemy las usa para crear las tablas y
  para mapear filas a objetos.

- **`schema.py`** — Define los **DTOs** con Pydantic. Son las "formas" del
  JSON. Hay schemas de entrada (`...Request`) que validan lo que manda el
  frontend, y schemas de salida (`...Response`) que controlan qué devolvemos.
  **Importante:** nunca devolvemos la entidad directamente; usamos un schema
  para no exponer campos sensibles (ej: en el quiz no mandamos `es_correcta`).

- **`repository.py`** — Solo consultas a la base de datos. Funciones tipo
  `buscar_usuario`, `crear_leccion`, etc. Nada de lógica de negocio aquí,
  solo `db.query(...)`.

- **`service.py`** — La lógica de negocio. Aquí van las reglas: "el módulo 3
  se desbloquea si aprobaste el quiz del módulo 1", "el quiz se aprueba con X
  aciertos", etc. El service llama al repository.

- **`controller.py`** — Define los **endpoints** (las URLs). Recibe la
  petición, llama al service y devuelve la respuesta. Aquí vive el `router`.

---

## 3. La carpeta `core/`

Cosas compartidas por todos los módulos:

- **`config.py`** — Lee las variables del archivo `.env` (URL de la base de
  datos, claves secretas, etc.). Equivale a `application.properties`.

- **`database.py`** — Crea la conexión a PostgreSQL y la función `get_db()`
  que entrega una sesión de base de datos a cada endpoint.

- **`security.py`** — Verifica el token de Google y genera/valida los JWT
  (los tokens que tu propio backend usa para saber quién está logueado).

- **`dependencies.py`** — Funciones reutilizables como `get_usuario_actual`
  (saca el usuario del token) y `requiere_admin` (exige rol admin).

---

## 4. Conceptos clave de FastAPI que verás en el código

### `Depends()` — Inyección de dependencias
Es lo más "raro" al principio. Cuando un endpoint escribe:

```python
def mi_endpoint(db: Session = Depends(get_db)):
```

FastAPI **ejecuta `get_db()` automáticamente** antes de tu función y te pasa
el resultado. Es como la inyección de dependencias de Spring, pero explícita.
Lo usamos para la base de datos y para sacar el usuario del token.

### `response_model`
```python
@router.get("/modulos", response_model=list[ModuloResponse])
```
Le dice a FastAPI: "filtra la respuesta para que tenga exactamente esta
forma". Si tu objeto tiene campos de más, los recorta. Esto da seguridad.

### `router`
Cada `controller.py` crea un `APIRouter`. Es un grupo de endpoints. Luego
`main.py` los junta todos. Equivale a tener varios `@RestController`.

---

## 5. Cómo levantar el proyecto (paso a paso)

### Paso 1 — Instala Python 3.11+ y crea un entorno virtual
Dentro de la carpeta `backend/`:

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

(El `venv` es como un contenedor aislado de librerías, para no ensuciar tu
Python global. Verás `(venv)` al inicio de tu terminal cuando esté activo.)

### Paso 2 — Instala las dependencias
```bash
pip install -r requirements.txt
```

### Paso 3 — Crea tu archivo `.env`
Copia `.env.example` a `.env` y rellena los valores reales:

```bash
# Windows:
copy .env.example .env
# Mac/Linux:
cp .env.example .env
```

Mínimo necesitas la `DATABASE_URL` apuntando a tu PostgreSQL. Ejemplo:
```
DATABASE_URL=postgresql://postgres:miclave@localhost:5432/guia_digital
```

### Paso 4 — Ten PostgreSQL corriendo
Instala PostgreSQL y crea una base de datos vacía llamada `guia_digital`
(o el nombre que pusiste en la URL). Las **tablas se crean solas** la primera
vez que levantes el servidor (gracias a `Base.metadata.create_all` en main.py).

### Paso 5 — Levanta el servidor
```bash
uvicorn main:app --reload
```

`uvicorn` es el servidor. `main:app` significa "el objeto `app` dentro de
`main.py`". `--reload` reinicia solo cuando guardas cambios.

### Paso 6 — Abre la documentación automática
Ve a tu navegador:
```
http://localhost:8000/docs
```

**Esto es lo más mágico de FastAPI:** te genera una página interactiva con
TODOS tus endpoints, donde puedes probarlos sin escribir código. Ahí ves cada
ruta, qué recibe y qué devuelve.

---

## 6. Orden recomendado para desarrollar (según tus Sprints)

- **Sprint 1:** `auth/` (login) + `educacion/` (módulos y lecciones, parte GET)
- **Sprint 2:** `progreso/` (guardar avance, quizzes, insignias)
- **Sprint 3:** `chatbot/` (lista blanca + fallback) + `admin/` (CRUD)

El módulo `chatbot/` y `admin/` ya están esqueletados pero los terminas en
Sprint 3.

---

## 7. Estructura final de archivos

```
backend/
├── main.py              ← punto de entrada, junta todo
├── requirements.txt     ← dependencias
├── .env.example         ← plantilla de variables (copia a .env)
│
├── core/
│   ├── config.py        ← lee el .env
│   ├── database.py      ← conexión PostgreSQL + get_db()
│   ├── security.py      ← token Google + JWT
│   └── dependencies.py  ← get_usuario_actual, requiere_admin
│
└── modules/
    ├── auth/            ← login con Google (Sprint 1)
    ├── educacion/       ← módulos, lecciones, quizzes (Sprint 1-2)
    ├── progreso/        ← avance e insignias (Sprint 2)
    ├── chatbot/         ← asistente lista blanca (Sprint 3)
    └── admin/           ← CRUD de contenido (Sprint 3)
        (cada uno con: controller.py, service.py,
         repository.py, entity.py, schema.py)
```

---

## 8. Una cosa importante sobre las tablas

Ahora mismo `main.py` usa `Base.metadata.create_all(bind=engine)`, que crea
las tablas automáticamente. Está bien para empezar y desarrollar rápido.
**Más adelante** (cuando cambies columnas), conviene usar **Alembic**
(migraciones) — ya está en el `requirements.txt`. Pero no te preocupes por eso
hasta que lo necesites; para Sprint 1 lo automático sobra.
