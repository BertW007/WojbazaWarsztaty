import random

from django.http.response import HttpResponse
from django.shortcuts import render, redirect
import rest_framework
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic.base import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from rest_framework.reverse import reverse

from simcourse.models import Player, PlayerStats, CourseProgress, Exams, ExamResult


class PlayerCreate(CreateView):
    model = Player
    fields = '__all__'
    success_url = reverse_lazy('new_stats')


class StatsCreate(CreateView):
    model = PlayerStats
    fields = ('sleep_state', 'mental_state', 'knowledge_state')
    success_url = reverse_lazy('create_progress')
    slug_field = 'stats_id'  # tym się zamienia id gracza na id relacji
    slug_url_kwarg = 'stats_id'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.stats = Player.objects.order_by('id').last()
        self.object.save()
        return redirect(self.get_success_url())

class ProgressCreate(CreateView):
    model = CourseProgress
    fields = ()
    success_url = reverse_lazy('create_exam')
    slug_field = 'related_to_id'  # tym się zamienia id gracza na id relacji
    slug_url_kwarg = 'related_to_id'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.related_to = Player.objects.order_by('id').last()
        self.object.save()
        return redirect(self.get_success_url())

class ExamCreate(CreateView):
    model = Exams
    fields = ()
    success_url = reverse_lazy('create_result')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.relation = Player.objects.order_by('id').last()
        self.object.save()
        return redirect(self.get_success_url())


class ResultCreate(CreateView):
    model = ExamResult
    fields = ()
    success_url = reverse_lazy('main_menu')
    slug_field = 'related_to_id'  # tym się zamienia id gracza na id relacji
    slug_url_kwarg = 'related_to_id'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.related_to = Player.objects.order_by('id').last()
        self.object.save()
        return redirect(self.get_success_url())


class PlayerDelete(DeleteView):
    model = Player
    success_url = reverse_lazy('main_menu')


class PlayerUpdate(UpdateView):
    model = Player
    fields = "__all__"
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('main_menu')

class ProgressUpdate(UpdateView):
    model = CourseProgress
    fields = "__all__"
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('main_menu')
    slug_field = 'related_to_id'  # tym się zamienia id gracza na id relacji
    slug_url_kwarg = 'related_to_id'

class StatsUpdate(UpdateView):
    model = PlayerStats
    fields = "__all__"
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('main_menu')
    slug_field = 'stats_id'  # tym się zamienia id gracza na id relacji
    slug_url_kwarg = 'stats_id'  #


# start szaberzone
#  'player': Player.objects.get(pk=player_id),
#             'stats': PlayerStats.objects.filter(stats=player_id),
#             'day_of_the_course': CourseProgress.objects.filter(related_to=player_id), #import
#                                                                                        from dump world to szaber
#             'exams': Exams.objects.filter(relation=player_id)
#
# sleep_state = models.IntegerField(choices=SLEEP_STATE)
# mental_state = models.IntegerField(choices=MENTAL_STATE)
# knowledge_state = models.IntegerField(choices=KNOWLEDGE_STATE)
# stats = models.OneToOneField(Player, on_delete=models.CASCADE)
# endszaberzone


class MainMenuView(View):
    def get(self, request):
        ctx = {
            'players': Player.objects.all(),
            'stats': PlayerStats.objects.all(),
            'day_of_the_course': CourseProgress.objects.all(),
            'exam': Exams.objects.all(),
            'results': ExamResult.objects.all()
        }
        return render(request, 'simcourse/main_menu.html', ctx)


