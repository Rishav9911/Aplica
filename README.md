# Aplica+

**AI-Driven Job Application Assistant**

Aplica+ is a cutting-edge job application assistant designed to automate and optimize the job search process using advanced AI technologies. Built with Python, Flask, Streamlit, MongoDB, Ollama, Hugging Face Transformers, and a Chrome Extension, Aplica+ streamlines job matching, outreach, and interview preparation.

## Features

- **Smart Job Matching:**  
  Utilizes Retrieval-Augmented Generation (RAG) pipelines to intelligently match users with relevant job postings.

- **Automated Outreach:**  
  Integrates with the Gmail API to automate job applications and outreach, reducing manual effort.

- **Chrome Extension (Powered by LLaMA-7b):**  
  Automatically completes job application forms and generates tailored cover letters, handling over 30 applications per week and cutting manual work by at least 50%.

- **Interview Preparation Tool:**  
  Employs Whisper and LLaMA models to transcribe audio interview responses and deliver instant, AI-based feedback.

## Technologies Used

- **Python**
- **Flask**
- **Streamlit**
- **MongoDB**
- **Ollama**
- **Hugging Face Transformers**
- **Whisper**
- **LLaMA-7b**
- **Chrome Extension**
- **Gmail API**

## Getting Started

### Prerequisites

- Python 3.8+
- MongoDB
- Node.js (for Chrome Extension development)
- Ollama and Hugging Face models

### Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Rishav9911/Aplica.git
   cd Aplica
   ```

2. **Install Python Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up MongoDB:**
   - Ensure MongoDB is running locally or update connection details in your environment.

4. **Configure Environment Variables:**
   - Set up API keys for Gmail, Hugging Face, Ollama, etc. in a `.env` file.

5. **Run the Backend:**
   ```bash
   flask run
   ```

6. **Launch the Streamlit App:**
   ```bash
   streamlit run app.py
   ```

7. **Install Chrome Extension:**
   - Follow instructions in the `chrome-extension/` directory.

## Usage

- Access the Streamlit dashboard to start matching jobs and preparing for interviews.
- Use the Chrome extension to automate job applications and generate personalized cover letters directly in your browser.
- Review AI-driven feedback on your interview responses for continuous improvement.

## Contributors
- Rishav Sachdeva
- Hansawani Saini
- Sushweta Bhattacharya

## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements or new features.

## Contact

For questions or support, please contact [Rishav9911](https://github.com/Rishav9911).

---
*Architected in March 2025*
