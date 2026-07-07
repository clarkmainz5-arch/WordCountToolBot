# WordCountTool Bot

A simple Telegram bot that counts words, characters, sentences, paragraphs,
and estimates reading/speaking time for any text you send it.

Bot username: **@WordCountToolBot**

## Features
- Word count
- Character count (with and without spaces)
- Sentence count
- Paragraph count
- Estimated reading time
- Estimated speaking time
- Works on plain messages or via `/count <text>`

## Project structure
```
.
├── bot.py              # main bot logic
├── requirements.txt    # Python dependencies
├── Procfile            # tells Railway how to run the bot
├── .gitignore
├── .env.example
└── README.md
```

## 1. Get your bot token
1. Open Telegram, message **@BotFather**.
2. Run `/newbot`, follow the prompts, and set the username to
   `WordCountToolBot` (or whatever is available).
3. BotFather will give you a token like `123456789:AAExample-Token`.
   Keep this secret.

## 2. Run locally (optional, for testing)
```bash
git clone <your-repo-url>
cd wordcounttoolbot
python -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate
pip install -r requirements.txt

# copy the example env file and add your token
cp .env.example .env
# edit .env and paste your real token

export BOT_TOKEN=your_token_here   # or use a tool like python-dotenv
python bot.py
```
Then message your bot on Telegram to test it.

## 3. Push to GitHub
```bash
cd wordcounttoolbot
git init
git add .
git commit -m "Initial commit: WordCountTool Bot"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

## 4. Deploy on Railway
1. Go to [railway.app](https://railway.app) and log in with GitHub.
2. Click **New Project → Deploy from GitHub repo**.
3. Select the repo you just pushed.
4. Railway will detect it's a Python app via `requirements.txt`.
5. Go to the **Variables** tab in your Railway service and add:
   - `BOT_TOKEN` = your token from BotFather
6. Go to the **Settings** tab and make sure the **Start Command** is:
   ```
   python bot.py
   ```
   (Railway usually picks this up from the `Procfile` automatically as a
   worker process — if it tries to run it as a web service instead, set the
   start command manually here.)
7. Deploy. Check the **Deployments → Logs** tab — you should see
   `Bot starting with polling...`
8. Message your bot on Telegram — it should respond.

## Notes
- This bot uses **long polling**, not webhooks, so there's no need to
  configure a public URL or webhook endpoint on Railway.
- Never commit your real `BOT_TOKEN` to GitHub — only `.env.example` should
  be in the repo, and `.env` is already excluded via `.gitignore`.
- If you regenerate your token in BotFather (`/revoke`), update the
  `BOT_TOKEN` variable in Railway too.