class TheMorningView(View):  # view only checks stats and progress, no action forward
    def get(self, request, player_id):
        ctx = {
            'player': Player.objects.get(pk=player_id),
            'stats': PlayerStats.objects.filter(stats=player_id),
            'day_of_the_course': CourseProgress.objects.get(related_to=player_id),
            'exams': Exams.objects.filter(relation=player_id),


        }
        if ctx['day_of_the_course'].day_of_course == 11:
            return redirect(f"/demo_final/{player_id}")
        else:
            return render(request, 'simcourse/the_morning.html', ctx)

    def post(self, request, player_id):
        progress = CourseProgress.objects.get(related_to=player_id)
        stats_check = PlayerStats.objects.get(stats=player_id)
        stats_check.mental_state = random.randint(1, 5)  # modifies mood life is brutal
        stats_check.save()
        if stats_check.knowledge_state > 6:
            stats_check.knowledge_state = 6
            stats_check.save()
        elif stats_check.knowledge_state < 1:
            stats_check.knowledge_state = 1
            stats_check.save()
        elif stats_check.sleep_state > 6:
            stats_check.sleep_state = 6
            stats_check.save()
        elif stats_check.sleep_state < 1:
            stats_check.sleep_state = 1
            stats_check.save()
        elif stats_check.mental_state > 6:
            stats_check.mental_state = 6
            stats_check.save()  # check for stats integrity
        elif stats_check.sleep_state < 1:
            stats_check.sleep_state = 1
            stats_check.save()
        elif progress.day_of_course == 9:
            return redirect(f"/exam1_intro/{player_id}")
        elif progress.day_of_course == 23:
            return redirect(f"/exam2_intro/{player_id}")  # bushes test check for exams
        elif progress.day_of_course == 37:
            return redirect(f"/exam3_intro/{player_id}")
        elif progress.day_of_course == 51:
            return redirect(f"/exam4_intro/{player_id}")
        elif progress.day_of_course == 65:
            return redirect(f"/exam5_intro/{player_id}")
        elif progress.day_of_course > 65:
            return redirect(f"/end_of_course/{player_id}")
        # elif progress.day_of_course % 2 == 0: checks if not morning reverses one phase
        #     progress.day_of_course -= 1
        #     progress.save()
        else:
            return redirect(f"/the_morning/{player_id}")  # redirects after submit idz do szkoly

class DemoFinalView(View):
    def get(self, request, player_id):
        ctx = {
            'player': Player.objects.get(pk=player_id),
            'stats': PlayerStats.objects.filter(stats=player_id),
            'day_of_the_course': CourseProgress.objects.filter(related_to=player_id),
            'exams': Exams.objects.filter(relation=player_id),
            'results': ExamResult.objects.get(related_to=player_id)
        }
        return render(request, 'simcourse/demo_final.html', ctx)



class GoToSchoolView(View):  # action view
    def get(self, request, player_id):
        ctx = {
            'player': Player.objects.get(pk=player_id),
            'stats': PlayerStats.objects.filter(stats=player_id),
            'day_of_the_course': CourseProgress.objects.filter(related_to=player_id),
            'exams': Exams.objects.filter(relation=player_id)
        }
        return render(request, 'simcourse/go_to_school.html', ctx)

    def post(self, request, player_id):
        progress_counter = CourseProgress.objects.get(related_to=player_id)  # roll up to next phase
        sleep_stat__up = PlayerStats.objects.get(stats=player_id)  # sleep attribute up 1
        sleep_stat__up.knowledge_state += 1  # this adds knowledge
        sleep_stat__up.save()
        progress_counter.day_of_course += 1  # this rolls progress forward
        progress_counter.save()
        if sleep_stat__up.knowledge_state > 6:
            sleep_stat__up.knowledge_state = 6
            sleep_stat__up.save()
        else:
            pass
        if sleep_stat__up.knowledge_state < 1:
            sleep_stat__up.knowledge_state = 1
            sleep_stat__up.save()
        else:
            pass
        if sleep_stat__up.mental_state > 6:
            sleep_stat__up.mental_state = 6
            sleep_stat__up.save()  # check for stats integrity
        else:
            pass
        if sleep_stat__up.mental_state < 1:
            sleep_stat__up.mental_state = 1
            sleep_stat__up.save()
        else:
            pass
        return redirect(f"/go_to_school/{player_id}")


