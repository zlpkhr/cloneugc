def material_symbols(request):
    return {
        "material_symbols": ",".join(
            sorted(
                [
                    "play_circle",
                    "face",
                    "favorite",
                    "visibility",
                    "share",
                    "check_circle",
                    "person_add",
                    "pause",
                    "voice_selection",
                    "mic"
                ]
            )
        )
    }
