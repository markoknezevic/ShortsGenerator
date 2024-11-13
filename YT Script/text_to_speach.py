from google.cloud import texttospeech

# Set up the client with your credentials
client_file = 'auth/sa.json'
client = texttospeech.TextToSpeechClient.from_service_account_file(client_file)

# Define the text to synthesize
synthesis_input = texttospeech.SynthesisInput(text="Hello, how are you today?")

# Select the voice and language options
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US",  # Language and locale
    ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL  # Voice gender
)

# Select the audio file format
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3  # Options: MP3, LINEAR16, etc.
)

# Make the request to the API
response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

# Save the audio response to a file
with open("output_audio.wav", "wb") as out:
    out.write(response.audio_content)
    print("Audio content written to file output_audio.mp3")
