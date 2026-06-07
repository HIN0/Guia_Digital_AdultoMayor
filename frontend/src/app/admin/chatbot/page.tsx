"use client"

import { useState, useEffect, useCallback } from "react"
import { useSession } from "next-auth/react"
import { useRouter } from "next/navigation"
import {
  adminListarPatologias,
  adminListarPreguntas,
  adminCrearPatologia,
  adminCrearPregunta,
  adminActualizarPregunta,
  adminEliminarPregunta,
  adminRecargarWhitelist,
  type PatologiaOut,
  type PreguntaChatbotOut,
} from "@/lib/api"
import { RefreshCw, Plus, Pencil, Trash2, Check, X, ChevronDown, ChevronUp } from "lucide-react"

// ── Helpers de estilo ─────────────────────────────────────────────────────────

const card = {
  backgroundColor: "white",
  borderRadius: "14px",
  boxShadow: "0 1px 6px rgba(0,0,0,0.08)",
  padding: "18px",
  marginBottom: "12px",
}

const inputStyle: React.CSSProperties = {
  width: "100%",
  border: "1.5px solid #D1D5DB",
  borderRadius: "10px",
  padding: "10px 14px",
  fontSize: "0.95rem",
  fontFamily: "inherit",
  outline: "none",
  backgroundColor: "#fafafa",
  color: "var(--huap-texto)",
  boxSizing: "border-box",
}

const btnPrimary: React.CSSProperties = {
  backgroundColor: "var(--huap-azul)",
  color: "white",
  border: "none",
  borderRadius: "10px",
  padding: "10px 20px",
  fontWeight: 600,
  fontSize: "0.95rem",
  cursor: "pointer",
  display: "flex",
  alignItems: "center",
  gap: "6px",
}

const btnDanger: React.CSSProperties = {
  backgroundColor: "#FFEBEE",
  color: "var(--huap-rojo)",
  border: "none",
  borderRadius: "8px",
  padding: "7px 12px",
  fontWeight: 600,
  fontSize: "0.85rem",
  cursor: "pointer",
  display: "flex",
  alignItems: "center",
  gap: "4px",
}

const btnSecondary: React.CSSProperties = {
  backgroundColor: "#F1F5F9",
  color: "#374151",
  border: "none",
  borderRadius: "8px",
  padding: "7px 12px",
  fontWeight: 600,
  fontSize: "0.85rem",
  cursor: "pointer",
  display: "flex",
  alignItems: "center",
  gap: "4px",
}

// ── Formulario nueva pregunta ─────────────────────────────────────────────────

interface FormNuevaPregunta {
  patologia_id: string
  texto_pregunta: string
  respuesta_validada: string
  variantes: string
}

const FORM_VACIO: FormNuevaPregunta = {
  patologia_id: "",
  texto_pregunta: "",
  respuesta_validada: "",
  variantes: "",
}

// ── Componente principal ──────────────────────────────────────────────────────

