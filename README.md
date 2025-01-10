# DriveX-Assignment
This document outlines the steps required to deploy the DriveX web application (frontend and backend) on a hosting service. Follow these steps carefully to ensure a successful deployment.

 1. Prerequisites
  Before you start, ensure you have:
	•	A GitHub repository for your project (frontend and backend in the same repo).
	•	Accounts on Render (for backend hosting) and Vercel (for frontend hosting).
	•	Installed Git, Node.js, and Python on your local machine.

 2. Set Up Your Repository
	1.	Create a GitHub repository and clone it locally:
        git clone https://github.com/<your-username>/<repository-name>.git
        cd <repository-name>
 	2.	Add all your project files to the repository:
      git add .
      git commit -m "Initial commit"
      git push -u origin main

 3. Backend Deployment on Render
  	1.	Log in to your Render account.
  	2.	Click New + and select Web Service.
  	3.	Connect your GitHub repository to Render.
  	4.	In the service settings:
  	•	Build Command:
      pip install -r requirements.txt
    •	Start Command:
      uvicorn main:app --host=0.0.0.0 --port=8000
   	5.	Set up environment variables (if required, e.g., for API keys or database credentials).
	  6.	Deploy the backend. Render will provide a URL like https://your-backend-service.onrender.com.

 4. Frontend Deployment on Vercel
	1.	Log in to your Vercel account.
	2.	Click New Project and import your GitHub repository.
	3.	Configure the settings:
	•	Root Directory: Select the frontend folder.
	•	Build Command:
    npm run build
  •	Output Directory:
    frontend/build
 	4.	Add environment variables for the backend URL:
	•	Key: REACT_APP_BACKEND_URL
	•	Value: URL of your Render backend service (e.g., https://your-backend-service.onrender.com).
	5.	Deploy the frontend. Vercel will provide a URL like https://your-frontend-project.vercel.app.

5. Verify Deployment
	1.	Open the Vercel URL in your browser.
	2.	Test the functionality:
	•	Upload a file.
	•	Ask a question.
	3.	Check that the frontend communicates with the backend hosted on Render.

6. Troubleshooting
	•	CORS Issues:
Ensure you have added the correct CORS settings in your backend:
    from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
