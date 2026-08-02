# KTU AI Study Assistant

**Name:** EB Fathima Suhana
**MUID:** fathimasuhana@mulearn

🌐 **Deployment Link:** [streamlit link](https://eujvqzvgdl29r9at8uuz3c.streamlit.app/~/+/#ktu-ai-study-assistant)

## Project Overview

This was for Assignment 10 of Epochs '26 - building something with a free LLM that actually solves a real problem. I went with an **AI Study Assistant** since I'm literally a CS student under the KTU scheme and this is something I'd actually use myself while studying, not just a random demo idea.

It's a Streamlit app with 3 modes:
1. **Concept Explainer** - paste in any topic you're stuck on and get it explained at whatever level you pick (beginner / student who knows basics / exam-focused).
2. **Notes Summarizer** - paste in messy lecture notes and get a clean bullet-point summary + a key terms list.
3. **Quiz Generator** - give it a topic and it generates self-test questions (MCQ or short answer) so you can quiz yourself before exams.

## Chosen Use Case

Went with the **AI Study Assistant** idea from the suggestions list, since exam prep / understanding topics quickly is something every student (including me) actually needs, so it felt like the most useful pick rather than building something I'd never actually open again after submitting.

## AI Platform / Model Used

Used the **Groq API** (free tier) with the `llama-3.3-70b-versatile` model. Picked Groq over Gemini/HuggingFace mainly because:
- Signup is quick and the free tier is genuinely generous (no credit card needed).
- Responses come back really fast (Groq is known for its fast inference), which matters for something like a study tool where you don't want to sit and wait.
- The Python SDK is basically identical to OpenAI's, so its simple to work with.

## Key Observations

- Having a mode-specific system prompt vs a single generic prompt made a big difference in output quality - when I first tested with one generic "You are a helpful assistant" prompt, the outputs were way less structured and sometimes ignored the format I wanted.
- The "explain it like I'm..." difficulty slider actually changes the depth of explanation noticeably, which was cool to see working properly.
- Groq's responses came back fast enough that the app doesn't feel laggy even though its calling an external API every time.
- Tested with a few topics from TOC and DS and the response is pretty fast.
- The responses are optimised based on the mode we choose - beginner to exam-oriented only.


## Challenges Faced

- Needed to handle the case where no API key is set yet, so the app doesn't just crash - added a check that shows a friendly warning message instead of throwing an error if someone opens the app without adding a key first.
- Had to be careful not to hardcode the API key anywhere in the code (that's a big no-no for a public repo) - used `st.secrets` for deployment and a sidebar password-type input for local testing instead, with the actual secrets file gitignored.
- Balancing prompt length/detail vs keeping responses fast and focused - had to explicitly tell the model to keep things concise in a couple of the prompts since it was giving overly long responses at first.

## Future Improvements

- Add chat memory so you can ask follow-up questions instead of every question being totally independent.
- Let users upload a PDF of their notes/textbook directly instead of copy-pasting text.
- Add a "difficulty score" or track which quiz questions the user got wrong to focus revision on weak areas.
- Tie it into my [KTU Study Planner](#) project so topics marked "not yet revised" there could be quizzed automatically here.
- Add support for switching between different free LLM providers (like Gemini) as a fallback if Groq's free tier limit gets hit.
