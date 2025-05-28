from tkinter import Tk, Label, Entry, Button, Text, Scrollbar, messagebox, Frame, ttk
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
from youtube_transcript_api import YouTubeTranscriptApi
import threading

# Define the model and tokenizer
model_name = "sshleifer/distilbart-cnn-12-6"
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)


# Function to handle video summarization
def summarize_video():
    loading_label.config(text="LOADING SUMMARY....", font=("Arial", 14, "italic"), fg="#27ae60")  # Green
    root.update_idletasks()

    video_url = entry_video_url.get()

    try:
        video_id = video_url.split("=")[1]
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        if not transcript:
            messagebox.showinfo("Error", "Subtitles are disabled for this video or no transcript available.")
            loading_label.config(text="Failed to load transcript.", font=("Arial", 14, "italic"), fg="#e74c3c")  # Red
            return

        # Original Transcript
        original_transcript_text.config(state="normal")
        original_transcript_text.delete(1.0, "end")
        original_transcript_text.insert("end", "ORIGINAL TRANSCRIPT :\n\n")

        for entry in transcript:
            original_transcript_text.insert("end", entry['text'] + "\n")

            # Update the number of sentences and words in the transcript
            num_sentences_transcript = len(transcript)
            num_words_transcript = sum(len(entry['text'].split()) for entry in transcript)

            label_transcript_info.config(
                text=f"Sentences in Transcript : {num_sentences_transcript}\nWords in Transcript : {num_words_transcript}",
                font=("Arial", 14), fg="#27ae60")  # Green
            root.update_idletasks()

        original_transcript_text.config(state="disabled")

        result = " ".join(entry['text'] for entry in transcript)

        summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

        num_iters = int(len(result) / 1000)
        summarized_text = []

        for i in range(0, num_iters + 1):
            start = i * 1000
            out = summarizer(result[start: start + 1000])
            out = out[0]['summary_text']
            summarized_text.append(out)

            # Update progress bar value
            progress_value = (i / num_iters) * 100
            progress_bar["value"] = progress_value
            root.update_idletasks()

        # Number of Sentences and Words in Summary
        num_sentences_summary = sum(text.count('.') for text in summarized_text)
        num_words_summary = sum(len(text.split()) for text in summarized_text)

        label_summary_length.config(
            text=f"Sentences in Summary : {num_sentences_summary}\nWords in Summary : {num_words_summary}",
            font=("Arial", 14), fg="#27ae60")  # Green

        summary_text.delete(1.0, "end")
        summary_text.insert("end", "\n\n".join(summarized_text))
        summary_text.config(font=("Arial", 12, "italic"), fg="#333")

    except Exception as e:
        messagebox.showinfo("Error", f"An error occurred: {str(e)}")
        label_transcript_info.config(text="Sentences in Transcript : \nWords in Transcript : ", font=("Roboto", 12),
                                     fg="#333")
        label_summary_length.config(text="Sentences in Summary : \nWords in Summary : ", font=("Roboto", 12), fg="#333")
        summary_text.delete(1.0, "end")

    loading_label.config(text="")  # Hide the loading label
    progress_bar.grid_remove()  # Remove the progress bar from the layout


# Set up Tkinter UI
root = Tk()
root.title("YouTube Video Summarizer")
root.geometry("900x750")
root.configure(bg="#f0f0f0")

main_frame = Frame(root, bg="#f0f0f0")
main_frame.pack()

header_label = Label(main_frame, text=" YouTube Video Summarizer ", font=("YouTube Sans", 20, "bold"), bg="#c0392b",
                     fg="white")
header_label.grid(row=0, column=0, pady=(20, 10))

label_video_url = Label(main_frame, text="Enter YouTube Video URL : ", font=("Roboto", 14), bg="#f0f0f0", fg="#333")
label_video_url.grid(row=1, column=0, pady=(0, 10))

entry_video_url = Entry(main_frame, width=70, font=("Roboto", 10))
entry_video_url.grid(row=2, column=0, padx=10, pady=(0, 20))

button_summarize = Button(main_frame, text="Summarize Video",
                          command=lambda: threading.Thread(target=summarize_video).start(),
                          font=("Arial", 13), bg="#2980b9", fg="white", padx=8, pady=4)
button_summarize.grid(row=3, column=0)

progress_bar = ttk.Progressbar(main_frame, mode="determinate", length=200)
progress_bar.grid(row=4, column=0, pady=(10, 20))

loading_label = Label(main_frame, text="", font=("Arial", 14, "italic"), bg="#f0f0f0", fg="#333")
loading_label.grid(row=5, column=0, pady=(10, 20))

label_transcript_info = Label(main_frame, text="",
                              font=("Roboto", 12), bg="#f0f0f0", fg="#333")
label_transcript_info.grid(row=6, column=0, pady=(0, 10))

original_transcript_text = Text(main_frame, height=8, width=80, wrap="word", font=("Arial", 12), bg="white", fg="#333")
original_transcript_text.grid(row=7, column=0, pady=(0, 10), padx=10)

scrollbar_original = Scrollbar(main_frame)
scrollbar_original.grid(row=7, column=1, sticky="ns", pady=(0, 10))
original_transcript_text.config(yscrollcommand=scrollbar_original.set)
scrollbar_original.config(command=original_transcript_text.yview)
original_transcript_text.config(state="disabled")

label_summary_length = Label(main_frame, text="",
                             font=("Roboto", 12), bg="#f0f0f0", fg="#333")
label_summary_length.grid(row=8, column=0, pady=(0, 10))

summary_text = Text(main_frame, height=10, width=80, wrap="word", font=("Arial", 12, "italic"), bg="white", fg="#333")
summary_text.grid(row=9, column=0, pady=(0, 20), padx=10)

scrollbar_summary = Scrollbar(main_frame)
scrollbar_summary.grid(row=9, column=1, sticky="ns", pady=(0, 20))
summary_text.config(yscrollcommand=scrollbar_summary.set)
scrollbar_summary.config(command=summary_text.yview)

root.mainloop()