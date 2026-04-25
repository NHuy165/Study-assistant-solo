mcq_schema = """
{
    "name": "string (A concise name of this multiple choice exercise)",
    "description": "string (A description of the contents of this exercise and what knowledge its questions cover)",
    "activity_items": [
        {
            "question": "string (The content of the question)",
            "answers": ["string", "string", "string", "string"],
            "correct": "integer (The index of the correct answer, 0-indexed. There can only be 1 correct answer.)"
        }
    ]
}

Additional information:
- The "activity_items" key is a JSON array containing the main questions of the multiple choice exercise.
- "answers": Do not include letter prefixes (like 'A', 'B', 'C'...). Just the answer text.
- The default number of activity_items is 10, the default number of answers for each question (activity item) is 4. This can be changed according to the user's explicit request.
"""

flashcard_schema = """
{
    "name": "string (A concise name of this set of flashcards)",
    "description": "string (A description of the contents of the flashcards and what knowledge they cover)",
    "activity_items": [
        {
            "front": "string (The front information, usually a term, a question or a hint)"
            "back": "string (Usually a definition, an answer or an explanation)"
        }
    ]
}
Additional information:
- The "activity_items" key is a JSON array containing the contents of the flashcards. Each flashcard is described by a dictionary containing "front" and "back" information.
- The default number of flashcards is 10. This can be changed according to the user's explicit request.
"""
