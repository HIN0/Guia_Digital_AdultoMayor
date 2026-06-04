"""
Capa de abstracción de datos.
Aísla todas las transacciones directas (queries) contra la base de datos.
"""
from sqlalchemy.orm import Session
from .entity import ProgresoLeccion, IntentoQuiz, InsigniaObtenida, Insignia
from .schema import ProgresoLeccionCreate, IntentoQuizCreate, SubmitQuizCreate, ResultadoQuizResponse, FeedbackPregunta
from modules.educacion.entity import QuizFinal, PreguntaQuiz, OpcionRespuesta

def registrar_leccion(db: Session, usuario_id: int, progreso: ProgresoLeccionCreate):
    """Inserta un nuevo registro de lección completada para un usuario."""
    nuevo_progreso = ProgresoLeccion(
        usuario_id=usuario_id, 
        leccion_id=progreso.leccion_id, 
        completada=True
    )
    db.add(nuevo_progreso)
    db.commit()
    db.refresh(nuevo_progreso)
    
    return nuevo_progreso

def obtener_lecciones_usuario(db: Session, usuario_id: int):
    """Retorna todas las lecciones marcadas como completadas por el usuario."""
    return db.query(ProgresoLeccion).filter(
        ProgresoLeccion.usuario_id == usuario_id, 
        ProgresoLeccion.completada == True
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
            PreguntaQuiz.quiz_final_id == submit.quiz_id
        ).first()
        if not pregunta:
            continue

        opcion_seleccionada = db.query(OpcionRespuesta).filter(
            OpcionRespuesta.id == resp.opcion_id,
            OpcionRespuesta.pregunta_id == resp.pregunta_id
        ).first()

        opcion_correcta = db.query(OpcionRespuesta).filter(
            OpcionRespuesta.pregunta_id == resp.pregunta_id,
            OpcionRespuesta.es_correcta == True
        ).first()

        es_correcta = opcion_seleccionada is not None and opcion_seleccionada.es_correcta
        if es_correcta:
            aciertos += 1

        feedbacks.append(FeedbackPregunta(
            pregunta_id=resp.pregunta_id,
            opcion_correcta_id=opcion_correcta.id if opcion_correcta else 0,
            opcion_seleccionada_id=resp.opcion_id,
            es_correcta=es_correcta,
            feedback=pregunta.feedback
        ))

    aprobado = aciertos >= quiz.minimo_aciertos

    intento = IntentoQuiz(usuario_id=usuario_id, quiz_id=submit.quiz_id, puntaje=aciertos, aprobado=aprobado)
    db.add(intento)
    db.commit()

    return ResultadoQuizResponse(
        puntaje=aciertos,
        minimo_aciertos=quiz.minimo_aciertos,
        aprobado=aprobado,
        feedbacks=feedbacks
    )

def obtener_insignias_usuario(db: Session, usuario_id: int):
    """Ejecuta un JOIN para obtener los detalles de las insignias ganadas por el usuario."""
    return db.query(Insignia).join(InsigniaObtenida).filter(
        InsigniaObtenida.usuario_id == usuario_id
    ).all()