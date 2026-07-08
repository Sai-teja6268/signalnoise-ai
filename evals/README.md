# SignalNoise AI - Evaluation Frameworks

This directory contains evaluation scripts for the SignalNoise AI system. We use **LangSmith** for tracing and dataset management, and **Ragas** for standard RAG (Retrieval-Augmented Generation) metrics.

## Setup

Ensure your environment variables are configured in the `.env` file at the root of the project:

```env
OPENAI_API_KEY=your_openai_key
LANGCHAIN_API_KEY=your_langchain_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=signalnoise_evals
```

## Datasets

- `dataset.json`: A seed dataset containing sample queries and expected outputs. You can expand this file with more test cases.

## Running LangSmith Evaluations

LangSmith evaluations will execute your pipeline and upload the traces to LangSmith UI, comparing the final answer to the `ground_truth` from the dataset.

```bash
python evals/eval_langsmith.py
```

## Running Ragas Evaluations

Ragas evaluations run locally and measure the RAG pipeline using multiple metrics (Faithfulness, Context Precision, Answer Relevancy, Context Recall).

```bash
python evals/eval_ragas.py
```

Results will be printed to the terminal and saved in `evals/ragas_results.json`.
