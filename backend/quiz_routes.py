from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from sqlalchemy import func
from backend.models import db, Quiz, Subject, Chapter,Question, Score, User



quiz_bp = Blueprint('quiz', __name__)

# Get all quizzes
@quiz_bp.route('/quizzes/all', methods=['GET'])
@jwt_required()
def get_all_quizzes():
    quizzes = Quiz.query.all()
    result = []
    for q in quizzes:
        result.append({
            "id": q.id,
            "title": q.title,
            "number_of_questions": len(q.questions),  # count questions
            "duration": q.time_duration.strftime("%H:%M") if q.time_duration else "",
            "subject_id": q.chapter.subject.id if q.chapter and q.chapter.subject else None,
            "subject_name": q.chapter.subject.name if q.chapter and q.chapter.subject else "",
            "chapter_id": q.chapter_id,
            "chapter_name": q.chapter.name if q.chapter else "",
            "date": str(q.date_of_quiz) if q.date_of_quiz else "",
        })
    return jsonify(result), 200



#################################
#SUBJECTS.PAGE LOGIC ROUTES
############################

# Add a subject
@quiz_bp.route('/subjects', methods=['POST'])
@jwt_required()
def add_subject():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    if not name:
        return jsonify({"msg": "Name is required"}), 400

    # check for duplicate subject names
    if Subject.query.filter_by(name=name).first():
        return jsonify({"msg": "Subject already exists"}), 409

    subject = Subject(name=name, description=description)
    db.session.add(subject)
    db.session.commit()

    return jsonify({"msg": "Subject added successfully", "id": subject.id}), 201

# Fetch all subjects
@quiz_bp.route('/subjects', methods=['GET'])
@jwt_required()
def get_subjects():
    subjects = Subject.query.all()
    data = [{
        "id": s.id,
        "name": s.name,
        "description": s.description
    } for s in subjects]

    return jsonify(data), 200


@quiz_bp.route('/subjects/<int:subject_id>', methods=['PUT'])
@jwt_required()
def update_subject(subject_id):
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    subject = Subject.query.get(subject_id)
    if not subject:
        return jsonify({"msg": "Subject not found"}), 404

    subject.name = name
    subject.description = description
    db.session.commit()

    return jsonify({"msg": "Subject updated successfully"}), 200

