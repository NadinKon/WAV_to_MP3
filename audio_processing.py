from pydub import AudioSegment


def convert_to_mp3(wav_data):
    audio = AudioSegment.from_wav(wav_data)
    mp3_data = audio.export(format='mp3')
    return mp3_data.read()
