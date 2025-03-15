# YOUTUBE VIDEO SUMMARIZER
Fed up with watching a long video only to realize its waste of time... 😢, now those days are gone 🤩. Get a quick summary of any video* and decide whether to watch or not. Let me introduce the youtube video summarizer which takes a youtube video and gives you the summary, insights and guess what, it provides the summary and thoughts from top comments as well 🤜🤛. And.. it just takes a few clicks and seconds. Here is what it does in detail:
- Takes a youtube URL and gets the transcript if available, otherwise, no summary from transcript is given but the comments is part is still present (if comments itself are present 😜).
- Analyzes the text, understands it and creates a comprehensive and detailed summary.
- Give a brief summary and divides the entire transcript in to meaningful sections and explain them.
- At the end, it provides, key insights and mentions some quotations used in the video.
- It takes top `100` comments, anazlyses and says what most people are saying, lists any insightful/thoughtful comments

`*` -> Currently supported languages: Telugu, Hindi and English
## How to setup
- Create a python virtual environment and install the following pip modules:
```bash
pip install requests youtube-transcript-api google-generativeai
```
- Save the code in `summarizer_with_transcript.py` in a python file.
- You need to save the following environment variables in a `.env` file.
```env
YOUTUBE_API_KEY=<your youtube api key>
GEMINI_API_KEY=<your gemini api key>
```
- Get the `YOUTUBE_API_KEY` from [here](https://console.cloud.google.com/apis/credentials) after creating a new project and enabling `YouTube Data API v3`.
- Get the `GEMINI_API_KEY` from [here](https://aistudio.google.com/apikey).

And... you are good to go
### Enjoy your time by choosing what you want to do with that time ✌️✌️