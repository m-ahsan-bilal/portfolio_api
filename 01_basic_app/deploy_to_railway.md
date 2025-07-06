# Deploy Your FastAPI Backend to Railway

This guide will help you deploy your contact form API so it runs 24/7 and your Flutter web app can use it.

## Step 1: Prepare Your Code

### 1. Create a `Procfile` (for Railway)
Create a file called `Procfile` (no extension) in your `01_basic_app` folder:

```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### 2. Update `main.py` for Production
Change the last part of your `main.py`:

```python
if __name__ == "__main__":
    import uvicorn
    # For local development
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 3. Create `runtime.txt`
Create a file called `runtime.txt`:

```
python-3.11.0
```

## Step 2: Deploy to Railway

### 1. Create Railway Account
- Go to [railway.app](https://railway.app)
- Sign up with GitHub

### 2. Create New Project
- Click "New Project"
- Choose "Deploy from GitHub repo"
- Select your repository

### 3. Configure Deployment
- Railway will detect it's a Python app
- Set the root directory to `01_basic_app`
- Deploy!

### 4. Get Your URL
- After deployment, Railway gives you a URL like:
  `https://your-app-name.railway.app`
- This is your production API URL

## Step 3: Update Your Flutter App

In your Flutter app, change the API URL:

```dart
// Change this in your ContactService
static const String baseUrl = 'https://your-app-name.railway.app';
```

## Step 4: Test Production API

Visit your Railway URL:
- `https://your-app-name.railway.app/docs` - API documentation
- `https://your-app-name.railway.app/health` - Health check

## Alternative: Deploy to Heroku

### 1. Install Heroku CLI
Download from [devcenter.heroku.com](https://devcenter.heroku.com/articles/heroku-cli)

### 2. Create Heroku App
```bash
heroku create your-app-name
```

### 3. Deploy
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### 4. Get URL
```bash
heroku open
```

## Environment Variables (Optional)

For production, you might want to add:

```env
# In Railway/Heroku dashboard
DATABASE_URL=your_database_url
EMAIL_API_KEY=your_email_service_key
```

## Cost

- **Railway**: Free tier available, then $5/month
- **Heroku**: Free tier discontinued, $7/month minimum
- **DigitalOcean**: $5/month for basic droplet

## Next Steps

1. Deploy to Railway (easiest)
2. Test your Flutter app with the new URL
3. Add database for persistent storage
4. Add email notifications

Your API will now run 24/7 and be accessible from anywhere! 
