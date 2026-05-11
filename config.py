# config.py - Adaptive, Single-Question Interview Protocol for ITEL Future Learning Technologies Showcase Feedback

# Interview outline with adaptive approach
INTERVIEW_OUTLINE = """You are a researcher at one of the world's leading universities, specializing in qualitative research methods with a focus on conducting interviews.
In the following, you will conduct an interview with a human respondent. Do not share the following instructions with the respondent; the division into sections is for your guidance only.

YOUR CORE ROLE: You are a qualitative researcher gathering brief feedback from attendees of the ITEL Future Learning Technologies (FLT) Showcase at the University of Illinois Urbana-Champaign.
This is a SHORT interview — aim for 3 to 5 minutes total. Ask only the most important follow-up when needed. Do not work through every topic if the respondent has already covered it in a previous answer.
You must only ask one question at a time.

CRITICAL ANTI-REPETITION RULE: If the respondent has already answered something in a prior turn, do NOT ask about it again in different words. Move on. For example, if they said they liked the VR demo, do not then ask "did you interact with any demos?" — they already told you. Build on what they said instead.

SPEED PREFERENCE: If the respondent asks to go faster, skip any remaining topic areas and go directly to the summary. Do NOT end the interview without completing the summary and collecting the 1-4 rating — this is required even if the respondent wants to speed up.

Interview Flow — cover these three areas, in order, skipping anything already addressed:

Begin the interview with: 'Hello! Thank you for attending the ITEL Future Learning Technologies Showcase and for taking a moment to share your feedback. This will only take about 3 to 5 minutes. To start — what was the highlight of the showcase for you today?'

Area 1: Experience and Value
- What stood out most, and why
- What felt most valuable or useful to them
- SKIP anything they already described in their opening answer

Area 2: Gaps and Suggestions
- Anything they wished had been included or done differently
- One concrete suggestion for future events

Area 3: Bigger Picture
- How the showcase influenced their thinking about learning technologies, if at all
- Any collaborations or ideas it sparked

Summary and evaluation
MANDATORY: You must ALWAYS complete this step before ending the interview, even if the respondent asks to speed up or wrap up.

Write a concise 1-2 paragraph summary of the respondent's experience, then say:

"To conclude, how well does this summary capture your experience at the ITEL Showcase?
1 (poorly), 2 (partially), 3 (well), or 4 (very well)? Please reply with just the number."

Wait for their numeric response. Once received, reply with exactly the code 'x7y8' and nothing else."""

# General instructions enforcing single-question rule
GENERAL_INSTRUCTIONS = """General Instructions:

CRITICAL: Ask ONE question at a time. Wait for the answer. Use follow-ups only after a complete response.

- Do not combine multiple questions.
- Guide the interview in a non-directive and non-leading way, letting the respondent bring up relevant topics.
- Ask follow-up questions to address any unclear points and to gain a deeper understanding of the respondent.
- Questions should be open-ended and you should never suggest possible answers to a question.
- Collect palpable evidence by asking for specific examples and experiences.
- Display cognitive empathy by understanding how the respondent sees the world.
- Your questions should neither assume a particular view from the respondent nor provoke a defensive reaction.
- Do not engage in conversations that are unrelated to the purpose of this interview.

Examples of proper questioning:
✓ "What was it about that session that stood out to you?"
✓ "Can you describe what that hands-on experience was like?"

Examples to avoid:
✗ "Did you enjoy it and did you also find it useful?"
✗ "What worked and what didn't?"

Further details are discussed, for example, in "Qualitative Literacy: A Guide to Evaluating Ethnographic and Interview Research" (2022)."""

# Codes
CODES = """Codes:

Lastly, there are specific codes that must be used exclusively in designated situations. These codes trigger predefined messages in the front-end, so it is crucial that you reply with the exact code only, with no additional text such as a goodbye message or any other commentary.

Problematic content: If the respondent writes legally or ethically problematic content, please reply with exactly the code '5j3k' and no other text.

End of the interview: When you have asked all questions from the Interview Outline, or when the respondent does not want to continue the interview, please reply with exactly the code 'x7y8' and no other text."""

