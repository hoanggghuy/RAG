import whisper
import sounddevice as sd
import soundfile as sf


ffmpeg_path = r"C:\ffmpeg-master-latest-win64-gpl-shared\ffmpeg-master-latest-win64-gpl-shared\bin"

def record_audio(filename, duration=5, sample_rate=16000):
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1,dtype="float32")
    print("Starting recording")
    sd.wait()
    sf.write(filename, audio, sample_rate)


def gen_text_from_audio(filename, duration=5, sample_rate=16000):
    audio_file = filename + ".wav"
    record_audio(audio_file, duration, sample_rate)
    result = model.transcribe(audio_file,language="en")
    return result["text"]


if __name__ == "__main__":
    model = whisper.load_model("small")
    while True:
        user_input = input("Enter to record or q to quit: ")
        if user_input.lower() == 'q':
            print("Done")
            break
        print(f"You said:{gen_text_from_audio(filename="test", duration=3)}")