class GoSleepInsteadSchoolView(View):  # action get sleep instead school result screen
    def get(self, request, player_id):
        ctx = {
            'player': Player.objects.get(pk=player_id),
            'stats': PlayerStats.objects.filter(stats=player_id),
            'day_of_the_course': CourseProgress.objects.filter(related_to=player_id),
            'exams': Exams.objects.filter(relation=player_id)
        }
        return render(request, 'simcourse/add_sleep.html', ctx)

    def post(self, request, player_id):
        progress_counter = CourseProgress.objects.get(related_to=player_id)  # roll up to next phase
        sleep_stat__up = PlayerStats.objects.get(stats=player_id)  # sleep attribute up 1
        sleep_stat__up.knowledge_state -= 1  # this adds knowledge
        sleep_stat__up.sleep_state += 1  # sleep attribute up 1
        sleep_stat__up.save()
        sleep_stat__up.mental_state = random.randint(1, 5)  # modifies mood life is brutal
        sleep_stat__up.save()
        progress_counter.day_of_course += 1
        progress_counter.save()
        if sleep_stat__up.knowledge_state > 6:
            sleep_stat__up.knowledge_state = 6
            sleep_stat__up.save()
        else:
            pass
        if sleep_stat__up.knowledge_state < 1:
            sleep_stat__up.knowledge_state = 1
            sleep_stat__up.save()
        else:
            pass
        if sleep_stat__up.sleep_state > 6:
            sleep_stat__up.sleep_state = 6
            sleep_stat__up.save()
        else:
            pass
        if sleep_stat__up.sleep_state < 1:
            sleep_stat__up.sleep_state = 1
            sleep_stat__up.save()
        else:
            pass
        if sleep_stat__up.mental_state > 6:
            sleep_stat__up.mental_state = 6
            sleep_stat__up.save()  # check for stats integrity
        else:
            pass
        if sleep_stat__up.mental_state < 1:
            sleep_stat__up.sleep_state = 1
            sleep_stat__up.save()
        else:
            pass
        return redirect(f"/add_sleep/{player_id}")


# adresy /bla/ nie dodają urli do siebie , bla/ nie

class AfterSchoolView(View):  # nothing happens in this view, redirector
    def get(self, request, player_id):
        ctx = {
            'player': Player.objects.get(pk=player_id),
            'stats': PlayerStats.objects.filter(stats=player_id),
            'day_of_the_course': CourseProgress.objects.filter(related_to=player_id),
            'exams': Exams.objects.filter(relation=player_id)

        }
        return render(request, 'simcourse/after_school.html', ctx)


class AfterDaySleepView(View):  # display view
    def get(self, request, player_id):
        ctx = {
            'player': Player.objects.get(pk=player_id),
            'stats': PlayerStats.objects.filter(stats=player_id),
            'day_of_the_course': CourseProgress.objects.filter(related_to=player_id),
            'exams': Exams.objects.filter(relation=player_id)

        }
        return render(request, 'simcourse/after_day_sleep.html', ctx)

class GoodNightSleepView(View):  # action view
    def get(self, request, player_id):
        ctx = {
            'player': Player.objects.get(pk=player_id),
            'stats': PlayerStats.objects.filter(stats=player_id),
            'day_of_the_course': CourseProgress.objects.filter(related_to=player_id),
            'exams': Exams.objects.filter(relation=player_id)
        }
        return render(request, 'simcourse/good_night_sleep.html', ctx)

    def post(self, request, player_id):
        progress_counter = CourseProgress.objects.get(related_to=player_id)  # roll up to next phase
        sleep_stat__up = PlayerStats.objects.get(stats=player_id)  # sleep attribute up 1
        sleep_stat__up.sleep_state += 1  # this adds knowledge
        sleep_stat__up.mental_state = random.randint(3, 6)
        sleep_stat__up.save()
        progress_counter.day_of_course += 1  # this rolls progress forward
        progress_counter.save()
        if sleep_stat__up.knowledge_state > 6:
            sleep_stat__up.knowledge_state = 6
            sleep_stat__up.save()
        else:
            pass
        if sleep_stat__up.knowledge_state < 1:
            sleep_stat__up.knowledge_state = 1
            sleep_stat__up.save()
        else:
            pass
        if sleep_stat__up.mental_state > 6:
            sleep_stat__up.mental_state = 6
            sleep_stat__up.save()  # check for stats integrity
        else:
            pass
        if sleep_stat__up.mental_state < 1:
            sleep_stat__up.mental_state = 1
            sleep_stat__up.save()
        else:
            pass
        return redirect(f"/go_to_school/{player_id}")



