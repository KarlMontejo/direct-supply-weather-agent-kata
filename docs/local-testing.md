# Local Testing

## Prerequisites

- Python 3.11+
- Node.js 18+
- OpenAI API key

## Steps

1. **Configure env**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your `OPENAI_API_KEY`.

2. **Start backend**

   ```bash
   set -a && source .env && set +a
   uv run uvicorn backend.app.main:app --reload
   ```

   Backend runs at `http://localhost:8000`. Health check: `GET /health`.

3. **Start frontend**

   In a new terminal:

   ```bash
   cd frontend
   npm install
   npm run dev
   ```

   Frontend runs at `http://localhost:3000`.

4. **Test**

   Open `http://localhost:3000`, type a message (e.g. "I need chicken for 50 meals"), send. You should see a reply and tool usage under assistant messages.
