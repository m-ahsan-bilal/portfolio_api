# Portfolio Contact Form Backend

A FastAPI backend for handling contact form submissions from your Flutter portfolio website.

## Features

- ✅ Contact form submission with email, topic, and message
- ✅ Data validation using Pydantic
- ✅ CORS support for web applications
- ✅ Logging for debugging
- ✅ Health check endpoint
- ✅ Admin endpoints to view submissions

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Server

```bash
# Option 1: Using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Option 2: Using Python
python main.py
```

### 3. Access the API

- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## API Endpoints

### POST /contact
Submit a contact form

**Request Body:**
```json
{
  "email": "user@example.com",
  "topic": "Project Inquiry",
  "message": "Hi, I'm interested in working with you..."
}
```

**Response:**
```json
{
  "success": true,
  "message": "Contact form submitted successfully!",
  "submission_id": 1,
  "timestamp": "2024-01-15T10:30:00"
}
```

### GET /contacts
Get all contact submissions (admin use)

### GET /contacts/{submission_id}
Get a specific contact submission

### GET /health
Health check endpoint

## Testing the API

Run the test script to verify everything works:

```bash
python test_api.py
```

## Integration with Flutter Web

### Example Flutter Code

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class ContactService {
  static const String baseUrl = 'http://localhost:8000'; // Change to your server URL
  
  static Future<Map<String, dynamic>> submitContactForm({
    required String email,
    required String topic,
    required String message,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/contact'),
        headers: {
          'Content-Type': 'application/json',
        },
        body: jsonEncode({
          'email': email,
          'topic': topic,
          'message': message,
        }),
      );
      
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed to submit contact form');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }
}
```

## Next Steps for Production

1. **Database Integration**: Replace the in-memory storage with a proper database (PostgreSQL, MongoDB, etc.)
2. **Email Notifications**: Add email sending functionality to notify you of new submissions
3. **Authentication**: Add admin authentication for viewing submissions
4. **Rate Limiting**: Prevent spam submissions
5. **Environment Variables**: Use environment variables for configuration
6. **Deployment**: Deploy to a cloud service (Heroku, Railway, DigitalOcean, etc.)

## Environment Variables (Recommended)

Create a `.env` file:

```env
DATABASE_URL=your_database_url
EMAIL_SERVICE_API_KEY=your_email_service_key
ADMIN_EMAIL=your_email@example.com
```

## Security Considerations

- In production, change `allow_origins=["*"]` to your specific domain
- Add input sanitization
- Implement rate limiting
- Use HTTPS in production
- Add proper error handling

## Troubleshooting

1. **CORS Errors**: Make sure the CORS middleware is properly configured
2. **Port Already in Use**: Change the port in the uvicorn command
3. **Import Errors**: Ensure all dependencies are installed
4. **Email Validation**: The API uses Pydantic's EmailStr for validation

## Support

For issues or questions, check the FastAPI documentation or create an issue in your repository. 
