import os
from groq import Groq
import instructor
from pydantic import BaseModel

class solution(BaseModel):
    isSolvable: bool
    solution: str

default_solution = solution(isSolvable=False, solution="There is some issue with the submission")



def auto_solve_assignment(assignment_problem):
    """
    Solve the given assignment problem using an LLM and return the solution as a string.
    """
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )
    # Enable instructor patches for Groq client
    client = instructor.from_groq(client)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Please Solve the assignment as Student point of view.The problem is:{assignment_problem}",
            }
        ],
        model="llama-3.3-70b-versatile",
        response_model=solution
    )

    print(chat_completion)
    return chat_completion