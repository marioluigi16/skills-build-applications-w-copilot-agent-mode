from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Drop collections directly using Djongo's database connection for robust cleanup
        from django.db import connection
        db = connection.cursor().db_conn.client[connection.settings_dict['NAME']]
        db.leaderboard.drop()
        db.activity.drop()
        db.workout.drop()
        db.user.drop()
        db.team.drop()

        # Create teams
        marvel = Team.objects.create(name='marvel', description='Marvel Team')
        dc = Team.objects.create(name='dc', description='DC Team')

        # Create users (reference Team objects directly)
        tony = User.objects.create(name='Tony Stark', email='tony@marvel.com', team=marvel)
        steve = User.objects.create(name='Steve Rogers', email='steve@marvel.com', team=marvel)
        bruce = User.objects.create(name='Bruce Wayne', email='bruce@dc.com', team=dc)
        clark = User.objects.create(name='Clark Kent', email='clark@dc.com', team=dc)

        # Create activities
        Activity.objects.create(user=tony, activity_type='run', duration=30, date=timezone.now().date())
        Activity.objects.create(user=steve, activity_type='cycle', duration=45, date=timezone.now().date())
        Activity.objects.create(user=bruce, activity_type='swim', duration=60, date=timezone.now().date())
        Activity.objects.create(user=clark, activity_type='yoga', duration=20, date=timezone.now().date())

        # Create workouts
        Workout.objects.create(name='Super Strength', description='Strength workout for heroes', suggested_for='marvel')
        Workout.objects.create(name='Flight Training', description='Flight workout for heroes', suggested_for='dc')

        # Create leaderboard
        Leaderboard.objects.create(user=tony, score=100, rank=1)
        Leaderboard.objects.create(user=steve, score=90, rank=2)
        Leaderboard.objects.create(user=bruce, score=80, rank=3)
        Leaderboard.objects.create(user=clark, score=70, rank=4)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
