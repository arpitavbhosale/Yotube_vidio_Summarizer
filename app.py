from youtube_transcript_api import YouTubeTranscriptApi as yta

link = "https://youtu.be/NiKtZgImdlY?si=SsVwrV9TkjcaDHGT"
id = link.split('/')
vid_id = id[-1]

data = yta.get_transcript(vid_id)
# print(data)
final_data = ''
for val in data:
    for key, value in val.items():
        if key == 'text':
            final_data += value
process_data = final_data.splitlines()
clean_data = ''.join(process_data)
print(clean_data)

i = 1
try:
    i.append(2)
except AttributeError:
   print('Thank You!!!')
