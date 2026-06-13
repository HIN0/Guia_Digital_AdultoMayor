from sqlalchemy.orm import Session
from sqlalchemy import func
from .entity import Conversacion, MensajeChat, PreguntaChatbot, Patologia


# ── Conversaciones ───────────────────────────────────────────────────────────

def obtener_o_crear_conversacion(db: Session, usuario_id: int, conversacion_id: int = None) -> Conversacion:
    if conversacion_id:
        conv = db.query(Conversacion).filter(
            Conversacion.id == conversacion_id,
            Conversacion.usuario_id == usuario_id
        ).first()
        if conv:
            return conv

    nueva_conv = Conversacion(usuario_id=usuario_id)
    db.add(nueva_conv)
    db.commit()
    db.refresh(nueva_conv)
    return nueva_conv

def guardar_mensaje(db: Session, conversacion_id: int, tipo: str, contenido: str, pregunta_chatbot_id: int = None) -> MensajeChat:
    mensaje = MensajeChat(
        conversacion_id=conversacion_id,
        tipo=tipo,
        contenido=contenido,
        pregunta_chatbot_id=pregunta_chatbot_id,
    )
    db.add(mensaje)
    db.commit()
    db.refresh(mensaje)
    return mensaje

def obtener_mensajes_recientes(db: Session, conversacion_id: int, limite: int = 6) -> list[MensajeChat]:
    mensajes = (
        db.query(MensajeChat)
        .filter(MensajeChat.conversacion_id == conversacion_id)
        .order_by(MensajeChat.id.desc())
        .limit(limite)
        .all()
    )
    return list(reversed(mensajes))


# ── Valoración (feedback) ────────────────────────────────────────────────────

def valorar_mensaje(db: Session, mensaje_id: int, usuario_id: int, valoracion: str) -> bool:
    mensaje = (
        db.query(MensajeChat)
        .join(Conversacion)
        .filter(
            MensajeChat.id == mensaje_id,
            Conversacion.usuario_id == usuario_id,
            MensajeChat.tipo.in_(["bot", "fallback"]),
        )
        .first()
    )
    if not mensaje:
        return False
    mensaje.valoracion = valoracion
    db.commit()
    return True


# ── Historial de conversaciones ──────────────────────────────────────────────

def listar_conversaciones(db: Session, usuario_id: int) -> list[dict]:
    conversaciones = (
        db.query(Conversacion)
        .filter(Conversacion.usuario_id == usuario_id)
        .order_by(Conversacion.fecha_inicio.desc())
        .limit(20)
        .all()
    )
    result = []
    for conv in conversaciones:
        total = db.query(func.count(MensajeChat.id)).filter(
            MensajeChat.conversacion_id == conv.id
        ).scalar()
        primer_mensaje_usuario = (
            db.query(MensajeChat)
            .filter(MensajeChat.conversacion_id == conv.id, MensajeChat.tipo == "usuario")
            .order_by(MensajeChat.id.asc())
            .first()
        )
        preview = primer_mensaje_usuario.contenido[:80] if primer_mensaje_usuario else "Conversación"
        result.append({
            "id": conv.id,
            "fecha_inicio": conv.fecha_inicio,
            "preview": preview,
            "total_mensajes": total or 0,
        })
    return result

def obtener_mensajes_conversacion(db: Session, conversacion_id: int, usuario_id: int) -> list[MensajeChat] | None:
    conv = db.query(Conversacion).filter(
        Conversacion.id == conversacion_id,
        Conversacion.usuario_id == usuario_id,
    ).first()
    if not conv:
        return None
    return (
        db.query(MensajeChat)
        .filter(MensajeChat.conversacion_id == conversacion_id)
        .order_by(MensajeChat.id.asc())
        .all()
    )


# ── Preguntas (whitelist) — lectura ─────────────────────────────────────────

def obtener_preguntas_activas(db: Session) -> list[PreguntaChatbot]:
    return db.query(PreguntaChatbot).filter(PreguntaChatbot.activa == True).all()

def listar_todas_las_preguntas(db: Session) -> list[PreguntaChatbot]:
    return db.query(PreguntaChatbot).order_by(PreguntaChatbot.id).all()

def obtener_pregunta_por_id(db: Session, pregunta_id: int) -> PreguntaChatbot | None:
    return db.query(PreguntaChatbot).filter(PreguntaChatbot.id == pregunta_id).first()


# ── Preguntas (whitelist) — escritura ───────────────────────────────────────

def crear_pregunta(db: Session, patologia_id: int, texto_pregunta: str,
                   respuesta_validada: str, variantes: list[str] = None) -> PreguntaChatbot:
    pregunta = PreguntaChatbot(
        patologia_id=patologia_id,
        texto_pregunta=texto_pregunta,
        respuesta_validada=respuesta_validada,
        variantes=variantes or [],
    )
    db.add(pregunta)
    db.commit()
    db.refresh(pregunta)
    return pregunta

def actualizar_pregunta(db: Session, pregunta_id: int, datos: dict) -> PreguntaChatbot | None:
    pregunta = obtener_pregunta_por_id(db, pregunta_id)
    if not pregunta:
        return None
    for campo, valor in datos.items():
        if valor is not None:
            setattr(pregunta, campo, valor)
    db.commit()
    db.refresh(pregunta)
    return pregunta

def eliminar_pregunta(db: Session, pregunta_id: int) -> bool:
    pregunta = obtener_pregunta_por_id(db, pregunta_id)
    if not pregunta:
        return False
    db.delete(pregunta)
    db.commit()
    return True


# ── Patologías ───────────────────────────────────────────────────────────────

def listar_patologias(db: Session) -> list[Patologia]:
    return db.query(Patologia).order_by(Patologia.id).all()

def crear_patologia(db: Session, nombre: str) -> Patologia:
    patologia = Patologia(nombre=nombre)
    db.add(patologia)
    db.commit()
    db.refresh(patologia)
    return patologia
