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
  lista_sintomas?: string[]
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

export interface ItemEjercicio {
  situacion?: string
  frase?: string
  caso?: string
  fuente?: string
  pregunta?: string
  patologia?: string
  respuesta?: string
  respuesta_ia?: string
  etiqueta?: string
  motivo?: string
  opciones?: string[]
  mejor?: string
  util?: boolean
}

export interface Ejercicio {
  tipo: string
  instruccion: string
  items: ItemEjercicio[]
  situacion_ejemplo?: string
}

export interface ContenidoLeccion {
  paginas: Pagina[]
  ejercicio?: Ejercicio
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

export interface InsigniaOtorgada {
  id: number
  nombre: string
  descripcion: string
  icono_url: string
}

export interface LeccionCompletadaResponse {
  leccion_id: number
  completada: boolean
  insignia_otorgada: InsigniaOtorgada | null
}

export async function completarLeccion(leccionId: number, token?: string): Promise<LeccionCompletadaResponse> {
  const headers: Record<string, string> = { 'Content-Type': 'application/json' }
  if (token) headers['Authorization'] = `Bearer ${token}`
  const res = await fetch(`${API_URL}/progreso/leccion`, {
    method: 'POST',
    headers,
    body: JSON.stringify({ leccion_id: leccionId }),
  })
  if (!res.ok) return { leccion_id: leccionId, completada: false, insignia_otorgada: null }
  return res.json()
}

export interface RespuestaItem {
  pregunta_id: number
  opcion_id: number
}

export interface FeedbackPregunta {
  pregunta_id: number
  opcion_correcta_id: number
  opcion_seleccionada_id: number
  es_correcta: boolean
  feedback: string
}

export interface ResultadoQuiz {
  puntaje: number
  minimo_aciertos: number
  aprobado: boolean
  feedbacks: FeedbackPregunta[]
  insignia_otorgada: InsigniaOtorgada | null
}

export async function submitQuizFinal(quizId: number, respuestas: RespuestaItem[], token?: string): Promise<ResultadoQuiz> {
  const headers: Record<string, string> = { 'Content-Type': 'application/json' }
  if (token) headers['Authorization'] = `Bearer ${token}`
  const res = await fetch(`${API_URL}/progreso/quiz`, {
    method: 'POST',
    headers,
    body: JSON.stringify({ quiz_id: quizId, respuestas }),
  })
  if (!res.ok) throw new Error('Error al enviar el quiz')
  return res.json()
}

// ── Progreso del usuario ────────────────────────────────────────────────────

export interface EstadoModuloBack {
  modulo_id: number
  orden: number
  desbloqueado: boolean
  completado: boolean
  lecciones_completadas: number[]
}

export interface ResumenProgreso {
  lecciones_completadas: number[]
  quizzes_aprobados: number[]
  insignias: InsigniaOtorgada[]
  modulos: EstadoModuloBack[]
  chatbot_desbloqueado: boolean
}

export async function getProgreso(token?: string): Promise<ResumenProgreso | null> {
  const headers: Record<string, string> = {}
  if (token) headers['Authorization'] = `Bearer ${token}`
  try {
    const res = await fetch(`${API_URL}/progreso/`, { headers })
    if (!res.ok) return null
    return res.json()
  } catch {
    return null
  }
}


/**
 * Sincroniza localStorage con los datos reales del backend.
 * Sobreescribe las keys de progreso para eliminar datos obsoletos.
 */
export function sincronizarLocalStorage(progreso: ResumenProgreso, moduloIds: number[]) {
  for (const estado of progreso.modulos) {
    const key = `huap_mod${estado.modulo_id}_lecciones_completadas`
    localStorage.setItem(key, JSON.stringify(estado.lecciones_completadas))

    if (estado.orden === 1) {
      if (estado.completado) localStorage.setItem("huap_mod1_completado", "true")
      else localStorage.removeItem("huap_mod1_completado")
    }
    if (estado.orden === 2) {
      if (estado.completado) localStorage.setItem("huap_mod2_completado", "true")
      else localStorage.removeItem("huap_mod2_completado")
    }
  }

  if (progreso.chatbot_desbloqueado) localStorage.setItem("huap_chatbot_desbloqueado", "true")
  else localStorage.removeItem("huap_chatbot_desbloqueado")

  // Limpiar keys de módulos que no vinieron del backend
  for (const id of moduloIds) {
    if (!progreso.modulos.find(e => e.modulo_id === id)) {
      localStorage.removeItem(`huap_mod${id}_lecciones_completadas`)
    }
  }
}


// ── Chatbot ──────────────────────────────────────────────────────────────────

export interface ChatResponse {
  respuesta: string
  conversacion_id: number
  mensaje_id: number
}

export async function preguntarChatbot(
  pregunta: string,
  conversacion_id: number | null,
  token: string,
): Promise<ChatResponse> {
  const res = await fetch(`${API_URL}/chatbot/preguntar`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ pregunta, conversacion_id }),
  })
  if (!res.ok) throw new Error('Error al procesar la pregunta')
  return res.json()
}

