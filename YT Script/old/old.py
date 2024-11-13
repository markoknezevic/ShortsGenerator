#Finding content timestamps
# audio_file_path = "output.mp3"
# text_file_path = "main_text_1.txt"

# task = Task('task_language=eng|os_task_file_format=json|is_text_type=plain|os_task_adjust_boundary_nonspeech_min=0.200|os_task_adjust_boundary_nonspeech_string="min"')

# task.audio_file_path_absolute = audio_file_path
# task.text_file_path_absolute = text_file_path

# task.sync_map_file_path_absolute = "sync_map.json"
# ExecuteTask(task).execute()
# task.output_sync_map_file()

# text_clips = []
#Add content to clip
# with open('sync_map.json', 'r') as file:
#     data = json.load(file)
#     fragments = data['fragments']

#     for element in fragments:
#         content = element['lines'][0]
#         start_time = element['begin']
#         end_time = element['end']
#         text_clip = TextClip(content, fontsize=50, color='white', font='Amiri-Bold')
#         text_clip = text_clip.set_start(start_time).set_end(end_time)
#         # text_clip = text_clip.crossfadein(1).crossfadeout(1)
#         text_clip = text_clip.set_position(("center", "center"))
#         text_clips.append(text_clip)



# //////////


# with open('google_sync_map.json', 'r') as file:
#     data = json.load(file)
#     fragments = data['results'][0]['alternatives'][0]['words']

#     for i in range(0, len(fragments), 2):
#         content = fragments[i]['word']
#         if (i+1) < len(fragments):
#             content = content +" "+fragments[i+1]['word']
#             end_time = fragments[i+1]['endTime'][:-1]
#         else:
#             end_time = fragments[i]['endTime'][:-1]

#         start_time = fragments[i]['startTime'][:-1]


#         text_clip = TextClip(content, fontsize=50, color='white', font='Amiri-Bold')
#         text_clip = text_clip.set_start(start_time).set_end(end_time)
#         # text_clip = text_clip.crossfadein(1).crossfadeout(1)
#         text_clip = text_clip.set_position(("center", "center"))
#         text_clips.append(text_clip)

# final_clip = CompositeVideoClip([video_with_audio] + text_clips)
# # Composite the content onto the video
# final_clip.write_videofile("output_video.mp4", codec="libx264")










