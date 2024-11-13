from moviepy.editor import VideoFileClip, ImageClip, AudioFileClip, concatenate_audioclips, TextClip, CompositeVideoClip
import random
from gtts import gTTS
from mutagen.mp3 import MP3
import io

from google.oauth2 import service_account
from google.cloud import speech, texttospeech




def create_audio_file(file_name, output_file_name):
    with open(file_name, "r") as file:
        main_text = file.read()

    # Creating audio from content
    tts = gTTS(text=main_text, lang='en', slow=False)
    tts.save(output_file_name)
    return AudioFileClip(output_file_name)


def create_audio_file_google_api(file_name, output_file_name, ssml_gender, voice_name):

    client_file = 'auth/sa.json'
    client = texttospeech.TextToSpeechClient.from_service_account_file(client_file)

    with open(file_name, "r") as file:
        main_text = file.read()
    synthesis_input = texttospeech.SynthesisInput(text=main_text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=voice_name,
        ssml_gender=ssml_gender
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=1.2
    )

    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    with open(output_file_name, "wb") as out:
        out.write(response.audio_content)

    return AudioFileClip(output_file_name)


def cut_background_video(main_audio_length, title_audio_length):
    # Creating video length based on audio length
    audio_length = main_audio_length + title_audio_length
    max_value = 433 - int(audio_length)
    random_number = random.randint(1, max_value)
    start_time = random_number
    end_time = start_time + audio_length

    video = VideoFileClip("background_videos/background_4.mov")
    cut_video = video.subclip(start_time, end_time)
    return cut_video


for x in range(5):

    i = x+1
    main_text_audio = create_audio_file_google_api(f"content/main_text_{i}.txt", f"audio_files/main_text_audio_{i}.wav", texttospeech.SsmlVoiceGender.NEUTRAL, "en-US-Standard-C")
    title_text_audio = create_audio_file_google_api(f"content/title_text_{i}.txt", f"audio_files/title_text_audio_{i}.wav", texttospeech.SsmlVoiceGender.NEUTRAL, "en-US-Standard-B")


    cut_video = cut_background_video(main_text_audio.duration, title_text_audio.duration)

    # Add audio to clip
    combined_audio = concatenate_audioclips([title_text_audio, main_text_audio])
    combined_audio.write_audiofile(
        f"audio_files/combined_audio_{i}.wav",
        codec="pcm_s16le",     # Linear16 format
        fps=16000,             # 16kHz sample rate
        nbytes=2,              # 16-bit depth
    )
    video_with_audio = cut_video.set_audio(combined_audio)

    # Set screenshot
    screenshot = ImageClip(f"content/screenshot_{i}.png")
    screenshot = screenshot.resize(width=900)
    screenshot = screenshot.set_start(0).set_end(title_text_audio.duration)
    screenshot = screenshot.set_position(("center", video_with_audio.h * 0.25))


    # Add subtitles
    text_clips = []
    outline_text_clips = []
    client_file = 'auth/sa.json'
    credentials = service_account.Credentials.from_service_account_file(client_file)
    client = speech.SpeechClient(credentials=credentials)

    audio_file = f'audio_files/main_text_audio_{i}.wav'
    with io.open(audio_file, 'rb') as f:
        content = f.read()
        audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=24000,
        language_code='en-US',
        model='video',
        audio_channel_count=1 ,
        enable_word_time_offsets=True
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        l = result.alternatives[0].words
        for j in range(0, len(l), 1):

            start_time = l[j].start_time

            if j < len(l):
                end_time = l[j].end_time
                word = l[j].word

                start_time = title_text_audio.duration + start_time.total_seconds()
                end_time = title_text_audio.duration + end_time.total_seconds()
                text_clip = TextClip(word, fontsize=72, color='black', font='Open-Sans')
                text_clip = text_clip.set_start(start_time).set_end(end_time)
                text_clip = text_clip.set_position(("center", video_with_audio.h * 0.75))
                text_clips.append(text_clip)

                outline_text_clip = TextClip(word, font="Open-Sans", fontsize=74, color="white")
                outline_text_clip = outline_text_clip.set_start(start_time).set_end(end_time)
                outline_text_clip = outline_text_clip.set_position(("center", video_with_audio.h * 0.75))
                outline_text_clips.append(outline_text_clip)

    final_clip = CompositeVideoClip([video_with_audio, screenshot] + outline_text_clips + text_clips)
    final_clip.write_videofile(f"final_video/final_video_{i}.mp4", codec="libx264")