export default function AdminChatbotPage() {
  const { data: session } = useSession()
  const router = useRouter()

  const [patologias, setPatologias] = useState<PatologiaOut[]>([])
  const [preguntas, setPreguntas] = useState<PreguntaChatbotOut[]>([])
  const [cargando, setCargando] = useState(true)
  const [error403, setError403] = useState(false)

  const [mostrarFormNueva, setMostrarFormNueva] = useState(false)
  const [form, setForm] = useState<FormNuevaPregunta>(FORM_VACIO)
  const [guardando, setGuardando] = useState(false)

  const [editandoId, setEditandoId] = useState<number | null>(null)
  const [formEdit, setFormEdit] = useState<Partial<FormNuevaPregunta>>({})

  const [recargando, setRecargando] = useState(false)
  const [msgRecarga, setMsgRecarga] = useState<string | null>(null)

  const [nuevaPatologia, setNuevaPatologia] = useState("")
  const [mostrarFormPatologia, setMostrarFormPatologia] = useState(false)

  const [expandidaId, setExpandidaId] = useState<number | null>(null)

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const token = (session as any)?.accessToken as string | undefined

  const cargarDatos = useCallback(async () => {
    if (!token) return
    try {
      const [pats, pregs] = await Promise.all([
        adminListarPatologias(token),
        adminListarPreguntas(token),
      ])
      setPatologias(pats)
      setPreguntas(pregs)
    } catch (e: unknown) {
      if (e instanceof Error && e.message.includes("403")) setError403(true)
    } finally {
      setCargando(false)
    }
  }, [token])

  useEffect(() => {
    cargarDatos()
  }, [cargarDatos])

  async function handleCrearPregunta() {
    if (!token || !form.patologia_id || !form.texto_pregunta || !form.respuesta_validada) return
    setGuardando(true)
    try {
      const variantes = form.variantes
        ? form.variantes.split("\n").map((v) => v.trim()).filter(Boolean)
        : []
      await adminCrearPregunta(
        {
          patologia_id: parseInt(form.patologia_id),
          texto_pregunta: form.texto_pregunta.trim(),
          respuesta_validada: form.respuesta_validada.trim(),
          variantes,
        },
        token,
      )
      setForm(FORM_VACIO)
      setMostrarFormNueva(false)
      await cargarDatos()
    } finally {
      setGuardando(false)
    }
  }

  async function handleGuardarEdicion(id: number) {
    if (!token) return
    const variantes =
      formEdit.variantes !== undefined
        ? formEdit.variantes.split("\n").map((v) => v.trim()).filter(Boolean)
        : undefined
    await adminActualizarPregunta(
      id,
      {
        texto_pregunta: formEdit.texto_pregunta?.trim(),
        respuesta_validada: formEdit.respuesta_validada?.trim(),
        variantes,
      },
      token,
    )
    setEditandoId(null)
    setFormEdit({})
    await cargarDatos()
  }

  async function handleEliminar(id: number) {
    if (!token) return
    if (!window.confirm("¿Eliminar esta pregunta de la whitelist?")) return
    await adminEliminarPregunta(id, token)
    await cargarDatos()
  }

  async function handleRecargar() {
    if (!token) return
    setRecargando(true)
    setMsgRecarga(null)
    try {
      await adminRecargarWhitelist(token)
      setMsgRecarga("Índice FAISS recargado correctamente.")
    } catch {
      setMsgRecarga("Error al recargar el índice.")
    } finally {
      setRecargando(false)
      setTimeout(() => setMsgRecarga(null), 4000)
    }
  }

  async function handleCrearPatologia() {
    if (!token || !nuevaPatologia.trim()) return
    await adminCrearPatologia(nuevaPatologia.trim(), token)
    setNuevaPatologia("")
    setMostrarFormPatologia(false)
    await cargarDatos()
  }

  function iniciarEdicion(p: PreguntaChatbotOut) {
    setEditandoId(p.id)
    setFormEdit({
      texto_pregunta: p.texto_pregunta,
      respuesta_validada: p.respuesta_validada,
      variantes: p.variantes.join("\n"),
    })
  }

  const nombrePatologia = (id: number) =>
    patologias.find((p) => p.id === id)?.nombre ?? `#${id}`

  // ── Render ──────────────────────────────────────────────────────────────────

  if (error403) {
    return (
      <div style={{ minHeight: "100dvh", display: "flex", alignItems: "center", justifyContent: "center", backgroundColor: "var(--huap-fondo)" }}>
        <div style={{ textAlign: "center", padding: "32px" }}>
          <p style={{ fontSize: "3rem", marginBottom: "8px" }}>🔒</p>
          <p style={{ fontWeight: 700, fontSize: "1.2rem", color: "var(--huap-texto)" }}>Acceso restringido</p>
          <p style={{ color: "#888", marginTop: "8px" }}>Necesitas permisos de administrador.</p>
          <button style={{ ...btnPrimary, margin: "24px auto 0", justifyContent: "center" }} onClick={() => router.back()}>
            Volver
          </button>
        </div>
      </div>
    )
  }

  return (
    <div style={{ minHeight: "100dvh", backgroundColor: "var(--huap-fondo)", paddingBottom: "40px" }}>

      {/* Barra superior */}
      <div style={{ backgroundColor: "var(--huap-azul)", padding: "16px 20px", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
          <button
            onClick={() => router.back()}
            style={{ background: "rgba(255,255,255,0.15)", border: "none", borderRadius: "8px", padding: "6px 12px", color: "white", cursor: "pointer", fontSize: "0.9rem" }}
          >
            ← Volver
          </button>
          <span style={{ color: "white", fontWeight: 700, fontSize: "1.1rem" }}>Admin Chatbot</span>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
          {msgRecarga && (
            <span style={{ color: "rgba(255,255,255,0.85)", fontSize: "0.8rem" }}>{msgRecarga}</span>
          )}
          <button
            onClick={handleRecargar}
            disabled={recargando}
            title="Reconstruir índice FAISS de whitelist"
            style={{
              ...btnPrimary,
              backgroundColor: "rgba(255,255,255,0.2)",
              fontSize: "0.85rem",
              padding: "8px 14px",
            }}
          >
            <RefreshCw size={15} strokeWidth={2} style={{ animation: recargando ? "spin 1s linear infinite" : "none" }} />
            {recargando ? "Recargando…" : "Recargar FAISS"}
          </button>
        </div>
      </div>

      <main style={{ padding: "20px 16px", maxWidth: "720px", margin: "0 auto" }}>

        {/* ── Sección Patologías ── */}
        <section style={{ marginBottom: "32px" }}>
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "12px" }}>
            <h2 style={{ fontWeight: 700, fontSize: "1rem", color: "var(--huap-azul)", margin: 0 }}>
              Patologías ({patologias.length})
            </h2>
            <button
              onClick={() => setMostrarFormPatologia((v) => !v)}
              style={{ ...btnPrimary, padding: "7px 14px", fontSize: "0.85rem" }}
            >
              <Plus size={15} strokeWidth={2.5} />
              Nueva
            </button>
          </div>

          {mostrarFormPatologia && (
            <div style={{ ...card, display: "flex", gap: "10px", alignItems: "center" }}>
              <input
                style={{ ...inputStyle, flex: 1 }}
                placeholder="Nombre de la patología (ej. Diabetes)"
                value={nuevaPatologia}
                onChange={(e) => setNuevaPatologia(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleCrearPatologia()}
              />
              <button style={{ ...btnPrimary, flexShrink: 0, padding: "10px 14px" }} onClick={handleCrearPatologia}>
                <Check size={16} />
              </button>
              <button style={{ ...btnSecondary, flexShrink: 0, padding: "10px 14px" }} onClick={() => setMostrarFormPatologia(false)}>
                <X size={16} />
              </button>
            </div>
          )}

          <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
            {cargando
              ? [1, 2, 3].map((n) => (
                  <div key={n} style={{ height: "32px", width: "90px", borderRadius: "20px", backgroundColor: "#e0e0e0", opacity: 0.5 }} />
                ))
              : patologias.map((p) => (
                  <span
                    key={p.id}
                    style={{
                      padding: "6px 14px",
                      borderRadius: "20px",
                      fontSize: "0.85rem",
                      fontWeight: 600,
                      backgroundColor: "#EEF4FA",
                      color: "var(--huap-azul)",
                      border: "1px solid #C5D9EF",
                    }}
                  >
                    {p.nombre}
                  </span>
                ))}
          </div>
        </section>

        {/* ── Sección Preguntas ── */}
        <section>
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "12px" }}>
            <h2 style={{ fontWeight: 700, fontSize: "1rem", color: "var(--huap-azul)", margin: 0 }}>
              Preguntas validadas ({preguntas.length})
            </h2>
            <button
              onClick={() => { setMostrarFormNueva((v) => !v); setForm(FORM_VACIO) }}
              style={{ ...btnPrimary, padding: "7px 14px", fontSize: "0.85rem" }}
            >
              <Plus size={15} strokeWidth={2.5} />
              Nueva pregunta
            </button>
          </div>

          {/* Formulario nueva pregunta */}
          {mostrarFormNueva && (
            <div style={{ ...card, border: "1.5px solid var(--huap-azul)", marginBottom: "16px" }}>
              <p style={{ fontWeight: 700, fontSize: "0.95rem", marginBottom: "14px", color: "var(--huap-azul)" }}>
                Nueva pregunta validada
              </p>
              <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
                <div>
                  <label style={{ fontSize: "0.82rem", fontWeight: 600, color: "#555", display: "block", marginBottom: "4px" }}>
                    Patología *
                  </label>
                  <select
                    style={{ ...inputStyle }}
                    value={form.patologia_id}
                    onChange={(e) => setForm((f) => ({ ...f, patologia_id: e.target.value }))}
                  >
                    <option value="">— Seleccionar —</option>
                    {patologias.map((p) => (
                      <option key={p.id} value={p.id}>{p.nombre}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label style={{ fontSize: "0.82rem", fontWeight: 600, color: "#555", display: "block", marginBottom: "4px" }}>
                    Pregunta principal *
                  </label>
                  <textarea
                    style={{ ...inputStyle, resize: "vertical", minHeight: "60px" }}
                    placeholder="¿Cuáles son los síntomas de la diabetes?"
                    value={form.texto_pregunta}
                    onChange={(e) => setForm((f) => ({ ...f, texto_pregunta: e.target.value }))}
                  />
                </div>
                <div>
                  <label style={{ fontSize: "0.82rem", fontWeight: 600, color: "#555", display: "block", marginBottom: "4px" }}>
                    Respuesta validada *
                  </label>
                  <textarea
                    style={{ ...inputStyle, resize: "vertical", minHeight: "100px" }}
                    placeholder="Los síntomas principales de la diabetes son…"
                    value={form.respuesta_validada}
                    onChange={(e) => setForm((f) => ({ ...f, respuesta_validada: e.target.value }))}
                  />
                </div>
                <div>
                  <label style={{ fontSize: "0.82rem", fontWeight: 600, color: "#555", display: "block", marginBottom: "4px" }}>
                    Variantes (una por línea, opcional)
                  </label>
                  <textarea
                    style={{ ...inputStyle, resize: "vertical", minHeight: "60px" }}
                    placeholder={"¿Qué síntomas tiene la diabetes?\n¿Cómo sé si tengo diabetes?"}
                    value={form.variantes}
                    onChange={(e) => setForm((f) => ({ ...f, variantes: e.target.value }))}
                  />
                </div>
                <div style={{ display: "flex", gap: "10px", justifyContent: "flex-end" }}>
                  <button style={btnSecondary} onClick={() => setMostrarFormNueva(false)}>
                    <X size={15} /> Cancelar
                  </button>
                  <button
                    style={{
                      ...btnPrimary,
                      opacity: !form.patologia_id || !form.texto_pregunta || !form.respuesta_validada || guardando ? 0.6 : 1,
                    }}
                    disabled={!form.patologia_id || !form.texto_pregunta || !form.respuesta_validada || guardando}
                    onClick={handleCrearPregunta}
                  >
                    <Check size={15} />
                    {guardando ? "Guardando…" : "Guardar"}
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Lista de preguntas */}
          {cargando ? (
            [1, 2, 3].map((n) => (
              <div key={n} style={{ ...card, height: "80px", opacity: 0.4 }} />
            ))
          ) : preguntas.length === 0 ? (
            <div style={{ ...card, textAlign: "center", color: "#aaa", padding: "32px" }}>
              <p>No hay preguntas validadas todavía.</p>
              <p style={{ fontSize: "0.85rem", marginTop: "6px" }}>Agrega una para construir la whitelist del chatbot.</p>
            </div>
          ) : (
            preguntas.map((p) => (
              <div key={p.id} style={{ ...card, border: editandoId === p.id ? "1.5px solid var(--huap-azul)" : "1px solid transparent" }}>

                {/* Cabecera de la tarjeta */}
                <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: "12px" }}>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "6px", flexWrap: "wrap" }}>
                      <span style={{
                        fontSize: "0.72rem", fontWeight: 700, padding: "2px 10px",
                        borderRadius: "20px", backgroundColor: "#EEF4FA", color: "var(--huap-azul)",
                      }}>
                        {nombrePatologia(p.patologia_id)}
                      </span>
                      <span style={{
                        fontSize: "0.72rem", fontWeight: 700, padding: "2px 10px",
                        borderRadius: "20px",
                        backgroundColor: p.activa ? "#E8F5E9" : "#FFEBEE",
                        color: p.activa ? "var(--huap-verde)" : "var(--huap-rojo)",
                      }}>
                        {p.activa ? "Activa" : "Inactiva"}
                      </span>
                      {p.variantes.length > 0 && (
                        <span style={{ fontSize: "0.72rem", color: "#888" }}>
                          +{p.variantes.length} variante{p.variantes.length > 1 ? "s" : ""}
                        </span>
                      )}
                    </div>

                    {editandoId !== p.id && (
                      <p
                        onClick={() => setExpandidaId(expandidaId === p.id ? null : p.id)}
                        style={{ fontWeight: 600, fontSize: "0.95rem", color: "var(--huap-texto)", cursor: "pointer", margin: 0 }}
                      >
                        {p.texto_pregunta}
                      </p>
                    )}
                  </div>

                  {/* Botones acción */}
                  {editandoId !== p.id && (
                    <div style={{ display: "flex", gap: "6px", flexShrink: 0 }}>
                      <button style={btnSecondary} onClick={() => iniciarEdicion(p)} title="Editar">
                        <Pencil size={14} />
                      </button>
                      <button style={btnDanger} onClick={() => handleEliminar(p.id)} title="Eliminar">
                        <Trash2 size={14} />
                      </button>
                      <button
                        style={btnSecondary}
                        onClick={() => setExpandidaId(expandidaId === p.id ? null : p.id)}
                        title={expandidaId === p.id ? "Colapsar" : "Ver respuesta"}
                      >
                        {expandidaId === p.id ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
                      </button>
                    </div>
                  )}
                </div>

                {/* Respuesta expandida */}
                {expandidaId === p.id && editandoId !== p.id && (
                  <div style={{ marginTop: "12px", paddingTop: "12px", borderTop: "1px solid #F0F0F0" }}>
                    <p style={{ fontSize: "0.82rem", color: "#888", fontWeight: 600, marginBottom: "4px" }}>RESPUESTA</p>
                    <p style={{ fontSize: "0.9rem", color: "#444", lineHeight: 1.6, whiteSpace: "pre-wrap" }}>
                      {p.respuesta_validada}
                    </p>
                    {p.variantes.length > 0 && (
                      <div style={{ marginTop: "10px" }}>
                        <p style={{ fontSize: "0.82rem", color: "#888", fontWeight: 600, marginBottom: "4px" }}>VARIANTES</p>
                        {p.variantes.map((v, i) => (
                          <p key={i} style={{ fontSize: "0.88rem", color: "#555", marginBottom: "2px" }}>• {v}</p>
                        ))}
                      </div>
                    )}
                  </div>
                )}

                {/* Formulario edición inline */}
                {editandoId === p.id && (
                  <div style={{ display: "flex", flexDirection: "column", gap: "12px", marginTop: "8px" }}>
                    <div>
                      <label style={{ fontSize: "0.82rem", fontWeight: 600, color: "#555", display: "block", marginBottom: "4px" }}>Pregunta</label>
                      <textarea
                        style={{ ...inputStyle, resize: "vertical", minHeight: "60px" }}
                        value={formEdit.texto_pregunta ?? ""}
                        onChange={(e) => setFormEdit((f) => ({ ...f, texto_pregunta: e.target.value }))}
                      />
                    </div>
                    <div>
                      <label style={{ fontSize: "0.82rem", fontWeight: 600, color: "#555", display: "block", marginBottom: "4px" }}>Respuesta validada</label>
                      <textarea
                        style={{ ...inputStyle, resize: "vertical", minHeight: "100px" }}
                        value={formEdit.respuesta_validada ?? ""}
                        onChange={(e) => setFormEdit((f) => ({ ...f, respuesta_validada: e.target.value }))}
                      />
                    </div>
                    <div>
                      <label style={{ fontSize: "0.82rem", fontWeight: 600, color: "#555", display: "block", marginBottom: "4px" }}>Variantes (una por línea)</label>
                      <textarea
                        style={{ ...inputStyle, resize: "vertical", minHeight: "60px" }}
                        value={formEdit.variantes ?? ""}
                        onChange={(e) => setFormEdit((f) => ({ ...f, variantes: e.target.value }))}
                      />
                    </div>
                    <div style={{ display: "flex", gap: "10px", justifyContent: "flex-end" }}>
                      <button style={btnSecondary} onClick={() => { setEditandoId(null); setFormEdit({}) }}>
                        <X size={15} /> Cancelar
                      </button>
                      <button style={btnPrimary} onClick={() => handleGuardarEdicion(p.id)}>
                        <Check size={15} /> Guardar
                      </button>
                    </div>
                  </div>
                )}
              </div>
            ))
          )}
        </section>
      </main>

      <style>{`
        @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
      `}</style>
    </div>
  )
}
