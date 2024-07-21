# Medical Note Redaction Service

![CI/CD Status](https://github.com/medinardaniel/llamafile/actions/workflows/cicd.yml/badge.svg)

## Final Demo Video
[Watch the Final Demo Video](https://your-final-demo-video-link.com)

## Project Purpose
The purpose of the Mediacal Note Redaction Service is to provide a system that redacts PHI (Protected Health Information) from given medical notes. This ensures that sensitive patient information is not exposed when sharing medical documents. The system replaces all PHI information with the word `<REDACTED>`.

## Architecture Diagram
![Architecture Diagram](path/to/architecture-diagram.png)

## Instructions for Setup, Running, and Testing the App

### Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo

2. **Set Up Virtual Environment**
python3 -m venv env
source env/bin/activate

3. **Install Dependencies**
make install

### Running the App

1. **Build Docker Image**
docker build -t llamafile-backend llamafile-backend

2. **Run Docker Container**
docker run -d -p 5000:5000 llamafile-backend

3. **Access the App**
Open your browser and go to http://localhost:5000

### Testing the App

1. **Run Unit Tests**
make test

2. **Example API Call**
curl -X POST http://localhost:5000/redact -H "Content-Type: application/json" -d '{
    "text": "Hi my name is Josephine Smith and I really need my medication shipped to Gotham, NJ 07030. You can also reach me at 123-565-1222 or at jsmith@gmail.com."
}'

**Expected Response**
{
    "redacted_text": "Hi my name is <REDACTED> and I really need my medication shipped to <REDACTED>. You can also reach me at <REDACTED> or at <REDACTED>."
}
