# llms-book-bans-benchmark

Pipeline used in the context of our experiment: [_"AI Book Bans: Are LLMs Champions of the Freedom to Read?"_](https://lil.law.harvard.edu)

Dataset available on HuggingFace: [LINK]

---

## Models tested

- [OpenAI GPT-3.5-turbo](https://platform.openai.com/docs/guides/gpt)
- [OpenAI GPT-4](https://platform.openai.com/docs/guides/gpt)
- [Google Palm2](https://ai.google/discover/palm2/) (text-bison-001)
- [Meta Llama2-13b-chat](https://ai.meta.com/llama/) via [Ollama](https://ollama.ai/library/llama2)
- [Meta Llama2-70b-chat](https://ai.meta.com/llama/) via [Ollama](https://ollama.ai/library/llama2)

---

## Running the pipeline

### Dependencies
- Python 3.11+
- [Poetry](https://python-poetry.org/)

### Steps
1. Install dependencies: `poetry install`
2. Copy `.env.example` as `.env` and populate it with relevant credentials
3. Run `poetry run python run.py`
