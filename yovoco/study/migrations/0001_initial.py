# Generated by Django 4.0.4 on 2022-05-05 15:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('entities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(default='20220505', max_length=50)),
                ('description', models.CharField(blank=True, default='No description', max_length=200, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'studies_lesson',
            },
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('question', models.CharField(blank=True, max_length=200, null=True)),
                ('answer1', models.CharField(blank=True, default='No answer', max_length=50, null=True)),
                ('answer2', models.CharField(blank=True, default='No answer', max_length=50, null=True)),
                ('answer3', models.CharField(blank=True, default='No answer', max_length=50, null=True)),
                ('correct_answer', models.CharField(blank=True, max_length=50, null=True)),
                ('question_type', models.CharField(choices=[('fm', 'Find Meaning'), ('fw', 'Find Word'), ('fwm', 'Find Word and Meaning'), ('fwi', 'Find Word from Image'), ('fwa', 'Find Word from Audio'), ('fmi', 'Find Mean from Image')], default='fm', max_length=50)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_updated_by', to=settings.AUTH_USER_MODEL)),
                ('vocabulary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entities.vocabulary')),
            ],
            options={
                'db_table': 'studies_quiz',
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(default='20220505', max_length=50)),
                ('description', models.CharField(blank=True, default='No description', max_length=200, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'studies_test',
            },
        ),
        migrations.CreateModel(
            name='QuizContent',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('client_answer', models.CharField(blank=True, max_length=50, null=True)),
                ('test_times', models.IntegerField(default=0)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_content', to='study.quiz')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_content', to='study.test')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'studies_quiz_content',
            },
        ),
        migrations.CreateModel(
            name='LessonItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('typing_count', models.IntegerField(default=0)),
                ('right_count', models.IntegerField(default=0)),
                ('wrong_list', models.CharField(blank=True, max_length=200, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_updated_by', to=settings.AUTH_USER_MODEL)),
                ('vocabulary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entities.vocabulary')),
            ],
            options={
                'db_table': 'studies_lesson_item',
            },
        ),
        migrations.CreateModel(
            name='LessonContent',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_content', to='study.lessonitem')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lesson_content', to='study.lesson')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'studies_lesson_content',
            },
        ),
    ]