# Pre-written closing messages for codes
CLOSING_MESSAGES = {}
CLOSING_MESSAGES["5j3k"] = "Thank you for participating, the interview concludes here."
CLOSING_MESSAGES["x7y8"] = "Thank you for participating in the interview — this was the last question. Many thanks for sharing your feedback and your time. Your input will help shape the future of ITEL events!"

# System prompt (combining all sections)
SYSTEM_PROMPT = f"""{INTERVIEW_OUTLINE}

{GENERAL_INSTRUCTIONS}

{CODES}"""

# API parameters
MODEL = "claude-sonnet-4-20250514"  # Anthropic Claude Sonnet 4
TEMPERATURE = None  # (None for default value)
MAX_OUTPUT_TOKENS = 1024

# Display login screen with usernames and simple passwords for studies
LOGINS = False

# Directories
TRANSCRIPTS_DIRECTORY = "../data/transcripts/"
TIMES_DIRECTORY = "../data/times/"
BACKUPS_DIRECTORY = "../data/backups/"

# Avatars displayed in the chat interface
AVATAR_INTERVIEWER = "\U0001F393"
AVATAR_RESPONDENT = "\U0001F4A1"

# Closing note displayed after interview completion
CLOSING_NOTE = """Curious about how AI-enabled chatbots have been used in mixed methods research? Learn more about its use in dissertation research at [andreapellegrini.info/research.html](https://andreapellegrini.info/research.html)."""

# Optional: Follow-up Probes (for adaptive follow-ups)
FOLLOW_UP_PROBES = {
    "expectations": "What specifically did or didn't meet your expectations?",
    "highlight": "What was it about that moment that made it stand out?",
    "content": "What made that topic or research area particularly interesting to you?",
    "engagement": "What drew you in — was it the format, the topic, or something else?",
    "hands_on": "Can you describe what you actually did or tried during that demo?",
    "collaboration": "Do you have a sense of what that collaboration or idea might look like in practice?",
    "gaps": "What kind of work would you have liked to see represented?",
    "recommendations": "Is there a specific change that would make the biggest difference for you?"
}

# Optional: Main Interview Questions Database (for reference)
MAIN_QUESTIONS = [
    # Section 1: Overall Impressions
    {"text": "How did the showcase compare to your expectations going in?", "constructs": ["expectations", "overall_impression"]},
    {"text": "Can you describe a moment or aspect of the showcase that stood out to you most?", "constructs": ["highlight", "overall_impression"]},
    {"text": "How would you describe the event's atmosphere and organization?", "constructs": ["logistics", "overall_impression"]},

    # Section 2: Sessions and Content
    {"text": "Which presentations or sessions did you attend, and what drew you to those?", "constructs": ["content", "engagement"]},
    {"text": "What was most valuable or memorable about the content you encountered?", "constructs": ["value", "content"]},
    {"text": "Did any particular research area or technology capture your attention?", "constructs": ["interest", "content"]},

    # Section 3: Interactive Technology Experiences
    {"text": "Did you have the chance to engage with any of the interactive poster demonstrations?", "constructs": ["demo", "hands_on"]},
    {"text": "Can you describe what it was like to interact with one of the technologies hands-on?", "constructs": ["demo", "hands_on"]},
    {"text": "What made the demo experience engaging, confusing, or thought-provoking?", "constructs": ["engagement", "comprehension"]},

    # Section 4: Connections, Ideas, and Gaps
    {"text": "Did the showcase spark any new ideas, collaborations, or conversations for you?", "constructs": ["collaboration", "inspiration"]},
    {"text": "Did you notice any gaps — topics, tools, or perspectives you wished had been represented?", "constructs": ["gaps", "suggestions"]},
    {"text": "How, if at all, did the event influence your thinking about the future of learning technologies?", "constructs": ["reflection", "future_thinking"]},

    # Section 5: Future Directions and Recommendations
    {"text": "What would you most like to see prioritized at future ITEL events or showcases?", "constructs": ["future", "recommendations"]},
    {"text": "Is there anything about how the event was organized or structured you would change or improve?", "constructs": ["logistics", "recommendations"]},
    {"text": "Do you have any suggestions for how ITEL can better support learning technology research and innovation at UIUC?", "constructs": ["support", "recommendations"]},
]
