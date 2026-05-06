import os
import django
from django.conf import settings
from django.db import models, connection
from django.core.management import call_command
from django.db.migrations.executor import MigrationExecutor
from django.db.migrations.state import ProjectState

