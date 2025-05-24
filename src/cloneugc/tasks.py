from celery import shared_task

from cloneugc.models import Actor
from cloneugc.services import voice_cloner
from cloneugc.utils import extract_audio


@shared_task
def clone_actor(actor_id: str, script: str):
    actor = Actor.objects.get(id=actor_id)

    if not actor.voice_cloned:
        temp_audio = extract_audio(actor.video.url)

        with open(temp_audio, "rb") as audio_file:
            actor.voice_id = voice_cloner.clone_voice(actor.name, audio_file)
            actor.save()
