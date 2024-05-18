from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UsersConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=50, unique=True)),  # Add unique constraint here
                ('password', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=15)),
                ('state', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=10)),
            ],
        ),
    ]
