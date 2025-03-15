import subprocess
from celery import shared_task
from django.conf import settings


@shared_task
def backup_database():
    if settings.DEV_MOD:
        backup_script = '../../scripts/backup_db.sh'
        result = subprocess.run([backup_script], shell=True, capture_output=True, text=True)
    else:
        backup_script = "/app/scripts/backup_db.sh"
        result = subprocess.run([backup_script], shell=True, capture_output=True, text=True)
    return f"Бэкап базы данных успешно завершена: {result.stdout}"

@shared_task
def backup_media():
    if settings.DEV_MOD:
        backup_script = '../../scripts/backup_media.sh'
        result = subprocess.run([backup_script], shell=True, capture_output=True, text=True)
    else:
        backup_script = "/app/scripts/backup_media.sh"
        result = subprocess.run([backup_script], shell=True, capture_output=True, text=True)
    return f"Бэкап медиа файлов успешно завершена: {result.stdout}"
