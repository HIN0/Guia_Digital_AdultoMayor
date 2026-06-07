from sqlalchemy.orm import Session
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
