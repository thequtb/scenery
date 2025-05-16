from django.db import migrations, models
import django.db.models.deletion
import pgvector.django.vector
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('required_fields', models.JSONField(blank=True, default=list)),
                ('optional_fields', models.JSONField(blank=True, default=list)),
                ('prompts', models.JSONField(blank=True, default=dict)),
                ('embedding', pgvector.django.vector.VectorField(blank=True, dimensions=1536, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('collected_data', models.JSONField(blank=True, default=dict)),
                ('agent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='conversations', to='agents.agent')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('user', 'User'), ('assistant', 'Assistant'), ('system', 'System')], default='user', max_length=10)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('conversation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='agents.conversation')),
            ],
        ),
    ] 