class WentPartyView(View):  # action view
    def get(self, request, player_id):
        ctx = {
            'player': Player.objects.get(pk=player_id),
            'stats': PlayerStats.objects.filter(stats=player_id),
            'day_of_the_course': CourseProgress.objects.filter(related_to=player_id),
            'exams': Exams.objects.filter(relation=player_id)

        }
        return render(request, 'simcourse/went_party.html', ctx)

    def post(self, request, player_id):
        progress_counter = CourseProgress.objects.get(related_to=player_id)  # roll up to next phase
        party_stats_mod = PlayerStats.objects.get(stats=player_id)  # sleep attribute up 1
        party_stats_mod.knowledge_state -= 1  # this adds knowledge
        party_stats_mod.sleep_state -= 1  # sleep attribute up 1
        party_stats_mod.mental_state += 1
        party_stats_mod.save()
        party_stats_mod.mental_state = random.randint(1, 5)  # modifies mood life is brutal
        party_stats_mod.save()
        progress_counter.day_of_course += 1
        progress_counter.save()
        if party_stats_mod.knowledge_state > 6:
            party_stats_mod.knowledge_state = 6
            party_stats_mod.save()
        else:
            pass
        if party_stats_mod.knowledge_state < 1:
            party_stats_mod.knowledge_state = 1
            party_stats_mod.save()
        else:
            pass
        if party_stats_mod.sleep_state > 6:
            party_stats_mod.sleep_state = 6
            party_stats_mod.save()
        else:
            pass
        if party_stats_mod.sleep_state < 1:
            party_stats_mod.sleep_state = 1
            party_stats_mod.save()
        else:
            pass
        if party_stats_mod.mental_state > 6:
            party_stats_mod.mental_state = 6
            party_stats_mod.save()  # check for stats integrity
        else:
            pass
        if party_stats_mod.mental_state < 1:
            party_stats_mod.sleep_state = 1
            party_stats_mod.save()
        else:
            pass
        return redirect(f"/went_party/{player_id}")


class NightSleep(View):
    def get(self, request, player_id):
        ctx = {
            'player': Player.objects.get(pk=player_id),
            'stats': PlayerStats.objects.filter(stats=player_id),
            'day_of_the_course': CourseProgress.objects.filter(related_to=player_id),
            'exams': Exams.objects.filter(relation=player_id)
        }
        return render(request, 'simcourse/night_sleep.html', ctx)

    def post(self, request, player_id):
        progress_counter = CourseProgress.objects.get(related_to=player_id)  # roll up to next phase
        sleep_stat__up = PlayerStats.objects.get(stats=player_id)  # sleep attribute up 1
        sleep_stat__up.sleep_state += 1  # sleep attribute up 1
        sleep_stat__up.mental_state += 1  # mental state plus 1
        sleep_stat__up.save()
        progress_counter.day_of_course += 1
        progress_counter.save()
        if sleep_stat__up.sleep_state > 6:
            sleep_stat__up.sleep_state = 6
            sleep_stat__up.save()
        else:
            pass
        if sleep_stat__up.sleep_state < 1:
            sleep_stat__up.sleep_state = 1
            sleep_stat__up.save()
        else:
            pass
        if sleep_stat__up.mental_state > 6:
            sleep_stat__up.mental_state = 6
            sleep_stat__up.save()  # check for stats integrity
        else:
            pass
        if sleep_stat__up.mental_state < 1:
            sleep_stat__up.sleep_state = 1
            sleep_stat__up.save()
        else:
            pass
        return redirect(f"/night_sleep/{player_id}")  # zrób view DoneSleepNight


