MCQ_format_prompt = """
{
    "name": "string",
    "description": "string",
    "activity_items": [
        {
            "question": "string",
            "answers": ["string", "string", "string", "string"],
            "correct": "integer"
        }
    ]
}

Additional information:
+ Material breakdown: Multiple choice questions, each question has 4 answers and only 1 answer is correct
+ The "activity_items" key is a JSON array containing the main questions of the multiple choice exercise.
+ "question": Contains the question itself.
+ "answers": Do not include letter prefixes (like 'A', 'B', 'C', 'D'). Just the answer text.
+ "correct": Contains the index of the correct answer, 0-indexed (possible values: 0, 1, 2, 3).
+ The default number of activity_items is 10. This can be changed according to the user's explicit request.
"""

flashcards_format_prompt = """
{
    "name": "string",
    "description": "string",
    "activity_items": [
        {
            "front": "string"
            "back": "string"
        }
    ]
}
Additional information:
+ Material breakdown: Study flashcards, the front contains the information the user can instantly see and the back contains information the user has to interact to be able to see.
+ The "activity_items" key is a JSON array containing the contents of the flashcards. Each flashcard is described using a dictionary containing "front" and "back" information.
+ "front": The front information, usually a term, a question or a hint.
+ "back": Usually a definition, an answer or an explanation.
+ The default number of flashcards is 10. This can be changed according to the user's explicit request.
"""

open_ended_format_prompt = """
{
    "name": "string",
    "description": "string",
    "activity_items": [
        {
            "question": "string"
            "correct": "string"
        }
    ]
}

Additional information:
+ Material breakdown: A simple set of open-ended (also known as essay) questions that have definitive answers. The user is graded not only on the answers they provide but also how they describe their thought process.
+ The "activity_items" key is a JSON array containing the open-ended questions.
+ "question": The contents of each question.
+ "correct": The comprehensive model answer of the question, covering all the main points and criteria the user will have to fulfill in order to get full marks. This field will be used when grading the user's answers.
+ The default number of questions is 10. This can be changed according to the user's explicit request.
"""