export async function valorarMensaje(
  mensaje_id: number,
  valoracion: 'positiva' | 'negativa',
  token: string,
): Promise<void> {
  await fetch(`${API_URL}/chatbot/valorar`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ mensaje_id, valoracion }),
  })
}

export interface ConversacionOut {
  id: number
  fecha_inicio: string
  preview: string
  total_mensajes: number
}

export interface MensajeOut {
  id: number
  tipo: string
  contenido: string
  valoracion: string | null
  fecha: string
}

export async function listarConversaciones(token: string): Promise<ConversacionOut[]> {
  const res = await fetch(`${API_URL}/chatbot/conversaciones`, {
    headers: { Authorization: `Bearer ${token}` },
  })
  if (!res.ok) throw new Error('Error al cargar conversaciones')
  return res.json()
}

export async function obtenerMensajesConversacion(id: number, token: string): Promise<MensajeOut[]> {
  const res = await fetch(`${API_URL}/chatbot/conversaciones/${id}/mensajes`, {
    headers: { Authorization: `Bearer ${token}` },
  })
  if (!res.ok) throw new Error('Error al cargar mensajes')
  return res.json()
}


// ── Admin — Patologías ────────────────────────────────────────────────────────

export interface PatologiaOut {
  id: number
  nombre: string
  validada: boolean
}

export async function adminListarPatologias(token: string): Promise<PatologiaOut[]> {
  const res = await fetch(`${API_URL}/chatbot/admin/patologias`, {
    headers: { Authorization: `Bearer ${token}` },
  })
  if (!res.ok) throw new Error('Error al cargar patologías')
  return res.json()
}

export async function adminCrearPatologia(nombre: string, token: string): Promise<PatologiaOut> {
  const res = await fetch(`${API_URL}/chatbot/admin/patologias`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify({ nombre }),
  })
  if (!res.ok) throw new Error('Error al crear patología')
  return res.json()
}


// ── Admin — Preguntas validadas (whitelist) ───────────────────────────────────

export interface PreguntaChatbotOut {
  id: number
  patologia_id: number
  texto_pregunta: string
  respuesta_validada: string
  variantes: string[]
  activa: boolean
}

export interface PreguntaChatbotCreate {
  patologia_id: number
  texto_pregunta: string
  respuesta_validada: string
  variantes?: string[]
}

export interface PreguntaChatbotUpdate {
  texto_pregunta?: string
  respuesta_validada?: string
  variantes?: string[]
  activa?: boolean
}

export async function adminListarPreguntas(token: string): Promise<PreguntaChatbotOut[]> {
  const res = await fetch(`${API_URL}/chatbot/admin/preguntas`, {
    headers: { Authorization: `Bearer ${token}` },
  })
  if (!res.ok) throw new Error('Error al cargar preguntas')
  return res.json()
}

export async function adminCrearPregunta(
  data: PreguntaChatbotCreate,
  token: string,
): Promise<PreguntaChatbotOut> {
  const res = await fetch(`${API_URL}/chatbot/admin/preguntas`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify(data),
  })
  if (!res.ok) throw new Error('Error al crear pregunta')
  return res.json()
}

export async function adminActualizarPregunta(
  id: number,
  data: PreguntaChatbotUpdate,
  token: string,
): Promise<PreguntaChatbotOut> {
  const res = await fetch(`${API_URL}/chatbot/admin/preguntas/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify(data),
  })
  if (!res.ok) throw new Error('Error al actualizar pregunta')
  return res.json()
}

export async function adminEliminarPregunta(id: number, token: string): Promise<void> {
  const res = await fetch(`${API_URL}/chatbot/admin/preguntas/${id}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}` },
  })
  if (!res.ok) throw new Error('Error al eliminar pregunta')
}

export async function adminRecargarWhitelist(token: string): Promise<void> {
  const res = await fetch(`${API_URL}/chatbot/admin/recargar-whitelist`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` },
  })
  if (!res.ok) throw new Error('Error al recargar whitelist')
}
