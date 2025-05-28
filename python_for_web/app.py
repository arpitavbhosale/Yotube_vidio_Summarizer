from flask import Flask, render_template, request, jsonify
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

# Define the model and tokenizer for summarization
model_name = "sshleifer/distilbart-cnn-12-6"
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize_video', methods=['POST'])
def summarize_video():
    video_url = request.form['video_url']
    length_factor = float(request.form.get('length_factor', 1.0))  # Default to 1.0 if not provided

    try:
        video_id = video_url.split("=")[1]
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        if not transcript:
            return jsonify({'error': 'Subtitles are disabled for this video or no transcript available.'}), 400

        result = " ".join(entry['text'] for entry in transcript)

        summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

        # Adjust the summary length based on the length factor
        num_iters = int(len(result) / (1000 * length_factor))
        summarized_text = []

        for i in range(0, num_iters + 1):
            start = int(i * (1000 * length_factor))  # Convert to integer
            out = summarizer(result[start: start + int(1000 * length_factor)])  # Convert to integer
            out = out[0]['summary_text']
            summarized_text.append(out)

        num_sentences_summary = sum(text.count('.') for text in summarized_text)
        num_words_summary = sum(len(text.split()) for text in summarized_text)

        # Calculate number of sentences and words in the transcript
        num_sentences_transcript = len(transcript)
        num_words_transcript = sum(len(entry['text'].split()) for entry in transcript)

        return jsonify({
            'transcript': transcript,
            'summary': summarized_text,
            'num_sentences_summary': num_sentences_summary,
            'num_words_summary': num_words_summary,
            'num_sentences_transcript': num_sentences_transcript,
            'num_words_transcript': num_words_transcript
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
