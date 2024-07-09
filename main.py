from pydub import AudioSegment
import speech_recognition as sr
import os

audio_file_path = './arquivo3.ogg'
wav_dir = 'wav_parts3'
txt_file_path = 'transcricao3.txt'

if not os.path.exists(wav_dir):
    os.makedirs(wav_dir)

audio = AudioSegment.from_file(audio_file_path)
duration_in_seconds = len(audio) / 1000

parts = []
for i in range(0, int(duration_in_seconds), 30):
    part = audio[i*1000:(i+30)*1000]
    part_wav_path = os.path.join(wav_dir, f'part_{i}.wav')
    part.export(part_wav_path, format="wav")
    parts.append(part_wav_path)

recognizer = sr.Recognizer()

def transcribe_audio(wav_file_path):
    transcription = []
    with sr.AudioFile(wav_file_path) as source:
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language="pt-BR")
            transcription.append(text)
        except sr.UnknownValueError:
            print("Google Web Speech API não entendeu o áudio")
        except sr.RequestError as e:
            print(f"Não foi possível solicitar os resultados do serviço Google Web Speech API; {e}")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
    return ' '.join(transcription)

full_text = ""
for part in parts:
    full_text += transcribe_audio(part) + " "

with open(txt_file_path, 'w', encoding='utf-8') as file:
    file.write(full_text.strip())

print(f'Transcrição salva em {txt_file_path}')
