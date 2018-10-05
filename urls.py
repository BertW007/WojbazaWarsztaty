
from django.conf.urls import url
from django.contrib import admin

from simcourse.views import StatsCreate, PlayerCreate, PlayerDelete, PlayerUpdate, \
    StatsUpdate, ProgressCreate, ExamCreate, AfterSchoolView, WentPartyView, NightSleep, \
    DoneHomework, AfterDaySleepView, LearnAfterSleptView, SleepEvenMoreView, MainMenuView, TheMorningView, \
    GoToSchoolView, GoSleepInsteadSchoolView, Exam1IntroView, Exam1ActionView, ResultCreate, ExamCheckView, \
    ExamPassedView, ExamFailedView, ChickenView, GoodNightSleepView, ProgressUpdate, DemoFinalView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('new_player', PlayerCreate.as_view(), name="new_player"),
    url('new_stats', StatsCreate.as_view(), name="new_stats"),
    url('create_result', ResultCreate.as_view(), name="create_result"),
    url(r'^the_morning/(?P<player_id>(\d)+)', TheMorningView.as_view(), name="the_morning"),  # view_stats
    url('main_menu', MainMenuView.as_view(), name="main_menu"),  # view_players
    url('delete_player/(?P<pk>(\d)+)', PlayerDelete.as_view(), name="delete_player"),
    url('update_player/(?P<pk>(\d)+)', PlayerUpdate.as_view(), name="update_player"),
    url('update_stats/(?P<stats_id>(\d)+)', StatsUpdate.as_view(), name="update_stats"),
    url('create_progress', ProgressCreate.as_view(), name="create_progress"),
    url('create_exam', ExamCreate.as_view(), name="create_exam"),
    url('go_to_school/(?P<player_id>(\d)+)', GoToSchoolView.as_view(), name="go_to_school"),  # addd_knowledge
    url('add_sleep/(?P<player_id>(\d)+)', GoSleepInsteadSchoolView.as_view(), name="add_sleep"),
    url('after_school/(?P<player_id>(\d)+)', AfterSchoolView.as_view(), name="after_school"),
    url('went_party/(?P<player_id>(\d)+)', WentPartyView.as_view(), name="went_party"),
    url('night_sleep/(?P<player_id>(\d)+)', NightSleep.as_view(), name="night_sleep"),
    url('done_homework/(?P<player_id>(\d)+)', DoneHomework.as_view(), name="done_homework"),
    url('after_day_sleep/(?P<player_id>(\d)+)', AfterDaySleepView.as_view(), name="after_day_sleep"),
    url('learn_after_slept/(?P<player_id>(\d)+)', LearnAfterSleptView.as_view(), name="learn_after_slept"),
    url('sleep_even_more/(?P<player_id>(\d)+)', SleepEvenMoreView.as_view(), name="sleep_even_more"),
    url('exam1_intro/(?P<player_id>(\d)+)', Exam1IntroView.as_view(), name="exam1_intro"),
    url('exam1_action/(?P<player_id>(\d)+)', Exam1ActionView.as_view(), name="exam1_action"),
    url('exam_check/(?P<player_id>(\d)+)', ExamCheckView.as_view(), name='exam_check'),
    url('exam_chicken/(?P<player_id>(\d)+)', ChickenView.as_view(), name="exam_chicken"),
    url('exam_passed/(?P<player_id>(\d)+)', ExamPassedView.as_view(), name="exam_passed"),
    url('exam_failed/(?P<player_id>(\d)+)', ExamFailedView.as_view(), name="exam_failed"),
    # url('exam1_redo_screen/(?P<player_id>(\d)+)', Exam1RedoScreenView.asView), name = "exam1_redo_screen"),
    # url('exam1_redo_pass/(?P<player_id>(\d)+)', Exam1RedoPassView.asView), name = "exam1_rdo_pass"),
    url('good_night_sleep/(?P<player_id>(\d)+)', GoodNightSleepView.as_view, name="good_night_sleep"),
    # url('game_over_screen/(?P<player_id>(\d)+)', GameOverScreenView.asView), name="game_over_screen"),
    url('update_progress/(?P<pk>(\d)+)', ProgressUpdate.as_view(), name="update_progress"),
    url('demo_final/(?P<player_id>(\d)+)', DemoFinalView.as_view(), name="update_progress"),

]

