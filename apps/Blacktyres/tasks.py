from celery import shared_task
from .parser import main
import asyncio


@shared_task
def run_blacktyres_parser():
    asyncio.run(main())
