import ollama

# Define Interview Question & User Answer
interview_question = "Describe a time when you handled a difficult situation at work."
user_answer = """
At my previous job, I had a conflict with a colleague over project deadlines.
I communicated openly, listened to their concerns, and proposed a solution that worked for both of us.
Eventually, we met the deadline successfully.
"""

# Create Prompt for LLaMA-2
prompt = f"""
You are an expert interview coach. Your task is to analyze the user's interview answer based on clarity, confidence, structure, and relevance.
Provide constructive feedback and suggest improvements if necessary.

**Interview Question:** {interview_question}

**User's Answer:** {user_answer}

**Evaluation:**
1. Strengths of the response
2. Areas for improvement
3. How well does this answer fit an interview scenario?
4. Suggested improvements to make the answer stronger

**Your feedback:**
"""

# Call Ollama's LLaMA-2 model
response = ollama.chat(model="llama2:7b", messages=[{"role": "user", "content": prompt}])

# Print Response
print(response["message"])
