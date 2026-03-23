# SIMKO AI — Product Description Writer

> A multi-agent AI pipeline that researches, drafts, and refines SEO-optimised product descriptions for e-commerce brands.

---

## What it does

Most AI writing tools rephrase what you give them. SIMKO AI works like a real copywriter — it researches first, then writes.

Give it a product name, a few features, and a target audience. It returns a polished, publish-ready description in seconds.

**Pipeline overview:**

```
User Input → Research Agent → Draft Agent → Refinement Agent → Output
```

1. **Research Agent** — Analyses the product category, maps audience psychology, and builds a structured brief
2. **Draft Agent** — Writes a first-pass description grounded in the research
3. **Refinement Agent** — Polishes tone, tightens flow, and weaves in SEO signals
4. **Output** — Returns the final copy, raw draft, and research notes for full transparency

---

## Tech Stack

| Layer | Technology |
|---|---|
| Agent Orchestration | LangGraph |
| LLM | OpenAI (GPT-4o) |
| Backend API | FastAPI |
| Frontend | Streamlit |
| Containerisation | Docker |
| Cloud Registry | AWS ECR |
| Language | Python 3.11+ |

---

## Getting Started

### Prerequisites
- Python 3.11+
- Docker (optional, for containerised run)
- OpenAI API key

### Installation

```bash
# Clone the repo
git clone https://github.com/your-username/simko-ai.git
cd simko-ai

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Add your OPENAI_API_KEY to .env
```

### Run locally

```bash
# Start the FastAPI backend
uvicorn main:app --reload

# In a separate terminal, launch the Streamlit frontend
streamlit run interface.py
```

### Run with Docker

```bash
docker build -t simko-ai .
docker run -p 8000:8000 --env-file .env simko-ai
```

---

## API Reference

### `POST /generate`

Generates a product description through the full agent pipeline.

**Request body:**
```json
{
  "product_name": "Apex Frontier Jeans",
  "product_category": "Apparel / Menswear",
  "key_features": ["14oz Selvedge Denim", "Double-stitched seams", "Slim fit"],
  "target_audience": "Urban professionals aged 20-40",
  "tone": "Rugged"
}
```

**Response:**
```json
{
  "final_description": "...",
  "draft_description": "...",
  "research_notes": "..."
}
```

**Supported tones:** `Professional` · `Rugged` · `Luxury` · `Playful` · `Urgent` · `Informative`

---

## Project Structure

```
simko-ai/
├── agents/
│   ├── research_agent.py
│   ├── draft_agent.py
│   └── refinement_agent.py
├── graph/
│   └── pipeline.py          # LangGraph pipeline definition
├── interface.py              # Streamlit frontend
├── main.py                   # FastAPI entrypoint
├── Dockerfile
├── requirements.txt
└── .env.example
```

---

## Roadmap

- [ ] Batch generation (multiple products at once)
- [ ] Shopify / WooCommerce direct integration
- [ ] Custom tone fine-tuning per brand
- [ ] Multi-language output support
- [ ] Analytics dashboard for copy performance

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

---

## License

MIT

---

*Built by [Your Name] · If this helped you, drop a ⭐*
