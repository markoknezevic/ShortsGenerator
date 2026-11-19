# Shorts Generator

**AI-powered YouTube Shorts creation using Google Cloud speech models and YouTube API integration.**

## Example

Imagine turning a short story into a narrated YouTube Short using a title, story text, an introductory image, and background footage.

Google Cloud's AI speech services turn the title and story into narration and recognize the spoken words to generate subtitle timings. The generator integrates that narration into background footage, displays the introductory image, and overlays word-by-word subtitles. The result is saved to `YT Script/final_video/final_video_1.mp4` and can then be uploaded through the YouTube integration.

## What this project does

Shorts Generator connects Google's AI speech models with video production and YouTube uploading. Its core workflow integrates three Google services:

- **Google Cloud Text-to-Speech:** uses speech synthesis models to generate English narration from the supplied title and story text.
- **Google Cloud Speech-to-Text:** uses speech recognition to transcribe the narration and return word timings for synchronized subtitles.
- **YouTube Data API:** uploads the finished video as private through a separate script authenticated with Google OAuth.

MoviePy combines the AI-generated narration, timed subtitles, introductory image, and existing background footage into an MP4 video. The story text, images, and background footage are supplied as inputs; AI handles speech synthesis and recognition.

The main script currently processes five sets of numbered inputs (`1` through `5`) in one run. Each output contains:

- A narrated title followed by the main text, using separate English voices.
- A random background clip trimmed to the combined narration length.
- An introductory image overlay.
- Word-by-word captions for the main narration.
- An MP4 video encoded with H.264.

## Scripts and requirements

- `YT Script/main.py` generates the videos. Run it from the `YT Script` directory because its file paths are relative to that directory.
- `YT Script/upload.py` separately uploads a generated video to YouTube as private. It currently selects video `4`; change its `i` variable to choose another video. It does not schedule publication.
- `YT Script/text_to_speach.py` is a standalone Google Cloud text-to-speech example.

Generation requires the numbered text and image inputs, background footage, the `audio_files` and `final_video` output directories, and Google Cloud credentials at `YT Script/auth/sa.json` with access to Text-to-Speech and Speech-to-Text. The Python imports also require MoviePy, gTTS, Mutagen, and the Google Cloud client libraries, plus the video and text-rendering tools used by MoviePy and the Open Sans font.

YouTube uploading uses a separate OAuth configuration at `YT Script/auth/yu.json` and reads the video description from `YT Script/general_description.txt`.

The current implementation uses hard-coded paths, voices, batch size, and a background selection limit of 433 seconds. It preserves the background video's dimensions, so use appropriately sized footage for vertical Shorts.
