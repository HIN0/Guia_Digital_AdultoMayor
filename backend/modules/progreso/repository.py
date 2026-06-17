"""
Capa de abstracción de datos.
Aísla todas las transacciones directas (queries) contra la base de datos.
"""
from sqlalchemy.orm import Session
from .entity import ProgresoLeccion, IntentoQuiz, InsigniaObtenida, Insignia
from .schema import (
    ProgresoLeccionCreate, SubmitQuizCreate,
    ResultadoQuizResponse, FeedbackPregunta, InsigniaResponse,
)
from modules.educacion.entity import QuizFinal, PreguntaQuiz, OpcionRespuesta, Modulo, Leccion

# Mapeo orden de módulo → nombre de insignia en BD
_INSIGNIA_POR_MODULO = {
    1: "Conocedor de la IA",
    2: "Practicante de la IA",
    3: "Asistente de IA",
}

def otorgar_insignia_modulo(db: Session, usuario_id: int, modulo_orden: int):
    """Otorga la insignia del módulo al usuario si no la tiene ya. Retorna el ORM o None."""
    nombre = _INSIGNIA_POR_MODULO.get(modulo_orden)
    if not nombre:
        return None
    insignia = db.query(Insignia).filter(Insignia.nombre == nombre).first()
    if not insignia:
        return None
    ya_tiene = db.query(InsigniaObtenida).filter(
        InsigniaObtenida.usuario_id == usuario_id,
        InsigniaObtenida.insignia_id == insignia.id,
    ).first()
    if ya_tiene:
        return None
    db.add(InsigniaObtenida(usuario_id=usuario_id, insignia_id=insignia.id))
    db.commit()
    return insignia


def registrar_leccion(db: Session, usuario_id: int, progreso: ProgresoLeccionCreate):
    """Inserta un nuevo registro de lección completada para un usuario."""
    nuevo_progreso = ProgresoLeccion(
        usuario_id=usuario_id,
        leccion_id=progreso.leccion_id,
        completada=True,
    )
    db.add(nuevo_progreso)
    db.commit()
    db.refresh(nuevo_progreso)
    return nuevo_progreso

def obtener_lecciones_usuario(db: Session, usuario_id: int):
    """Retorna todas las lecciones marcadas como completadas por el usuario."""
    return db.query(ProgresoLeccion).filter(
        ProgresoLeccion.usuario_id == usuario_id,
        ProgresoLeccion.completada == True,
    ).all()

def procesar_quiz(db: Session, usuario_id: int, submit: SubmitQuizCreate) -> ResultadoQuizResponse:
    quiz = db.query(QuizFinal).filter(QuizFinal.id == submit.quiz_id).first()
    if not quiz:
        raise ValueError(f"Quiz {submit.quiz_id} no encontrado")

    feedbacks = []
    aciertos = 0

    for resp in submit.respuestas:
        pregunta = db.query(PreguntaQuiz).filter(
            PreguntaQuiz.id == resp.pregunta_id,
            PreguntaQuiz.quiz_final_id == submit.quiz_id,
        ).first()
        if not pregunta:
            continue

        opcion_seleccionada = db.query(OpcionRespuesta).filter(
            OpcionRespuesta.id == resp.opcion_id,
            OpcionRespuesta.pregunta_id == resp.pregunta_id,
        ).first()

        opcion_correcta = db.query(OpcionRespuesta).filter(
            OpcionRespuesta.pregunta_id == resp.pregunta_id,
            OpcionRespuesta.es_correcta == True,
        ).first()

        es_correcta = opcion_seleccionada is not None and opcion_seleccionada.es_correcta
        if es_correcta:
            aciertos += 1

        feedbacks.append(FeedbackPregunta(
            pregunta_id=resp.pregunta_id,
            opcion_correcta_id=opcion_correcta.id if opcion_correcta else 0,
            opcion_seleccionada_id=resp.opcion_id,
            es_correcta=es_correcta,
            feedback=pregunta.feedback,
        ))

    aprobado = aciertos >= quiz.minimo_aciertos

    db.add(IntentoQuiz(usuario_id=usuario_id, quiz_id=submit.quiz_id, puntaje=aciertos, aprobado=aprobado))
    db.commit()

    # Otorgar insignia del módulo cuando el quiz es aprobado
    insignia_response = None
    if aprobado:
        modulo = db.query(Modulo).filter(Modulo.id == quiz.modulo_id).first()
        if modulo:
            insignia_orm = otorgar_insignia_modulo(db, usuario_id, modulo.orden)
            if insignia_orm:
                insignia_response = InsigniaResponse.model_validate(insignia_orm)

    return ResultadoQuizResponse(
        puntaje=aciertos,
        minimo_aciertos=quiz.minimo_aciertos,
        aprobado=aprobado,
        feedbacks=feedbacks,
        insignia_otorgada=insignia_response,
    )

def usuario_aprobo_quiz(db: Session, usuario_id: int, quiz_id: int) -> bool:
    """Retorna True si el usuario aprobó este quiz al menos una vez."""
    return db.query(IntentoQuiz).filter(
        IntentoQuiz.usuario_id == usuario_id,
        IntentoQuiz.quiz_id == quiz_id,
        IntentoQuiz.aprobado == True,
    ).first() is not None

def obtener_lecciones_completadas_de_modulo(db: Session, usuario_id: int, modulo_id: int) -> list[int]:
    """Retorna IDs de lecciones completadas por el usuario en un módulo específico."""
    rows = (
        db.query(ProgresoLeccion.leccion_id)
        .join(Leccion, ProgresoLeccion.leccion_id == Leccion.id)
        .filter(
            ProgresoLeccion.usuario_id == usuario_id,
            Leccion.modulo_id == modulo_id,
            ProgresoLeccion.completada == True,
        ).all()
    )
    return [r[0] for r in rows]

def obtener_quizzes_aprobados(db: Session, usuario_id: int) -> list[int]:
    """Retorna los IDs de quizzes que el usuario aprobó al menos una vez."""
    intentos = db.query(IntentoQuiz.quiz_id).filter(
        IntentoQuiz.usuario_id == usuario_id,
        IntentoQuiz.aprobado == True,
    ).distinct().all()
    return [i[0] for i in intentos]

def obtener_insignias_usuario(db: Session, usuario_id: int):
    """Ejecuta un JOIN para obtener los detalles de las insignias ganadas por el usuario."""
    return db.query(Insignia).join(InsigniaObtenida).filter(
        InsigniaObtenida.usuario_id == usuario_id,
    ).all()
