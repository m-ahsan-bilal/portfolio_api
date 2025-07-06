from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Portfolio Contact API", version="1.0.0")

# Add CORS middleware to allow requests from your Flutter web app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your specific domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for contact form data validation
class ContactForm(BaseModel):
    email: EmailStr
    topic: str
    message: str

# Store contact submissions (in a real app, you'd use a database)
contact_submissions = []

@app.get("/")
def read_root():
    return {"message": "Portfolio Contact API is running!", "status": "active"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/contact", response_model=dict)
async def submit_contact_form(contact: ContactForm):
    """
    Submit a contact form with email, topic, and message
    """
    try:
        # Log the contact submission
        logger.info(f"New contact form submission from: {contact.email}")
        logger.info(f"Topic: {contact.topic}")
        
        # Create submission record
        submission = {
            "id": len(contact_submissions) + 1,
            "email": contact.email,
            "topic": contact.topic,
            "message": contact.message,
            "timestamp": datetime.now().isoformat(),
            "status": "received"
        }
        
        # Store the submission (in production, save to database)
        contact_submissions.append(submission)
        
        # Here you would typically:
        # 1. Send an email notification to yourself
        # 2. Store in a database
        # 3. Send confirmation email to user
        
        logger.info(f"Contact form submitted successfully. ID: {submission['id']}")
        
        return {
            "success": True,
            "message": "Contact form submitted successfully!",
            "submission_id": submission["id"],
            "timestamp": submission["timestamp"]
        }
        
    except Exception as e:
        logger.error(f"Error processing contact form: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/contacts", response_model=dict)
async def get_contact_submissions():
    """
    Get all contact form submissions (for admin purposes)
    """
    logger.info(f"Getting all submissions. Total: {len(contact_submissions)}")
    return {
        "submissions": contact_submissions,
        "total": len(contact_submissions),
        "debug_info": {
            "server_started": True,
            "memory_storage": True,
            "note": "Data will be lost when server restarts"
        }
    }

@app.get("/contacts/{submission_id}")
async def get_contact_submission(submission_id: int):
    """
    Get a specific contact form submission by ID
    """
    logger.info(f"Requesting submission ID: {submission_id}")
    logger.info(f"Total submissions in memory: {len(contact_submissions)}")
    logger.info(f"Available IDs: {[s['id'] for s in contact_submissions]}")
    
    if submission_id <= 0 or submission_id > len(contact_submissions):
        raise HTTPException(
            status_code=404, 
            detail=f"Submission not found. Available IDs: {[s['id'] for s in contact_submissions]}"
        )
    
    return contact_submissions[submission_id - 1]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
