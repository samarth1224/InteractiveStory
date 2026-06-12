module.exports = {
  apps: [
    {
      name: 'interactivestory-frontend',
      cwd: './frontend',
      script: 'npm',
      args: 'start',
      env: {
        NODE_ENV: 'production',
        NEXT_PUBLIC_API_URL: 'https://yourdomain.com/api', // To be updated by user
      },
    },
    {
      name: 'interactivestory-backend',
      cwd: './Backend',
      script: 'venv/bin/uvicorn', // Assuming venv is used in production
      args: 'app.main:app --host 127.0.0.1 --port 8000 --workers 4',
      interpreter: 'none',
      env: {
        ENVIRONMENT: 'production',
        // Other production env vars should be set here or in a .env file loaded by PM2
      },
    },
  ],
};
