multiple_choice_questions_schema = """
{
    "name": "string (A concise name of this multiple choice exercise)",
    "description": "string (A description of the contents of this exercise and what knowledge its questions cover)",
    "activity_items": [
        {
            "question": "string",
            "answers": ["string", "string", "string", "string"],
            "correct": "integer"
        }
    ]
}

Additional information:
- Description: Multiple choice questions, each question has 4 answers and only 1 answer is correct
- The "activity_items" key is a JSON array containing the main questions of the multiple choice exercise.
- "question": Contains the question itself.
- "answers": Do not include letter prefixes (like 'A', 'B', 'C'...). Just the answer text.
- "correct": Contains the index of the correct answer, 0-indexed.
- The default number of activity_items is 10. This can be changed according to the user's explicit request.
"""

flashcards_schema = """
{
    "name": "string (A concise name of this set of flashcards)",
    "description": "string (A description of the contents of the flashcards and what knowledge they cover)",
    "activity_items": [
        {
            "front": "string"
            "back": "string"
        }
    ]
}
Additional information:
- Description: Study flashcards, the front contains the information the user can instantly see and the back contains information the user has to interact to be able to see.
- The "activity_items" key is a JSON array containing the contents of the flashcards. Each flashcard is described using a dictionary containing "front" and "back" information.
- "front": The front information, usually a term, a question or a hint.
- "back": Usually a definition, an answer or an explanation.
- The default number of flashcards is 10. This can be changed according to the user's explicit request.
"""

tap_to_review_schema = """
{
    "name": "string (A concise name of this set of clozes)",
    "description": "string (A description of the contents of the clozes and what knowledge they cover)",
    "activity_items": [
        {
            "text": "string"
            "gaps": ["string1", "string2", ...]
        }
    ]
}

Additional information:
- Description: A cloze deletion problem where the user has to click the censored words to reveal them. Each paragraph may contain information about a specific study problem. Keep in mind that this is not a PROBLEM, but a review material.
- The "activity_items" key is a JSON array containing the paragraphs of information. Each paragraph is described using a paragraph with missing words and the missing words themselves in correct order.
- "text": The paragraph of information, usually about a method to a problem, a definition, facts about a specific concept, anything that the user should remember. Each censored word is marked by the string $!GAP!$
- "gaps": The censored word that will be revealed when the user clicks it. The array has to contain the words in the correct order based on the paragraph in "text". The censored words should be important concepts, points of information that are essential to the overall information being displayed in "text", basically something that the user has to engrave in memories. The number of gaps HAS TO MATCH the number of $!GAP!$ in the paragraph.
- The default number of paragraphs is 10. This can be changed according to the user's explicit request.
"""
