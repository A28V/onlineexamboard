from django.shortcuts import render
from django.http import HttpResponseRedirect;
from django.contrib import messages
# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import ExamName,Start_exam_user,AttemptedQuestion,Question,Result
from users.models import UsersConfig
from datetime import datetime
from pytz import timezone
from datetime import datetime, timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse;
from django.http import JsonResponse


def result_page(request, id):
    if 'userid' in request.session:
        user_id = request.session['userid']
        try:
            user = UsersConfig.objects.get(id=user_id)
            attempted_questions = AttemptedQuestion.objects.filter(exam=id, user=user)
            correct_count = sum(attempt.is_correct for attempt in attempted_questions)
            score = correct_count * 2
            result = Result.objects.create(user=user, exam_id=id, score=score)
            results = Result.objects.filter(user=user, exam=id)
            exam = ExamName.objects.get(id=id)
            total_questions=exam.questions.count()
            total_score = total_questions*2
            return render(request, 'result_page.html', {'exam': exam, 'questions': exam.questions.all(), 'score': score, 'attempted_questions': attempted_questions,'total_score':total_score})
        except (UsersConfig.DoesNotExist, ExamName.DoesNotExist):
            return HttpResponseRedirect('/login')
    else:
        return HttpResponseRedirect('/login')

def exam_list(request):
    request.session['userid'];
    if request.session['useremail'] != "":
        exams = ExamName.objects.all()
        return render(request, 'exam_list.html', {'exams': exams})
    else:
        return HttpResponseRedirect('/login')

