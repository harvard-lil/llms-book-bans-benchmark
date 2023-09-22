# llms-book-bans-benchmark

<a href="https://lil.law.harvard.edu/blog/2023/09/24/ai-book-bans-freedom-to-read-case-study/"><img src="https://lil-blog-media.s3.amazonaws.com/ai-book-bans-lead-graphic.png"></a>

Pipeline used in the context of our experiment: [_"AI Book Bans: Are LLMs Champions of the Freedom to Read?"_](https://lil.law.harvard.edu/blog/2023/09/24/ai-book-bans-freedom-to-read-case-study/)

Dataset available on [HuggingFace](https://huggingface.co/datasets/harvard-lil/llms-book-bans-benchmark).

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
