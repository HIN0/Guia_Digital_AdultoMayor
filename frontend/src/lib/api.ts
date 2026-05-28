const API_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000/api'

// ── Tipos de respuesta del backend ──────────────────────────────────────────

export interface ModuloResumen {
  id: number
  nombre: string
  orden: number
  requiere_modulo_previo: boolean
}

export async function getModulos(): Promise<ModuloResumen[]> {
  const res = await fetch(`${API_URL}/educacion/modulos`)
  if (!res.ok) throw new Error('Error al cargar módulos')
  return res.json()
}


export interface LeccionResumen {
  id: number
  titulo: string
  orden: number
}

export interface OpcionQuizFinal {
  id: number
  texto: string
}

export interface PreguntaQuizFinal {
  id: number
  enunciado: string
  opciones: OpcionQuizFinal[]
}

export interface QuizFinal {
  id: number
  minimo_aciertos: number
  bloqueante: boolean
  preguntas: PreguntaQuizFinal[]
}

export interface ModuloDetalle {
  id: number
  nombre: string
  orden: number
  requiere_modulo_previo: boolean
  lecciones: LeccionResumen[]
  quiz_final: QuizFinal | null
}

// ── Tipos del contenido de una lección (campo JSON flexible) ────────────────

export interface Pagina {
  n: number
  tipo: string
  titulo: string
  texto: string
  apoyo_visual: string
}

export interface OpcionQuizCorto {
  texto: string
  correcta: boolean
}

export interface PreguntaQuizCorto {
  pregunta: string
  opciones: OpcionQuizCorto[]
  feedback: string
}

export interface QuizCorto {
  preguntas: PreguntaQuizCorto[]
  resultado: {
    umbral_aprobado: number
    titulo_aprobado: string
    mensaje_aprobado: string
    titulo_fallido: string
    mensaje_fallido: string
  }
}

export interface ContenidoLeccion {
  paginas: Pagina[]
  ejercicio?: Record<string, unknown>
  quiz_corto: QuizCorto
}

export interface LeccionDetalle {
  id: number
  titulo: string
  orden: number
  contenido: ContenidoLeccion
}

// ── Funciones de fetch ───────────────────────────────────────────────────────

export async function getModuloDetalle(id: number): Promise<ModuloDetalle> {
  const res = await fetch(`${API_URL}/educacion/modulos/${id}`)
  if (!res.ok) throw new Error('Error al cargar el módulo')
  return res.json()
}

export async function getLeccion(id: number): Promise<LeccionDetalle> {
  const res = await fetch(`${API_URL}/educacion/lecciones/${id}`)
  if (!res.ok) throw new Error('Error al cargar la lección')
  return res.json()
}

export async function completarLeccion(leccionId: number): Promise<void> {
  await fetch(`${API_URL}/progreso/leccion`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ leccion_id: leccionId }),
  })
}
