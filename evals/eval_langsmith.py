import os
import json
import uuid
import sys
from langsmith import Client, evaluate
from langsmith.evaluation import LangChainStringEvaluator

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))

from signalnoise.api.routers.analyze import get_signalnoise_service

def create_or_get_dataset(client: Client, dataset_name: str, dataset_path: str):
    # Load JSON dataset
    with open(dataset_path, "r") as f:
        data = json.load(f)
    
    if client.has_dataset(dataset_name=dataset_name):
        return client.read_dataset(dataset_name=dataset_name)
    
    print(f"Creating dataset {dataset_name} in LangSmith...")
    dataset = client.create_dataset(
        dataset_name=dataset_name,
        description="Dataset for testing SignalNoise AI pipeline"
    )
    
    for item in data:
        client.create_example(
            inputs={"query": item["question"]},
            outputs={"answer": item["ground_truth"]},
            dataset_id=dataset.id,
        )
    return dataset

def predict(inputs: dict) -> dict:
    """Wrapper function to evaluate SignalNoise pipeline"""
    service = get_signalnoise_service()
    query = inputs["query"]
    
    try:
        # We pass default kwargs
        result = service.analyze(query=query, analysis_mode="comprehensive")
        
        # We extract the executive summary as the answer
        return {
            "answer": result.executive_summary,
            # We can also pass context if we need it for custom evaluators
            "contexts": [res.content for res in result.retrieval_results]
        }
    except Exception as e:
        return {"answer": f"Error: {e}", "contexts": []}

def run_evaluation():
    # Ensure LangSmith keys are present
    if not os.getenv("LANGCHAIN_API_KEY"):
        print("ERROR: LANGCHAIN_API_KEY not found in environment.")
        print("Please set LANGCHAIN_API_KEY and LANGCHAIN_TRACING_V2=true")
        return
        
    client = Client()
    dataset_name = "SignalNoise_Eval_v1"
    dataset_path = os.path.join(os.path.dirname(__file__), "dataset.json")
    
    dataset = create_or_get_dataset(client, dataset_name, dataset_path)
    
    # We can use a standard QA evaluator from LangChain
    qa_evaluator = LangChainStringEvaluator("qa")
    
    print("Starting LangSmith evaluation...")
    results = evaluate(
        predict,
        data=dataset_name,
        evaluators=[qa_evaluator],
        experiment_prefix="SignalNoise-Pipeline-Eval",
        # client=client,
    )
    print("Evaluation completed. Check LangSmith UI for detailed trace results.")

if __name__ == "__main__":
    # If using dotenv for local testing
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))
    
    run_evaluation()
