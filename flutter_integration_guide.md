# Flutter Contact Form Integration Guide

Since you already have a contact page in your Flutter app, here's how to connect it to this FastAPI backend:

## 1. Add HTTP Dependency

Add this to your `pubspec.yaml`:

```yaml
dependencies:
  http: ^1.1.0
```

Then run:
```bash
flutter pub get
```

## 2. Create a Service Class

Create a new file `lib/services/contact_service.dart`:

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class ContactService {
  // Change this URL to your deployed backend URL
  static const String baseUrl = 'http://localhost:8000';
  
  static Future<Map<String, dynamic>> submitContactForm({
    required String email,
    required String topic,
    required String message,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/contact'),
        headers: {'Content-Type': 'application/json'},
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

## 3. Update Your Existing Contact Form

In your existing contact page, replace your form submission logic with:

```dart
// Import the service
import 'package:your_app/services/contact_service.dart';

// In your form submission method:
Future<void> _submitForm() async {
  try {
    final result = await ContactService.submitContactForm(
      email: emailController.text,
      topic: topicController.text,
      message: messageController.text,
    );
    
    // Show success message
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('Message sent successfully!'),
        backgroundColor: Colors.green,
      ),
    );
    
    // Clear form
    emailController.clear();
    topicController.clear();
    messageController.clear();
    
  } catch (e) {
    // Show error message
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('Error sending message: $e'),
        backgroundColor: Colors.red,
      ),
    );
  }
}
```

## 4. Test the Integration

1. Make sure your FastAPI backend is running (`python main.py`)
2. Run your Flutter app
3. Fill out and submit the contact form
4. Check the backend logs to see the submission

## 5. For Production

When deploying:
1. Deploy your FastAPI backend to a cloud service
2. Update the `baseUrl` in `ContactService` to your deployed URL
3. Update CORS settings in the backend to allow your domain

## API Endpoint Details

**URL:** `POST /contact`

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

That's it! Your existing contact form will now send data to your FastAPI backend. 