class DoneHomework(View):
    def get(self, request, player_id):
        ctx = {
            'player': Player.objects.get(pk=player_id),
            'stats': PlayerStats.objects.filter(stats=player_id),
            'day_of_the_course': CourseProgress.objects.filter(related_to=player_id),
            'exams': Exams.objects.filter(relation=player_id)
        }
        return render(request, 'simcourse/done_homework.html', ctx)

        #

    def post(self, request, player_id):
        # import pdb;pdb.set_trace()     #debugger
        progress_counter = CourseProgress.objects.get(related_to=player_id)  # roll up to next phase
        homework_done_stats = PlayerStats.objects.get(stats=player_id)  # sleep attribute up 1
        homework_done_stats.knowledge_state += 1  # this adds/deducts knowledge
        homework_done_stats.sleep_state -= 1  # sleep attribute
        homework_done_stats.save()
        homework_done_stats.mental_state += 1
        homework_done_stats.save()
        progress_counter.day_of_course += 1
        progress_counter.save()
        if homework_done_stats.knowledge_state > 6:
            homework_done_stats.knowledge_state = 6
            homework_done_stats.save()
        else:
            pass
        if homework_done_stats.knowledge_state < 1:
            homework_done_stats.knowledge_state = 1
            homework_done_stats.save()
        else:
            pass
        if homework_done_stats.sleep_state > 6:
            homework_done_stats.sleep_state = 6
            homework_done_stats.save()
        else:
            pass
        if homework_done_stats.sleep_state < 1:
            homework_done_stats.sleep_state = 1
            homework_done_stats.save()
        else:
            pass
        if homework_done_stats.mental_state > 6:
            homework_done_stats.mental_state = 6
            homework_done_stats.save()  # check for stats integrity
        else:
            pass
        if homework_done_stats.mental_state < 1:
            homework_done_stats.sleep_state = 1
            homework_done_stats.save()
        else:
            pass
        return redirect(f"/done_homework/{player_id}")


class LearnAfterSleptView(View):
    def get(self, request, player_id):
        ctx = {
            'player': Player.objects.get(pk=player_id),
            'stats': PlayerStats.objects.filter(stats=player_id),
            'day_of_the_course': CourseProgress.objects.filter(related_to=player_id),
            'exams': Exams.objects.filter(relation=player_id)

        }
        return render(request, 'simcourse/learn_after_slept.html', ctx)

    def post(self, request, player_id):
        progress_counter = CourseProgress.objects.get(related_to=player_id)  # roll up to next phase
        chase_knowledge = PlayerStats.objects.get(stats=player_id)  # sleep attribute up 1
        chase_knowledge.knowledge_state += 1  # this adds knowledge
        chase_knowledge.sleep_state -= 1
        chase_knowledge.mental_state = random.randint(1, 3)  # modifies mood life is brutal
        chase_knowledge.save()
        progress_counter.day_of_course += 1  # this rolls progress forward
        progress_counter.save()
        if chase_knowledge.knowledge_state > 6:
            chase_knowledge.knowledge_state = 6
            chase_knowledge.save()
        else:
            pass
        if chase_knowledge.knowledge_state < 1:
            chase_knowledge.knowledge_state = 1
            chase_knowledge.save()
        else:
            pass
        if chase_knowledge.mental_state > 6:
            chase_knowledge.mental_state = 6
            chase_knowledge.save()  # check for stats integrity
        else:
            pass
        if chase_knowledge.mental_state < 1:
            chase_knowledge.mental_state = 1
            chase_knowledge.save()
        else:
            pass
        return redirect(f"/learn_after_slept/{player_id}")


class SleepEvenMoreView(View):
    def get(self, request, player_id):
        ctx = {
            'player': Player.objects.get(pk=player_id),
            'stats': PlayerStats.objects.filter(stats=player_id),
            'day_of_the_course': CourseProgress.objects.filter(related_to=player_id),
            'exams': Exams.objects.filter(relation=player_id)

        }
        return render(request, 'simcourse/sleep_even_more.html', ctx)

    def post(self, request, player_id):
        progress_counter = CourseProgress.objects.get(related_to=player_id)  # roll up to next phase
        more_sleep = PlayerStats.objects.get(stats=player_id)  # sleep attribute up 1
        more_sleep.knowledge_state -= 1  # this adds knowledge
        more_sleep.sleep_state += 1
        more_sleep.mental_state = random.randint(3, 5)  # modifies mood life is brutal
        more_sleep.save()
        progress_counter.day_of_course += 1  # this rolls progress forward
        progress_counter.save()
        if more_sleep.knowledge_state > 6:
            more_sleep.knowledge_state = 6
            more_sleep.save()
        else:
            pass
        if more_sleep.knowledge_state < 1:
            more_sleep.knowledge_state = 1
            more_sleep.save()
        else:
            pass
        if more_sleep.mental_state > 6:
            more_sleep.mental_state = 6
            more_sleep.save()  # check for stats integrity
        else:
            pass
        if more_sleep.mental_state < 1:
            more_sleep.mental_state = 1
            more_sleep.save()
        else:
            pass
        return redirect(f"/sleep_even_more/{player_id}")


