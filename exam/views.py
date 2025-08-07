from django.shortcuts import render, redirect
from .forms import UploadExamForm
from .models import ExamSession
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
import json
from django.http import FileResponse
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

def upload_exam_view(request):
    if request.method == 'POST':
        form = UploadExamForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Read and decode the uploaded file
                uploaded_file = request.FILES['json_file']
                file_data = uploaded_file.read().decode('utf-8')
                json_data = json.loads(file_data)

                # Extract data from form
                exam_name = form.cleaned_data['exam_name']
                duration = form.cleaned_data['duration']
                json_file_name = uploaded_file.name

                # Store in session
                request.session['questions'] = json_data
                request.session['exam_name'] = exam_name
                request.session['duration'] = duration * 60  # in seconds
                request.session['start_time'] = datetime.now().timestamp()
                request.session['answers'] = {}

                # Save model instance
                exam_session = ExamSession.objects.create(
                    exam_name=exam_name,
                    duration=duration,
                    json_file_name=json_file_name
                )
                request.session['exam_session_id'] = exam_session.id

                return redirect('exam')  # go to exam page

            except json.JSONDecodeError:
                messages.error(request, "Uploaded file is not a valid JSON.")
            except Exception as e:
                messages.error(request, "An error occurred while processing the file.")
    else:
        form = UploadExamForm()

    return render(request, 'exam/upload.html', {'form': form})




# Exam Page with Navigation
def exam_view(request):
    questions = request.session.get('questions')
    answers = request.session.get('answers', {})

    if not questions:
        return redirect('upload_exam')

    total_questions = len(questions)
    q_index = int(request.GET.get('q', 0))

    # Ensure q_index is in bounds
    q_index = max(0, min(q_index, total_questions - 1))

    if request.method == 'POST':
        selected = request.POST.getlist('choice')
        try:
            answers[str(q_index)] = list(map(int, selected))
        except ValueError:
            answers[str(q_index)] = []  # fallback in case of bad input

        request.session['answers'] = answers

        if 'next' in request.POST:
            return HttpResponseRedirect(f"{reverse('exam')}?q={min(q_index + 1, total_questions - 1)}")
        elif 'prev' in request.POST:
            return HttpResponseRedirect(f"{reverse('exam')}?q={max(q_index - 1, 0)}")
        elif 'finish' in request.POST:
            return redirect('submit_exam')

    current_question = questions[q_index]
    is_multiple = len(current_question.get('answer', [])) > 1

    # Timer
    duration = request.session.get('duration', 600)
    start_time = request.session.get('start_time', datetime.now().timestamp())
    time_left = duration - int(datetime.now().timestamp() - start_time)
    if time_left <= 0:
        return redirect('submit_exam')

    return render(request, 'exam/exam_page.html', {
        'question': current_question,
        'q_index': q_index,
        'total': total_questions,
        'answers': answers.get(str(q_index), []),
        'is_multiple': is_multiple,
        'time_left': time_left,
        'palette': answers
    })


# Submit Exam and Evaluate
def submit_exam_view(request):
    questions = request.session.get('questions')
    answers = request.session.get('answers', {})
    exam_session_id = request.session.get('exam_session_id')

    if not questions or not exam_session_id:
        return redirect('upload_exam')

    correct = 0
    wrong = 0
    total = len(questions)

    for i, question in enumerate(questions):
        correct_ans = sorted(question.get('answer', []))
        user_ans = sorted(answers.get(str(i), []))

        if user_ans == correct_ans:
            correct += 1
        elif user_ans:
            wrong += 1

    unanswered = total - (correct + wrong)
    score = correct  # 1 mark per correct question

    # Save result to DB
    try:
        exam_session = ExamSession.objects.get(id=exam_session_id)
        exam_session.total_marks = total
        exam_session.marks_obtained = score
        exam_session.correct_answers = correct
        exam_session.wrong_answers = wrong
        exam_session.save()
    except ExamSession.DoesNotExist:
        messages.warning(request, "Could not find exam session to update results.")

    # Save result to session
    request.session['result_data'] = {
        'score': score,
        'total': total,
        'correct': correct,
        'wrong': wrong,
        'unanswered': unanswered
    }

    return redirect('result')


# Display Final Results
def result_view(request):
    questions = request.session.get('questions')
    answers = request.session.get('answers', {})
    result = request.session.get('result_data', {})

    if not questions or not result:
        return redirect('upload_exam')

    feedback = []

    for index, question in enumerate(questions):
        correct_answers = question.get('answer', [])
        user_answers = answers.get(str(index), [])

        is_correct = sorted(user_answers) == sorted(correct_answers)
        feedback.append({
            'question': question['question'],
            'choices': question['choices'],
            'correct_answers': correct_answers,
            'user_answers': user_answers,
            'is_correct': is_correct,
        })

    return render(request, 'exam/result.html', {
        'result': result,
        'feedback': feedback,
    })




def download_result_pdf(request):
    questions = request.session.get('questions')
    answers = request.session.get('answers', {})
    result = request.session.get('result_data', {})

    if not questions or not result:
        return redirect('upload_exam')

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("📄 <b>Mock Test Result</b>", styles['Title']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Score: {result['score']} / {result['total']}", styles['Normal']))
    elements.append(Paragraph(f"Correct Answers: {result['correct']}", styles['Normal']))
    elements.append(Paragraph(f"Wrong Answers: {result['wrong']}", styles['Normal']))
    elements.append(Paragraph(f"Unanswered: {result['unanswered']}", styles['Normal']))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("📝 <b>Detailed Question Analysis:</b>", styles['Heading2']))
    elements.append(Spacer(1, 10))

    for idx, question in enumerate(questions):
        correct_answers = question.get('answer', [])
        user_answers = answers.get(str(idx), [])
        question_text = question['question']
        choices = question['choices']

        elements.append(Paragraph(f"<b>Q{idx + 1}:</b> {question_text}", styles['Normal']))

        for i, choice in enumerate(choices):
            style = ""
            prefix = "• "

            if i in correct_answers and i in user_answers:
                style = "<font color='green'>✅ "
            elif i in correct_answers:
                style = "<font color='green'>✔ "
            elif i in user_answers:
                style = "<font color='red'>❌ "
            else:
                style = ""

            end_style = "</font>" if style else ""
            elements.append(Paragraph(f"{style}{prefix}{choice}{end_style}", styles['Normal']))

        if not user_answers:
            elements.append(Paragraph("<font color='orange'><i>Not Answered</i></font>", styles['Normal']))

        elements.append(Spacer(1, 10))

    doc.build(elements)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='exam_result.pdf')
