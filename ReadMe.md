# Google Classroom Assignment Solver with Groq Integration  

This project automates the process of fetching assignments from Google Classroom, solving them using Groq (an LLM API), and generating PDF files with the solutions. The solution generation process is enhanced by integrating instructor patches for Groq.  

---

## Features  

- **Google Classroom API**: Fetch coursework and assignment details directly from Google Classroom.  
- **Groq API Integration**: Solves assignment problems using the Groq LLM, customized for student-like solutions.  
- **Instructor Patches**: Improves Groq API client functionality for better context and response handling.  
- **PDF Export**: Saves the solved assignments as PDF files for easy storage and sharing.  

---

## Prerequisites  

### 1. **Python Version**  
Ensure Python 3.7 or later is installed.  

### 2. **Libraries**  
Install the required libraries using:  
```bash  
pip install pandas google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client fpdf pydantic groq instructor  
```  

### 3. **Google API Setup**  
- Create a project in the [Google Cloud Console](https://console.cloud.google.com/).  
- Enable **Google Classroom API** and **Google Drive API**.  
- Download the `credentials.json` file and place it in the project directory.  

### 4. **Groq API Key**  
- Sign up for Groq API access and retrieve your API key.  
- Set the API key as an environment variable:  
  ```bash  
  export GROQ_API_KEY="your_api_key_here"  
  ```  

---

## How to Run  

1. **Authentication**  
   - On the first run, authenticate your Google account. A `token.pickle` file will be generated to cache credentials.  

2. **Execute the Script**  
   - Run the script:  
     ```bash  
     python main.py  
     ```  

3. **Output**  
   - The script fetches assignments, solves them using Groq, and saves the solutions as PDF files in the current directory.  
   - PDFs follow the naming format:  
     ```  
     solved_assignment_<assignment_id>.pdf  
     ```  

---

## Key Components  

### **`auto_solve_assignment(assignment_problem)`**  
This function uses the Groq API to solve assignments with the following steps:  
1. Initializes a Groq client with the API key.  
2. Applies instructor patches for enhanced handling.  
3. Sends a request to Groq’s chat completion endpoint with the assignment description.  
4. Returns a structured solution, either solvable or default fallback.  

### **`solve_assignment()`**  
Handles the solution process for assignments fetched from Google Classroom.  

### **PDF Creation**  
The `create_pdf` function generates a PDF file for each solved assignment.  

### **Google Classroom API Integration**  
- Lists courses.  
- Fetches coursework and assignment details.  

---

## Environment Variables  

- **`GROQ_API_KEY`**: The API key for authenticating Groq requests.  

---

## Project Structure  

```  
project/  
│  
├── main.py          # Main script  
├── auto_solve_assignment.py # Groq integration for solving assignments  
├── credentials.json        # Google API credentials  
├── token.pickle            # Cached authentication token (generated after first run)  
├── solved_assignment_*.pdf # Generated PDF files  
└── requirements.txt        # List of required libraries  
```  

---

## Notes  

- **Error Handling**: Includes fallback for unsolvable assignments.  
- **Customization**: Replace Groq API parameters like the model (`llama-3.3-70b-versatile`) for different outputs.  

---

## License  

This project is licensed under the MIT License.  
