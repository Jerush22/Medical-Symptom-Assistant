# Medical Symptom Assistant

A web-based medical symptom assistant built using Python, Flask, and a locally running Ollama language model. It collects basic symptom information and provides general health-related information with safety reminders.

## Features

- Collects basic patient information and reported symptoms.
- Considers symptom duration, severity, medical history, medications, and allergies.
- Uses keyword-based checks to flag certain urgent symptoms.
- Uses a local Llama 3.2 model through Ollama to generate general health information.
- Displays the analysis through a web interface.
- Saves generated reports locally.

## Technologies Used

- Python
- Flask
- Ollama
- Llama 3.2 (1B)
- HTML
- CSS

## Project Structure

```text
Medical_Symptom_Assistant/
├── app.py
├── .gitignore
├── README.md
├── static/
│   └── style.css
├── templates/
│   ├── index.html
│   └── result.html
└── reports/
```

## Prerequisites

- Python installed
- Ollama installed and running
- Git (optional, for version control)

## Setup and Run

1. Clone the repository:

   ```bash
   git clone https://github.com/Jerush22/Medical-Symptom-Assistant.git
   ```

2. Open the project folder:

   ```bash
   cd Medical-Symptom-Assistant
   ```

3. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

4. Install the required packages:

   ```bash
   pip install flask ollama
   ```

5. Download the local model if it is not already installed:

   ```bash
   ollama pull llama3.2:1b
   ```

6. Start the Flask application:

   ```bash
   python app.py
   ```

7. Open the application in your browser at:

   `http://127.0.0.1:5000`

Make sure Ollama is running before using the application.

## Medical Safety Disclaimer

This project is intended for educational and informational purposes only. It does not provide a medical diagnosis and is not a substitute for professional medical advice. Keyword-based urgency checks may miss emergencies or flag symptoms incorrectly. For potentially life-threatening symptoms, seek emergency medical care immediately.

## Future Enhancements

- Improve urgent-symptom detection.
- Add stronger privacy and access controls.
- Improve the readability of generated reports.
- Add automated tests and more comprehensive error handling.

## Author

Jerush22
