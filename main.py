from typing import Union
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, field_validator
import logging
from datetime import datetime
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Portfolio Contact API", version="1.0.0")

# Add CORS middleware to allow requests from your Flutter web app
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://m-ahsan-bilal.github.io",  # Your GitHub Pages domain
        "https://ahsan.dev",  # Your custom domain
        "https://www.ahsan.dev",  # Your custom domain with www
        "http://localhost:3000",  # Local development
        "http://localhost:8080",  # Local development
        "http://localhost:5000",  # Flutter web default
        "http://localhost:5001",  # Flutter web alternative
        "http://localhost:8081",  # Flutter web alternative
        "http://127.0.0.1:3000",  # Local development
        "http://127.0.0.1:8080",  # Local development
        "http://127.0.0.1:5000",  # Flutter web localhost
        "http://127.0.0.1:5001",  # Flutter web alternative
        "http://127.0.0.1:8081",  # Flutter web alternative
        "http://localhost:59930"
        "http://localhost:59930/#/contact"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Pydantic model for contact form data validation
class ContactForm(BaseModel):
    email: EmailStr
    topic: str
    message: str
    
    @field_validator('topic')
    @classmethod
    def validate_topic(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('Topic must be at least 2 characters')
        if len(v) > 100:
            raise ValueError('Topic must be less than 100 characters')
        # Remove any potentially dangerous characters
        v = re.sub(r'[<>"\']', '', v)
        return v.strip()
    
    @field_validator('message')
    @classmethod
    def validate_message(cls, v):
        if len(v.strip()) < 10:
            raise ValueError('Message must be at least 10 characters')
        if len(v) > 2000:
            raise ValueError('Message must be less than 2000 characters')
        # Remove any potentially dangerous characters
        v = re.sub(r'[<>"\']', '', v)
        return v.strip()

# Store contact submissions (in a real app, you'd use a database)
contact_submissions = []

# Simple rate limiting - store recent submissions by IP
recent_submissions = {}

@app.get("/")
def read_root():
    return {"message": "Portfolio Contact API is running!", "status": "active"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/contact", response_model=dict)
async def submit_contact_form(contact: ContactForm, request: Request):
    """
    Submit a contact form with email, topic, and message
    """
    try:
        # Get client IP for rate limiting
        client_ip = request.client.host if request.client else "unknown"
        
        # Simple rate limiting: max 3 submissions per IP per hour
        current_time = datetime.now()
        if client_ip in recent_submissions:
            # Remove old entries (older than 1 hour)
            recent_submissions[client_ip] = [
                time for time in recent_submissions[client_ip] 
                if (current_time - time).seconds < 3600
            ]
            
            if len(recent_submissions[client_ip]) >= 3:
                raise HTTPException(
                    status_code=429, 
                    detail="Too many submissions. Please wait before submitting again."
                )
        
        # Add current submission to rate limiting
        if client_ip not in recent_submissions:
            recent_submissions[client_ip] = []
        recent_submissions[client_ip].append(current_time)
        
        # Log the contact submission
        logger.info(f"New contact form submission from: {contact.email} (IP: {client_ip})")
        logger.info(f"Topic: {contact.topic}")
        
        # Create submission record
        submission = {
            "id": len(contact_submissions) + 1,
            "email": contact.email,
            "topic": contact.topic,
            "message": contact.message,
            "timestamp": current_time.isoformat(),
            "status": "received",
            "ip_address": client_ip
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
        
    except HTTPException:
        raise
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
