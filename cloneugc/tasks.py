from celery import shared_task
from django.core.files.base import ContentFile

from cloneugc.models import Generation
from cloneugc.services import lipsyncer, voice_cloner
from cloneugc.utils import extract_audio, reverse_absolute


@shared_task
def clone_actor(gen_id: str, script: str):
    gen = Generation.objects.get(id=gen_id)

    if not gen.actor.voice_cloned:
        gen.status = "First generation: cloning voice"
        gen.save()

        temp_audio = extract_audio(gen.actor.video.url)

        with open(temp_audio, "rb") as audio_file:
            gen.actor.voice_id = voice_cloner.clone_voice(gen.actor.name, audio_file)
            gen.actor.save()

    gen.status = "Generating audio from script"
    gen.save()

    audio = voice_cloner.tts(gen.actor.voice_id, script)

    gen.audio.save(f"{gen.actor.name}.mp3", ContentFile(audio))

    gen.status = "Syncing lips"
    gen.save()

    request_id = lipsyncer.lipsync(
        gen.actor.video.url, gen.audio.url, reverse_absolute("lipsyncer_callback")
    )

    gen.lipsync_request_id = request_id
    gen.save()
