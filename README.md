YouTube Video Summarizer

	A Python-based web application that fetches the transcript of a YouTube video and generates a summarized version using a state-of-the-art NLP model.
	Built with Flask, HuggingFace Transformers, and YouTube Transcript API.
 Features
- 🎯 Enter any YouTube video URL and get a summarized version of its transcript.
- 📜 View original transcript and detailed summary statistics (word/sentence counts).
- 📝 Copy the summary to clipboard.
- ⚙️ Control the summary length dynamically (shorter or longer).
- 📈 Animated progress bar during processing.

Tech Stack
 
Flask - Backend web framework              
HuggingFace Transformers - Text summarization pipeline (`distilbart-cnn-12-6`) 
YouTube Transcript API - Fetches video transcript        
Bootstrap 4 - Responsive frontend styling        
 jQuery - AJAX calls and DOM manipulation    

Prerequisites
Ensure Python 3.8+ is installed on your system.
install dependencies:
pip install flask transformers youtube-transcript-api
Running the App
1.	Clone this repository:
2.	Run the Flask app:
python app.py
3.	Open your browser and visit:

Limitations
	Summarization quality depends on the video’s transcript availability.
	Long videos may need chunked summarization due to token limits.
	No support for videos without subtitles or auto-generated transcript access blocked.
![image](https://github.com/user-attachments/assets/b11f1062-6d2d-4053-b0c4-e081ed4e91d3)
![image](https://github.com/user-attachments/assets/906b0e2d-8469-43c3-9fe7-52754f67fc9f)
![image](https://github.com/user-attachments/assets/86de6129-a1ad-422f-910c-228053f3188f)