@quiz_bp.route('/subjects/<int:subject_id>', methods=['DELETE'])
@jwt_required()
def delete_subject(subject_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        return jsonify({"msg": "Subject not found"}), 404

    db.session.delete(subject)
    db.session.commit()
    return jsonify({"msg": "Subject deleted successfully"}), 200


@quiz_bp.route("/subjects", methods=["OPTIONS"])
def subjects_options():
    return '', 200


#################################
#CHAPTERS.PAGE LOGIC ROUTES
############################


# Add a new chapter
@quiz_bp.route('/chapters', methods=['POST'])
@jwt_required()
def add_chapter():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    subject_id = data.get('subject_id')

    if not name or not subject_id:
        return jsonify({"msg": "Name and subject_id are required"}), 400

    chapter = Chapter(name=name, description=description, subject_id=subject_id)
    db.session.add(chapter)
    db.session.commit()

    return jsonify({

        "id": chapter.id,
        "name": chapter.name,
        "description": chapter.description,
        "subject_id": chapter.subject_id
    }), 201


# Get chapters by subject
@quiz_bp.route('/chapters/<int:subject_id>', methods=['GET'])
@jwt_required()
def get_chapters(subject_id):
    chapters = Chapter.query.filter_by(subject_id=subject_id).all()
    data = [{
        "id": c.id,
        "name": c.name,
        "description": c.description,
        "subject_id": c.subject_id
    } for c in chapters]

    return jsonify(data), 200

# Update a chapter
@quiz_bp.route('/chapters/<int:chapter_id>', methods=['PUT'])
@jwt_required()
def update_chapter(chapter_id):
    data = request.get_json()
    chapter = Chapter.query.get(chapter_id)

    if not chapter:
        return jsonify({"msg": "Chapter not found"}), 404

    chapter.name = data.get('name', chapter.name)
    chapter.description = data.get('description', chapter.description)
    db.session.commit()

    return jsonify({"msg": "Chapter updated successfully"}), 200

# Delete a chapter
@quiz_bp.route('/chapters/<int:chapter_id>', methods=['DELETE'])
@jwt_required()
def delete_chapter(chapter_id):
    chapter = Chapter.query.get(chapter_id)

    if not chapter:
        return jsonify({"msg": "Chapter not found"}), 404

    db.session.delete(chapter)
    db.session.commit()

    return jsonify({"msg": "Chapter deleted successfully"}), 200

# CORS Preflight support
@quiz_bp.route("/chapters", methods=["OPTIONS"])
def chapters_options():
    return '', 200


#################################
#QUIZZES.PAGE LOGIC ROUTES
############################

# Get quizzes by chapter
@quiz_bp.route('/chapters/<int:chapter_id>/quizzes', methods=['GET'])
@jwt_required()
def get_quizzes_by_chapter(chapter_id):
    quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
    data = [{
        "id": q.id,
        "title": q.title,
        "date_of_quiz": str(q.date_of_quiz) if q.date_of_quiz else "",
        "time_duration": q.time_duration,
        "remarks": q.remarks,
    } for q in quizzes]
    return jsonify(data), 200

# Add quiz to a chapter
@quiz_bp.route('/quizzes', methods=['POST'])
@jwt_required()
def add_quiz():
    data = request.get_json()

    title = data.get('title')
    date_of_quiz = datetime.strptime(data.get('date_of_quiz'), "%Y-%m-%d").date()
    time_duration = datetime.strptime(data.get('time_duration'), "%H:%M").time()
    remarks = data.get('remarks')
    chapter_id = data.get('chapter_id')

    if not title or not chapter_id:
        return jsonify({"msg": "Title and chapter_id are required"}), 400

    quiz = Quiz(
        title=title,
        date_of_quiz=date_of_quiz,
        time_duration=time_duration,
        remarks=remarks,
        chapter_id=chapter_id
    )
    db.session.add(quiz)
    db.session.commit()

    return jsonify({
        "id": quiz.id,
        "title": quiz.title,
        "date_of_quiz": str(quiz.date_of_quiz),
        "time_duration": str(quiz.time_duration),
        "remarks": quiz.remarks,
    }), 201


# Update quiz
@quiz_bp.route('/quizzes/<int:quiz_id>', methods=['PUT'])
@jwt_required()
def update_quiz(quiz_id):
    data = request.get_json()
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({"msg": "Quiz not found"}), 404

    quiz.title = data.get('title', quiz.title)
    quiz.date_of_quiz = datetime.strptime(data.get("date_of_quiz"), "%Y-%m-%d").date()
    quiz.time_duration = datetime.strptime(data.get("time_duration"), "%H:%M").time()
    quiz.remarks = data.get('remarks', quiz.remarks)

    db.session.commit()
    return jsonify({"msg": "Quiz updated successfully"}), 200

# Delete quiz
@quiz_bp.route('/quizzes/<int:quiz_id>', methods=['DELETE'])
@jwt_required()
def delete_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({"msg": "Quiz not found"}), 404

    db.session.delete(quiz)
    db.session.commit()
    return jsonify({"msg": "Quiz deleted successfully"}), 200




#################################
#QUESTIONS.PAGE LOGIC ROUTES
############################

questions_bp = Blueprint('questions', __name__, url_prefix='/quiz')

# GET all questions for a specific quiz
@questions_bp.route('/chapters/<int:chapter_id>/quizzes/<int:quiz_id>/questions', methods=['GET', "OPTIONS"])
@jwt_required()
def get_questions(quiz_id, chapter_id):
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    data = [{
        "id": q.id,
        "question_statement": q.question_statement,
        "option1": q.option1,
        "option2": q.option2,
        "option3": q.option3,
        "option4": q.option4,
        "correct_answer": q.correct_answer
    } for q in questions]
    return jsonify(data), 200

# POST: Add a new question to a quiz
@questions_bp.route('/chapters/<int:chapter_id>/quizzes/<int:quiz_id>/questions', methods=['POST', "OPTIONS"])
@jwt_required()
def add_question(quiz_id, chapter_id):
    data = request.get_json()
    question = Question(
        quiz_id=quiz_id,
        question_statement=data.get("question_statement"),
        option1=data.get("option1"),
        option2=data.get("option2"),
        option3=data.get("option3"),
        option4=data.get("option4"),
        correct_answer=data.get("correct_answer"),
    )
    db.session.add(question)
    db.session.commit()
    return jsonify({"message": "Question added successfully"}), 201

# PUT: Edit/update a specific question
@questions_bp.route('/questions/<int:question_id>', methods=['PUT', "OPTIONS"])
@jwt_required()
def update_question(question_id):
    question = Question.query.get(question_id)
    if not question:
        return jsonify({"error": "Question not found"}), 404

    data = request.get_json()
    question.question_statement = data.get("question_statement", question.question_statement)
    question.option1 = data.get("option1", question.option1)
    question.option2 = data.get("option2", question.option2)
    question.option3 = data.get("option3", question.option3)
    question.option4 = data.get("option4", question.option4)
    question.correct_answer = data.get("correct_answer", question.correct_answer)
    
    db.session.commit()
    return jsonify({"message": "Question updated successfully"}), 200

# DELETE: Remove a question
@questions_bp.route('/questions/<int:question_id>', methods=['DELETE', "OPTIONS"])
@jwt_required()
def delete_question(question_id):
    question = Question.query.get(question_id)
    if not question:
        return jsonify({"error": "Question not found"}), 404

    db.session.delete(question)
    db.session.commit()
    return jsonify({"message": "Question deleted successfully"}), 200




###################################################################################
#USER DASHBOARD
###################################

@quiz_bp.route('/quizzes/<int:quiz_id>/questions', methods=['GET'])
@jwt_required()
def get_quiz_questions(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    result = [{
        'id': q.id,
        'question_statement': q.question_statement,
        'option1': q.option1,
        'option2': q.option2,
        'option3': q.option3,
        'option4': q.option4
    } for q in questions]
    return jsonify({
        'quiz_id': quiz.id,
        'duration': quiz.time_duration.strftime("%H:%M") if quiz.time_duration else "00:15",
        'questions': result
    }), 200



@quiz_bp.route('/quizzes/<int:quiz_id>/submit', methods=['POST'])
@jwt_required()
def submit_quiz(quiz_id):
    data = request.get_json()
    answers = data.get("answers")  # list of {question_id, selected_option}
    
    user_id = get_jwt_identity()
    correct = 0

    for ans in answers:
        question = Question.query.get(ans["question_id"])
        if question and question.correct_answer == ans["selected_option"]:
            correct += 1

    new_score = Score(
        quiz_id=quiz_id,
        user_id=user_id,
        total_scored=correct,
        time_stamp_of_attempt=datetime.now()
    )
    db.session.add(new_score)
    db.session.commit()

    return jsonify({
        "message": "Quiz submitted successfully",
        "correct": correct,
        "total": len(answers)
    }), 200



########################
#SCORE BOARD
#########################

# GET all scores for the current user
@quiz_bp.route('/user/scores', methods=['GET'])
@jwt_required()
def get_user_scores():
    user_id = get_jwt_identity()
    scores = Score.query.filter_by(user_id=user_id).order_by(Score.time_stamp_of_attempt.asc()).all()
    result = []
    for score in scores:
        total_questions = len(score.quiz.questions)
        result.append({
            "id": score.id,
            "quiz_id": score.quiz_id,
            "time_stamp_of_attempt": score.time_stamp_of_attempt,
            "total_scored": f"{score.total_scored}/{total_questions}",
            "percentage": round((score.total_scored / total_questions) * 100, 2) if total_questions > 0 else 0
        })
    return jsonify(result), 200


# GET quiz completion summary
@quiz_bp.route('/user/quiz-summary', methods=['GET'])
@jwt_required()
def get_quiz_completion_summary():
    user_id = get_jwt_identity()
    all_quiz_ids = [quiz.id for quiz in Quiz.query.all()]
    attempted_quiz_ids = {score.quiz_id for score in Score.query.filter_by(user_id=user_id).all()}
    return jsonify({
        "total_quizzes": len(all_quiz_ids),
        "attempted_quizzes": len(attempted_quiz_ids)
    }), 200




########################     SEARCH RELATED ROUTES ################################################################

@quiz_bp.route('/search', methods=['GET', "OPTIONS"])
#@jwt_required()
def search_all():
    search_type = request.args.get('type')
    q = request.args.get('q', '').lower()

    if search_type == 'users':
        results = User.query.filter(User.username.ilike(f"%{q}%")).all()
        return jsonify([{
            "id": u.id,
            "username": u.username,
            "full_name": u.full_name,
            "qualification": u.qualification,
            "dob": str(u.dob) if u.dob else None
        } for u in results]), 200

    elif search_type == 'subjects':
        results = Subject.query.filter(Subject.name.ilike(f"%{q}%")).all()
        return jsonify([{
            "id": s.id,
            "name": s.name,
            "description": s.description
        } for s in results]), 200

    elif search_type == 'quizzes':
        results = Quiz.query.filter(Quiz.title.ilike(f"%{q}%")).all()
        return jsonify([{
            "id": qz.id,
            "title": qz.title
        } for qz in results]), 200

    return jsonify([]), 200




#GET USER BY ID:
@quiz_bp.route('/user/<int:user_id>', methods=['GET', "OPTIONS"])
#@jwt_required()
def get_user_info(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    return jsonify({
        "id": user.id,
        "username": user.username,
        "full_name": user.full_name,
        "qualification": user.qualification,
        "dob": str(user.dob) if user.dob else None
    }), 200

#GET USERS SCORE HISTORY:
@quiz_bp.route('/user/<int:user_id>/scores', methods=['GET', "OPTIONS"])
#@jwt_required()
def get_scores_for_user(user_id):
    scores = Score.query.filter_by(user_id=user_id).order_by(Score.time_stamp_of_attempt).all()
    result = []
    for score in scores:
        total_questions = len(score.quiz.questions)
        result.append({
            "quiz_id": score.quiz_id,
            "time_stamp_of_attempt": score.time_stamp_of_attempt.isoformat(),
            "total_scored": score.total_scored,
            "percentage": round((score.total_scored / total_questions) * 100, 2) if total_questions > 0 else 0
        })
    return jsonify(result), 200


#Quiz Detail + Avg Scores
@quiz_bp.route('quiz/details/<int:quiz_id>', methods=['GET', "OPTIONS"])
@jwt_required()
def get_quiz_details(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({"msg": "Quiz not found"}), 404

    # Get scores grouped by user
    scores = db.session.query(
        User.username,
        func.avg(Score.total_scored).label("avg_score"),
        func.count(Question.id).label("total_questions")
    ).join(Score).join(Quiz).join(Question).filter(
        Score.quiz_id == quiz_id
    ).group_by(User.id).all()

    labels = []
    data = []

    for username, avg_score, total_q in scores:
        percentage = round((avg_score / total_q) * 100, 2) if total_q else 0
        labels.append(username)
        data.append(percentage)

    return jsonify({
        "quiz": {
            "id": quiz.id,
            "chapter_id": quiz.chapter_id,
            "title": quiz.title,
            "date_of_quiz": str(quiz.date_of_quiz),
            "time_duration": quiz.time_duration,
            "remarks": quiz.remarks
        },
        "chart": {
            "labels": labels,
            "data": data
        }
    }), 200


# Subject Detail + Avg Scores per Quiz
@quiz_bp.route('/subject/<int:subject_id>', methods=['GET', "OPTIONS"])
@jwt_required()
def get_subject_details(subject_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        return jsonify({"msg": "Subject not found"}), 404

    # Get quizzes under subject
    quizzes = Quiz.query.join(Chapter).filter(Chapter.subject_id == subject_id).all()

    chart_labels = []
    chart_data = []

    for quiz in quizzes:
        total_questions = len(quiz.questions)
        scores = Score.query.filter_by(quiz_id=quiz.id).all()
        if scores and total_questions > 0:
            avg_score = sum(s.total_scored for s in scores) / len(scores)
            percentage = round((avg_score / total_questions) * 100, 2)
            chart_labels.append(quiz.title)
            chart_data.append(percentage)

    return jsonify({
        "subject": {
            "id": subject.id,
            "name": subject.name,
            "description": subject.description
        },
        "chart": {
            "labels": chart_labels,
            "data": chart_data
        }
    }), 200


