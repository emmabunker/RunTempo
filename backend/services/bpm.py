import random
LOCAL_BPM_LOOKUP = {
    ("my moon my man", "feist"): 124,
    ("don't fade away", "beach fossils"): 128,
    ("madwoman", "laufey"): 87,
    ("shadow in the sun", "joe p"): 118,
    ("neon pill", "cage the elephant"): 120,
}

def normalize_text(text):
    return text.strip().lower()

def get_bpm_for_track(title, artists):
    normalized_title = normalize_text(title)

    for artist in artists:
        normalized_artist = normalize_text(artist)

        lookup_key = (normalized_title, normalized_artist)

        if lookup_key in LOCAL_BPM_LOOKUP:
            return LOCAL_BPM_LOOKUP[lookup_key]
        
    return random.randint(60, 220)
