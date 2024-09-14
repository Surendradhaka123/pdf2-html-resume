# PDF to HTML Resume Generator

## Overview

The **PDF to HTML Resume Generator** allows users to upload their LinkedIn PDF resume and convert it into an HTML format using the OpenAI API for extracting and generating the required content. This app is built using a combination of JavaScript, Python, and HTML, and is deployed on **Vercel**. The primary objective is to enable users to generate an HTML resume that is both interactive and easy to update.

## Features

- Upload LinkedIn PDF resumes.
- Extracts relevant data from the PDF using the OpenAI API.
- Converts the extracted data into an HTML resume format.
- Provides links to view and download the HTML resume.
- Real-time feedback with a spinner to indicate progress.
  
## Tech Stack

- **Frontend**: HTML, JavaScript
- **Backend**: FastAPI (for PDF parsing and interaction with OpenAI API)
- **Deployment**: Vercel (for serverless hosting)

## Problem

The problem was to create an application that could extract relevant information from a PDF resume and convert it into an HTML file that could be viewed and downloaded. We also needed to handle user interactions efficiently, providing feedback while the processing was taking place and ensuring that the deployed app on Vercel operated within the service’s limitations, such as timeout constraints.

## Approach & Solution

### Step 1: Frontend (HTML + JavaScript)

1. **Form Handling**: The app presents a form where users can upload their PDF file and input their OpenAI API key. Upon form submission, a `FormData` object is created, which contains the PDF file and API key.
2. **User Feedback**: A spinner was added to indicate that the backend is processing the request, preventing multiple submissions by disabling the form until processing is complete.
3. **Handling API Responses**: On receiving a successful response from the backend, two buttons are shown to view and download the generated HTML resume. If there's an error, a clear error message is shown to the user.

### Step 2: Backend (FastAPI + OpenAI)

1. **File Upload and API Integration**: The uploaded PDF is sent to the backend, where FastAPI handles file uploads and processes the form data.
2. **OpenAI API Usage**: The backend communicates with the OpenAI API using the provided API key to generate the resume from the extracted data.
3. **Error Handling**: Proper error handling was implemented to manage scenarios like invalid API keys, malformed PDFs, or timeouts.

### Step 3: Deployment & Vercel Configuration

1. **Vercel Serverless Limitations**: During deployment, the primary issue faced was the `FUNCTION_INVOCATION_TIMEOUT`, which indicates that the serverless function on Vercel was exceeding the time limit allowed by the platform.
   
2. **Optimizing the Backend**:
   - I reviewed the backend code to ensure efficient data extraction and interaction with the OpenAI API.
   - Adjusted the backend to immediately respond to the client once the request was accepted, and only proceed with more complex processing tasks after that.

3. **Future Improvements**:
   - For long-running tasks like PDF processing, a queue system (e.g., AWS SQS or Celery) could be used to handle tasks asynchronously.
   - Use of a persistent backend service if timeout issues continue to persist with serverless architecture.

### Step 4: Testing

- The app was tested locally and then deployed to Vercel.
- Various error scenarios such as incorrect API keys, file format issues, and network failures were handled and tested.

### Step 5: Addressing Common Errors

1. **504 Gateway Timeout (FUNCTION_INVOCATION_TIMEOUT)**:
   - We ran into timeouts due to Vercel’s serverless function execution time limit. To address this, we minimized heavy processing tasks and considered moving these to an asynchronous task queue or a persistent backend for long-running tasks.

2. **JSON Parsing Error**:
   - A minor issue related to parsing JSON responses was encountered, which was resolved by ensuring all server responses are formatted properly.

## How to Run Locally

### Prerequisites

- Python 3.x
- FastAPI

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/Surendradhaka123/pdf2-html-resume.git
   cd pdf-to-html-resume
   ```

2. Install the necessary dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the FastAPI server:

   ```bash
   python run main.py
   ```

4. Open the app in your browser:

   Navigate to `http://127.0.0.1:8080` to interact with the form.


## Future Improvements

- **Task Queue for Long-Running Jobs**: Implement asynchronous processing using task queues to handle long-running PDF processing jobs.
- **Rich Resume Customization**: Add more customization options to the generated HTML resume such as themes, colors, and layouts.
- **Better Error Feedback**: Provide more detailed error feedback to the user, including specific error messages when API limits are exceeded or when network issues occur.
