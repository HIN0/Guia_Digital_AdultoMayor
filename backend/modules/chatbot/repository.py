from collections import defaultdict

from sqlalchemy import func, or_
from sqlalchemy.orm import Session, aliased

from .entity import Conversacion, MensajeChat, Patologia, PreguntaChatbot

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

def guardar_mensaje(db: Session, conversacion_id: int, tipo: str, contenido: str,
                    pregunta_chatbot_id: int = None, secciones: list = None) -> MensajeChat:
    mensaje = MensajeChat(
        conversacion_id=conversacion_id,
        tipo=tipo,
        contenido=contenido,
        pregunta_chatbot_id=pregunta_chatbot_id,
        secciones=secciones,
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
            MensajeChat.tipo.in_(["bot", "fallback", "emergencia"]),
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
    """Una sola consulta con agregados. Antes hacía un count y una búsqueda del
    primer mensaje POR conversación: con el tope de 20, 41 consultas."""
    totales = (
        db.query(
            MensajeChat.conversacion_id.label("conversacion_id"),
            func.count(MensajeChat.id).label("total"),
        )
        .group_by(MensajeChat.conversacion_id)
        .subquery()
    )
    primeros = (
        db.query(
            MensajeChat.conversacion_id.label("conversacion_id"),
            func.min(MensajeChat.id).label("mensaje_id"),
        )
        .filter(MensajeChat.tipo == "usuario")
        .group_by(MensajeChat.conversacion_id)
        .subquery()
    )
    primer_mensaje = aliased(MensajeChat)

    filas = (
        db.query(Conversacion, totales.c.total, primer_mensaje.contenido)
        .outerjoin(totales, totales.c.conversacion_id == Conversacion.id)
        .outerjoin(primeros, primeros.c.conversacion_id == Conversacion.id)
        .outerjoin(primer_mensaje, primer_mensaje.id == primeros.c.mensaje_id)
        .filter(Conversacion.usuario_id == usuario_id)
        .order_by(Conversacion.fecha_inicio.desc())
        .limit(20)
        .all()
    )
    return [
        {
            "id": conv.id,
            "fecha_inicio": conv.fecha_inicio,
            "preview": (contenido or "Conversación")[:80],
            "total_mensajes": total or 0,
        }
        for conv, total, contenido in filas
    ]

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


# ── Revisión de calidad (admin) ──────────────────────────────────────────────

def resumen_chatbot(db: Session) -> dict:
    """Contadores para saber cómo se está portando el bot en producción."""
    conteos = dict(
        db.query(MensajeChat.tipo, func.count(MensajeChat.id))
        .group_by(MensajeChat.tipo)
        .all()
    )
    valoraciones = dict(
        db.query(MensajeChat.valoracion, func.count(MensajeChat.id))
        .filter(MensajeChat.valoracion.isnot(None))
        .group_by(MensajeChat.valoracion)
        .all()
    )
    return {
        "preguntas": conteos.get("usuario", 0),
        "respuestas": conteos.get("bot", 0),
        "fallbacks": conteos.get("fallback", 0),
        "emergencias": conteos.get("emergencia", 0),
        "valoraciones_positivas": valoraciones.get("positiva", 0),
        "valoraciones_negativas": valoraciones.get("negativa", 0),
    }


def listar_para_revision(db: Session, limite: int = 50) -> list[dict]:
    """Respuestas que el equipo debería mirar: las que cayeron en fallback (el
    bot no supo responder) y las que el usuario valoró negativamente. Cada una
    con la pregunta que la provocó, que es lo que hace falta para decidir si
    agregarla a la whitelist.

    Dos consultas en total: los mensajes marcados y, en bloque, las preguntas
    de sus conversaciones."""
    marcados = (
        db.query(MensajeChat)
        .filter(or_(MensajeChat.tipo == "fallback", MensajeChat.valoracion == "negativa"))
        .order_by(MensajeChat.id.desc())
        .limit(limite)
        .all()
    )
    if not marcados:
        return []

    preguntas = (
        db.query(MensajeChat)
        .filter(
            MensajeChat.conversacion_id.in_({m.conversacion_id for m in marcados}),
            MensajeChat.tipo == "usuario",
        )
        .order_by(MensajeChat.id.asc())
        .all()
    )
    por_conversacion = defaultdict(list)
    for pregunta in preguntas:
        por_conversacion[pregunta.conversacion_id].append(pregunta)

    items = []
    for mensaje in marcados:
        previas = [p for p in por_conversacion[mensaje.conversacion_id] if p.id < mensaje.id]
        items.append({
            "mensaje_id": mensaje.id,
            "conversacion_id": mensaje.conversacion_id,
            "fecha": mensaje.fecha,
            "motivo": "fallback" if mensaje.tipo == "fallback" else "valoracion_negativa",
            "pregunta": previas[-1].contenido if previas else "",
            "respuesta": mensaje.contenido,
            "secciones": mensaje.secciones or [],
        })
    return items


# ── Preguntas (whitelist) — lectura ─────────────────────────────────────────

def obtener_preguntas_activas(db: Session) -> list[PreguntaChatbot]:
    return (
        db.query(PreguntaChatbot)
        .join(Patologia)
        .filter(PreguntaChatbot.activa, Patologia.validada)
        .all()
    )

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
    return db.query(Patologia).filter(Patologia.validada).order_by(Patologia.id).all()

def crear_patologia(db: Session, nombre: str) -> Patologia:
    patologia = Patologia(nombre=nombre)
    db.add(patologia)
    db.commit()
    db.refresh(patologia)
    return patologia