def exam_details(request,id):
    exam = ExamName.objects.filter(id=id)
    if(exam.exists()):
        user =UsersConfig.objects.get(id=request.session['userid']);
        exam_instances = Start_exam_user.objects.filter(exam=id,user=user)
        if exam_instances.exists():
            remaining_time=exam.first().duration
            ist_time = exam_instances.first().timestamp.astimezone(timezone('Asia/Kolkata'))
            dt = ist_time.replace(second=0, microsecond=0)
            end_time = dt + timedelta(minutes=remaining_time)
            current_time = datetime.now(timezone('Asia/Kolkata'))
            remaining_time = end_time - current_time
            remaining_time = int(remaining_time.total_seconds() //60)
            # if remaining_time < 0:
            #     messages.success(request, "Congratulations on completing the exam successfully! If you have any further questions or need assistance with anything else, feel free to ask.")
            #     return HttpResponseRedirect('/exam-list')
        exam_1 = ExamName.objects.get(id=id)
        question_ids = exam_1.questions.values_list('id', flat=True)
        questions_queryset = exam_1.questions.all()
        return render(request, 'exam_detail.html',{"user_email":request.session['useremail'],'questions_queryset':questions_queryset,'exam':exam[0],'id':id})
    else:
        return HttpResponseRedirect('/login')


def views_exam_details(request,id):
    if request.session['useremail'] != "":
        
        exam_qs = ExamName.objects.filter(id=id)
        if exam_qs.exists():
            exam = exam_qs.values()
            duration=0
            remaining_time=0
            if len(exam)!=0:
                exam1 = exam[0]
                remaining_time=exam1['duration']
                exam_1 = ExamName.objects.get(id=id)
                question_ids = exam_1.questions.values_list('id', flat=True)
                questions_queryset = exam_1.questions.all()
                question_data = questions_queryset[0]
                num_questions = questions_queryset.count()
                user =UsersConfig.objects.get(id=request.session['userid']);
                exam_instances = Start_exam_user.objects.filter(exam=id,user=user)
                examidouser = ""
                ist_time = None
                for instance in exam_instances:
                    examidouser = instance.id
                    ist_time = instance.timestamp.astimezone(timezone('Asia/Kolkata'))
                if(examidouser==""):
                    start_examUser = Start_exam_user(
                        user=user,
                        exam=exam_1,
                        timestamp=datetime.now(timezone('Asia/Kolkata'))
                    )
                    start_examUser.save()
                    messages.success(request, "Exam Started...")
                else:
                    dt = ist_time.replace(second=0, microsecond=0)
                    end_time = dt + timedelta(minutes=remaining_time)
                    current_time = datetime.now(timezone('Asia/Kolkata'))
                    remaining_time = end_time - current_time
                    remaining_time = int(remaining_time.total_seconds() //60)
                    # if remaining_time < 0:
                    #     messages.success(request, "Congratulations on completing the exam successfully! If you have any further questions or need assistance with anything else, feel free to ask.")
                    #     return HttpResponseRedirect('/result_page')
        else:
            messages.success(request, "Handle non-existent exam query gracefully with custom error message.")
    else:
        messages.success(request, "Handle non-existent exam query gracefully with custom error message.")
        return HttpResponseRedirect('/login')

    return render(request, 'start_exam.html',{"user_email":request.session['useremail'],'question_data':question_data,'exam':exam[0],"num_questions":num_questions,"remaining_time":remaining_time})

def startexam(request):
    return render(request, 'start_exam.html')

def get_next_question(request):
    user_email = request.session.get('useremail', None)
    if user_email:
        id = request.POST.get('id')
        if not id:
            return JsonResponse({'error': 'Exam ID is required'}, status=400)
        
        exam_qs = ExamName.objects.filter(id=id)
        if exam_qs.exists():
            exam = exam_qs.first()
            remaining_time = exam.duration
            questions_queryset = exam.questions.order_by('id')
            page_number = request.POST.get('page', 1)
            paginator = Paginator(questions_queryset, 1)
            exam=ExamName.objects.get(id=id)
            user = UsersConfig.objects.get(id=request.session['userid']);
            try:
                page = paginator.page(page_number)
            except EmptyPage:
                return JsonResponse({'error': 'Page not found'}, status=404)
            current_questions = list(page.object_list.values())  
            question_ids = page.object_list.values_list('id', flat=True)
            attempted_questions1 = ""
            if question_ids[0] != "":
                question=Question.objects.get(id=question_ids[0])
                attempted_questions = AttemptedQuestion.objects.filter(
                user=user,
                exam=exam,
                question=question,
                )
                attempted_questions1=attempted_questions.first().chosen_option


            data = {
                'remaining_time': remaining_time,
                'current_questions': current_questions,
                'total_questions': paginator.count,
                'attempted_questions':attempted_questions1
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Exam not found'}, status=404)
    else:
        return JsonResponse({'error': 'Unauthorized'}, status=401)


def save_next(request):
    user_email = request.session.get('useremail', None)
    if user_email:
        user = UsersConfig.objects.get(id=request.session['userid']);
        question=Question.objects.get(id=request.POST.get('qid'))
        is_correct = question.correct_answer==request.POST.get('selectedOption')
        chosen_option=request.POST.get('selectedOption')
        exam=ExamName.objects.get(id=request.POST.get('id'))
        id = request.POST.get('id')
        if not id:
            return JsonResponse({'error': 'Exam ID is required'}, status=400)
        attempted_questions = AttemptedQuestion.objects.filter(
            user=user,
            exam=exam,
            question=question
        )
        if not attempted_questions.exists():
            attempt = AttemptedQuestion(
                user=user,
                question=question,
                chosen_option=chosen_option,
                is_correct=is_correct,
                exam=exam
            )
            attempt.save()
        exam_qs = ExamName.objects.filter(id=id)
        if exam_qs.exists():
            exam = exam_qs.first()
            remaining_time = exam.duration
            questions_queryset = exam.questions.order_by('id')
            page_number = int(request.POST.get('page', 1))
            paginator = Paginator(questions_queryset, 1) 
            try:
                page = paginator.page(page_number)
            except EmptyPage:
                return JsonResponse({'error': 'Page not found'}, status=404)
            current_questions = list(page.object_list.values())
            question_ids = page.object_list.values_list('id', flat=True)
            attempted_questions1 = ""
            if question_ids[0] != "":
                question=Question.objects.get(id=question_ids[0])
                attempted_questions = AttemptedQuestion.objects.filter(
                user=user,
                exam=exam,
                question=question,
                )
                attempted_questions1=attempted_questions.first().chosen_option  
            data = {
                'remaining_time': remaining_time,
                'current_questions': current_questions,
                'total_questions': paginator.count,
                'attempted_questions':attempted_questions1
            }
            return JsonResponse(data)
            