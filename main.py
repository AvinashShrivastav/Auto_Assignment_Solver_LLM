import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle
import io
import googleapiclient.errors
from googleapiclient.http import MediaIoBaseDownload
from pydantic import BaseModel
from fpdf import FPDF  # Library for PDF creation
from solve_assignment import auto_solve_assignment

# Define the required scopes
SCOPES = [
    "https://www.googleapis.com/auth/classroom.courses",
    "https://www.googleapis.com/auth/classroom.coursework.me",
    "https://www.googleapis.com/auth/classroom.student-submissions.me.readonly",
    "https://www.googleapis.com/auth/classroom.student-submissions.students.readonly",
    "https://www.googleapis.com/auth/classroom.announcements.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]

def solve_assignment(assignment_problem):
    """
    Solve the given assignment problem using an LLM and return the solution as a string.
    """
    # Placeholder for LLM-based solution generation
    solution = auto_solve_assignment(assignment_problem)
    if solution.isSolvable:
        return solution.solution
    else:
        return "There is some issue with the submission"



def create_pdf(content, filename):
    """
    Create a PDF file with the given content and save it as the specified filename.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, content)
    pdf.output(filename)
    print(f"PDF created: {filename}")

def main():
    """Fetch assignments and solve them using LLMs."""
    creds = None

    # Check if token.pickle exists for cached credentials
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    # If no valid credentials, authenticate the user
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0, include_granted_scopes="true")

        # Save credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    # Build the Classroom API service
    classroom_service = build("classroom", "v1", credentials=creds)

    # List courses
    results = classroom_service.courses().list(pageSize=10).execute()
    courses = results.get("courses", [])

    if not courses:
        print("No courses found.")
    else:
        print("Courses:")
        for course in courses:
            print(f"{course['name']} ({course['id']})")
            fetch_assignments_and_solve(classroom_service, course['id'])

def fetch_assignments_and_solve(classroom_service, course_id):
    """Fetch assignments and solve them for a given course."""
    
    # List all assignments (coursework) for the course
    coursework_results = classroom_service.courses().courseWork().list(courseId=course_id).execute()
    coursework = coursework_results.get("courseWork", [])
    if not coursework:
        print(f"No assignments found for course {course_id}.")
    else:
        print(f"Assignments for course {course_id}:")
        for assignment in coursework:
            print(f"  - {assignment['title']}")
            assignment_problem = assignment.get("description", "No description available")
            
            # Solve the assignment using the solve_assignment function
            solution = solve_assignment(assignment_problem)
            
            # Create a PDF for the solved assignment
            pdf_filename = f"solved_assignment_{assignment['id']}.pdf"
            create_pdf(solution, pdf_filename)

if __name__ == "__main__":
    main()
