import os
import json
import sys
import nest_asyncio

# Required to run async loops inside notebooks/eval scripts
nest_asyncio.apply()

from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))

from signalnoise.api.routers.analyze import get_signalnoise_service

def generate_predictions(dataset_path: str) -> dict:
    with open(dataset_path, "r") as f:
        data = json.load(f)
        
    service = get_signalnoise_service()
    
    questions = []
    answers = []
    contexts = []
    ground_truths = []
    
    print("Generating predictions for Ragas evaluation...")
    for item in data:
        query = item["question"]
        questions.append(query)
        ground_truths.append(item["ground_truth"])
        
        try:
            print(f"Analyzing query: '{query}'")
            result = service.analyze(query=query, analysis_mode="comprehensive")
            
            answers.append(result.executive_summary)
            # Ragas expects context as a list of strings
            contexts.append([res.content for res in result.retrieval_results])
        except Exception as e:
            print(f"Error processing query '{query}': {e}")
            answers.append(f"Error: {e}")
            contexts.append([])
            
    return {
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths
    }

def run_evaluation():
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY not found in environment.")
        return
        
    dataset_path = os.path.join(os.path.dirname(__file__), "dataset.json")
    
    # 1. Get predictions
    data_dict = generate_predictions(dataset_path)
    
    # 2. Convert to HuggingFace Dataset
    dataset = Dataset.from_dict(data_dict)
    
    # 3. Setup Ragas LLM and Embeddings explicitly (optional, but good practice)
    # Ragas uses OpenAI by default if OPENAI_API_KEY is present
    
    metrics = [
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall,
    ]
    
    print("Starting Ragas evaluation...")
    result = evaluate(
        dataset=dataset,
        metrics=metrics,
    )
    
    print("\n--- Ragas Evaluation Results ---")
    print(result)
    
    # Save to file
    out_path = os.path.join(os.path.dirname(__file__), "ragas_results.json")
    # convert to dict and save
    df = result.to_pandas()
    df.to_json(out_path, orient="records", indent=4)
    print(f"Detailed results saved to {out_path}")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))
    run_evaluation()
