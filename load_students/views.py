from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from django.contrib.auth.models import User
from main.models import UserProfile, Group

from .forms import StudentForm

from django.contrib.auth.hashers import make_password
from teacher.helpers import generate_password

from collections import defaultdict

def form(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        form = StudentForm(request.POST)

        if form.is_valid():
            return HttpResponseRedirect('load_students/process/')
    else:
        form = StudentForm()

    return render(request, 'student_data.html', {'form': form})

def process(request):
    students = request.POST.get('students', '').split('\n')
    incorrect = []
    id_exists = []
    no_group = []
    groups = defaultdict(int)
    for line in students:
        s = line.split(',')
        if len(s) != 4:
            incorrect.append(line)
        else:
            student_id, first, last, group = [e.strip() for e in s]

            if User.objects.filter(username=student_id).exists():
                id_exists.append(line)
            elif not Group.objects.filter(title=group).exists():
                no_group.append(line)
            else:
                group = Group.objects.get(title=group)
                pw = generate_password('-')
                
                user = User.objects.create(username=student_id,
                        first_name=first, last_name=last,
                        email=student_id+'@limes.nl',
                        password=make_password(pw))

                profile = UserProfile(user=user, code=group.leader.userprofile.code)
                profile.save()
                profile.groups.add(group)
                profile.save()

                groups[group.title] += 1
    
    return render(request, 'data_results.html', {'groups': dict(groups),
            'incorrect': incorrect, 'id_exists': id_exists, 'no_group': no_group})

