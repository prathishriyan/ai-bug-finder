# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)

### to run backend


### to run ollama

ollama pull phi

### push to git

1.Check git status
git status

2. add all changes
git add .

3.Commit your changes
git commit -m "Fix Monaco editor state, file upload, and C++ language support"


4.Push to GitHub
git push origin main

or if master?
git push origin master




##### FIRST TIME PUSH (repo exists but not linked)
🔹 Step 1: Initialize git (if needed)
git init

🔹 Step 2: Add remote repository

(copy URL from GitHub → Code → HTTPS)

git remote add origin https://github.com/USERNAME/REPO_NAME.git


Verify:

git remote -v

🔹 Step 3: Add, commit, push
git add .
git commit -m "Initial commit"
git branch -M main
git push -u origin main



##### If you change FRONTEND code (React)

Then run:

docker-compose build frontend
docker-compose up -d


OR rebuild only frontend:

docker-compose up --build frontend -d


#### If you change BACKEND code (FastAPI)

Then run:
docker-compose build backend
docker-compose up -d


OR rebuild only backend:

docker-compose up --build backend -d


#### If you change docker-compose.yml

Then ALWAYS do:
docker-compose down
docker-compose up --build -d


Because changes to docker-compose require full restart.


#### If you change Dockerfile

Example changes:

Changed Python version

Added dependencies

Updated COPY commands

Then do:
docker-compose build --no-cache
docker-compose up -d


#### If you forget which service to rebuild, you can always safely do:

docker-compose up --build -d


This will:

rebuild modified services only

restart containers automatically

without touching volumes



#### HOW TO USE YOUR AI BUG FINDER WEBSITE

⭐ Step 1 — Start all containers

Before using the website, run:

docker compose up -d


This starts:

Ollama (LLM model)

Backend (FastAPI)

Frontend (React + Nginx)

⭐ Step 2 — Wait 20 seconds

Ollama takes time to load the model inside the container.

Backend also needs a few seconds to connect to Ollama.

If you use it too quickly, you get errors like:

Unexpected token I
Internal Server Error
KeyError: response

⭐ Step 3 — Open the website in browser

Go to:

http://localhost


This is your frontend UI.

Not:

❌ localhost:80/analyze
❌ localhost:8000
❌ 0.0.0.0

Just:

http://localhost

⭐ Step 4 — Write or paste code

Inside the Monaco editor:

Choose Python / C / C++ / Java / JS

Paste your code or type it

⭐ Step 5 — Click “Analyze”

The UI will:

1️⃣ Send request to:

POST /api/analyze


2️⃣ Frontend automatically forwards to backend:

http://localhost:8000/analyze


3️⃣ Backend sends to Ollama:

http://ollama:11434/api/generate


4️⃣ Ollama returns fixed code

5️⃣ Frontend shows results

⭐ Step 6 — Check results

The UI displays:

❌ Errors

⚠️ Warnings

💡 Hints

✅ Solution

📌 Additional Tips

⭐ Step 7 — If something breaks
🔍 Check backend logs:
docker logs bugfinder-backend

🔍 Check Ollama logs:
docker logs ollama


If you see:

404 /api/generate


It means the model is not pulled yet (run ollama pull).

⭐ Step 8 — Stop the website

When done:

docker compose down



#####Simplest workflow for daily use

Whenever you want to use your AI Bug Finder app:

✔ Step 1:

docker compose up -d


✔ Step 2:
Open browser

http://localhost
    