class Exam1IntroView(View):
    def get(self, request, player_id):
        ctx = {
            'player': Player.objects.get(pk=player_id),
            'stats': PlayerStats.objects.filter(stats=player_id),
            'day_of_the_course': CourseProgress.objects.filter(related_to=player_id),
            'exams': Exams.objects.filter(relation=player_id),

        }
        return render(request, 'simcourse/exam1_intro.html', ctx)


class Exam1ActionView(View):
    def get(self, request, player_id):
        ctx = {
            'player': Player.objects.get(pk=player_id),
            'stats': PlayerStats.objects.filter(stats=player_id),
            'day_of_the_course': CourseProgress.objects.filter(related_to=player_id),
            'exams': Exams.objects.filter(relation=player_id),
            'result': ExamResult.objects.filter(related_to=player_id)

        }
        return render(request, 'simcourse/exam1_action.html', ctx)

    def post(self, request, player_id):
        # progress_summary = CourseProgress.objects.get(related_to=player_id)  # roll up to next phase
        # stats_summary = PlayerStats.objects.get(stats=player_id)  # sleep attribute up 1
        # exams = Exams.objects.filter(relation=player_id)
        exam = ExamResult.objects.get(related_to=player_id)
        exam.result = random.randint(1, 7)
        exam.save()
        # progress_summary.day_of_course += 1  # this rolls progress forward cut in moment forward down
        # progress_summary.save()
        return redirect(f"/exam1_action/{player_id}")


class ChickenView(View):
    def get(self, request, player_id):
        ctx = {
            'player': Player.objects.get(pk=player_id),
            'stats': PlayerStats.objects.filter(stats=player_id),
            'day_of_the_course': CourseProgress.objects.filter(related_to=player_id),
            'exams': Exams.objects.filter(relation=player_id),
            'result': ExamResult.objects.filter(related_to=player_id)

        }
        return render(request, 'simcourse/chicken_form.html', ctx)


class ExamCheckView(View):
    def post(self, request, player_id):
        exam = ExamResult.objects.get(related_to=player_id)
        progress_summary = CourseProgress.objects.get(related_to=player_id)
        if exam.result <= 3:
            progress_summary.day_of_course += 1  # this rolls progress forward
            progress_summary.save()
            return redirect(f"/exam_failed/{player_id}")
        else:
            progress_summary.day_of_course += 2  # this rolls progress forward
            progress_summary.save()
            return redirect(f"/exam_passed/{player_id}")


class ExamPassedView(View):
    def get(self, request, player_id):
        ctx = {
            'player': Player.objects.get(pk=player_id),
            'stats': PlayerStats.objects.filter(stats=player_id),
            'day_of_the_course': CourseProgress.objects.filter(related_to=player_id),
            'exams': Exams.objects.filter(relation=player_id),
            'result': ExamResult.objects.get(related_to=player_id)

        }
        return render(request, 'simcourse/exam_passed.html', ctx)


class ExamFailedView(View):
    def get(self, request, player_id):
        ctx = {
            'player': Player.objects.get(pk=player_id),
            'stats': PlayerStats.objects.filter(stats=player_id),
            'day_of_the_course': CourseProgress.objects.filter(related_to=player_id),
            'exams': Exams.objects.filter(relation=player_id),
            'result': ExamResult.objects.get(related_to=player_id)

        }
        return render(request, 'simcourse/exam_failed.html', ctx)
