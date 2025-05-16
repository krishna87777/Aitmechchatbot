# AIT Placement Assistant

## Overview
AIT Placement Assistant is an interactive chatbot web application designed to help Army Institute of Technology students access placement-related information. Built with Streamlit and powered by Mistral AI, the application provides accurate and contextual answers to student queries about campus placements, companies, preparation strategies, and more.


## Features

### 🔐 User Authentication
- **User registration** with username, email, and registration number
- **Year selection** to personalize information
- **Login tracking** to monitor usage statistics

### 💬 AI-Powered Chat Interface
- **Natural language queries** about AIT placements
- **Contextual responses** based on stored placement data
- **Chat history** maintained during the session
- **Quick topics** for one-click queries about common placement questions

### 📊 User Dashboard
- **User statistics** showing total registered users and logins
- **Personalized experience** with username display
- **Easy logout** functionality

### 🎨 Modern UI/UX
- **Dark theme** for reduced eye strain
- **Responsive design** that works on all devices
- **Animated components** for a dynamic user experience

## Technology Stack

- **Frontend**: Streamlit
- **Database**: MongoDB
- **Vector Database**: FAISS for efficient similarity search
- **AI Model**: Mistral-7B-Instruct-v0.3 via Hugging Face
- **Embedding Model**: sentence-transformers/all-MiniLM-L6-v2
- **Framework**: LangChain for RAG (Retrieval Augmented Generation)

## Installation

### Prerequisites
- Python 3.8+
- MongoDB
- Hugging Face API Token

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/krishna87777/Aitmechchatbot
   cd ait-placement-assistant
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with the following variables:
   ```
   MONGODB_URI=your_mongodb_connection_string
   HF_TOKEN=your_huggingface_api_token
   ```

5. Set up your vector database:
   ```bash
   python scripts/create_vectorstore.py
   ```
   Note: This step assumes you have a script to create the vector database from your placement data.

## Usage

1. Start the application:
   ```bash
   streamlit run app.py
   ```

2. Open your browser and navigate to `http://localhost:8501`

3. Register/Login with your details

4. Ask questions about AIT placements!

## Sample Questions

- What companies visited AIT for Mechanical placements?
- What is the average package offered at AIT?
- How should I prepare for core roles?
- Which company offered the highest package last year?
- What skills are required for software roles?

## Data Sources

The placement assistant uses information from:
- Historical placement data from AIT
- Company visit records
- Student placement outcomes
- Industry requirements and trends

## Deployment

The application can be deployed using:

### Streamlit Cloud
1. Push your code to GitHub
2. Connect your GitHub repository to Streamlit Cloud
3. Configure your environment variables
4. Deploy

### Alternative Deployment Options
- Heroku
- AWS Elastic Beanstalk
- Docker container on any cloud provider

## Customization

### Adding New Data
To update the placement information:
1. Prepare your data in the appropriate format
2. Update the vector database using the provided scripts
3. Restart the application to use the new information

### Changing the AI Model
To use a different AI model:
1. Update the `HUGGINGFACE_REPO_ID` variable
2. Ensure the model is compatible with the HuggingFaceEndpoint interface
3. Adjust the parameters as needed for the new model

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Streamlit](https://streamlit.io/) for the web app framework
- [LangChain](https://python.langchain.com/) for the RAG implementation
- [HuggingFace](https://huggingface.co/) for hosting the AI model
- [MongoDB](https://www.mongodb.com/) for database services
- [Mistral AI](https://mistral.ai/) for the language model
