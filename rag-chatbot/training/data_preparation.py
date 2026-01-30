"""
Data Preparation and Training Script for RAG Chatbot
"""
import json
from pathlib import Path
from typing import List, Dict, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class DataPreparator:
    """Prepare training data for RAG chatbot"""
    
    def __init__(self, output_dir: str = "./training/data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def create_qa_pairs_from_documents(
        self,
        documents: List[str],
        output_file: str = "qa_training_data.jsonl"
    ) -> str:
        """
        Create question-answer pairs from documents
        This is a template - in practice, you'd use an LLM to generate Q&A pairs
        """
        qa_pairs = []
        
        logger.info(f"Generating Q&A pairs from {len(documents)} documents")
        
        # This is a placeholder - in production, use an LLM to generate meaningful Q&A pairs
        for i, doc in enumerate(documents):
            # Sample structure for training data
            qa_pair = {
                "document_id": f"doc_{i}",
                "context": doc[:500],  # First 500 chars
                "question": f"What is discussed in this document?",
                "answer": "This is a placeholder answer - use LLM to generate real Q&A pairs",
                "metadata": {
                    "source": "training_set",
                    "created_at": datetime.now().isoformat()
                }
            }
            qa_pairs.append(qa_pair)
        
        # Save as JSONL
        output_path = self.output_dir / output_file
        with open(output_path, 'w') as f:
            for pair in qa_pairs:
                f.write(json.dumps(pair) + '\n')
        
        logger.info(f"Created {len(qa_pairs)} Q&A pairs at {output_path}")
        return str(output_path)
    
    def prepare_fine_tuning_data(
        self,
        qa_pairs: List[Dict],
        output_file: str = "fine_tuning_data.jsonl",
        system_prompt: str = "You are a helpful AI assistant that answers questions based on provided context."
    ) -> str:
        """
        Prepare data in OpenAI fine-tuning format
        """
        fine_tuning_data = []
        
        for pair in qa_pairs:
            training_example = {
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": f"Context: {pair['context']}\n\nQuestion: {pair['question']}"
                    },
                    {"role": "assistant", "content": pair["answer"]}
                ]
            }
            fine_tuning_data.append(training_example)
        
        # Save in OpenAI format
        output_path = self.output_dir / output_file
        with open(output_path, 'w') as f:
            for example in fine_tuning_data:
                f.write(json.dumps(example) + '\n')
        
        logger.info(f"Prepared {len(fine_tuning_data)} fine-tuning examples at {output_path}")
        return str(output_path)
    
    def create_evaluation_dataset(
        self,
        qa_pairs: List[Dict],
        output_file: str = "eval_data.jsonl",
        split_ratio: float = 0.2
    ) -> str:
        """
        Create evaluation dataset from Q&A pairs
        """
        import random
        
        # Shuffle and split
        random.shuffle(qa_pairs)
        eval_size = int(len(qa_pairs) * split_ratio)
        eval_pairs = qa_pairs[:eval_size]
        
        # Format for evaluation
        eval_data = []
        for pair in eval_pairs:
            eval_data.append({
                "query": pair["question"],
                "context": pair["context"],
                "ground_truth": pair["answer"]
            })
        
        # Save
        output_path = self.output_dir / output_file
        with open(output_path, 'w') as f:
            for item in eval_data:
                f.write(json.dumps(item) + '\n')
        
        logger.info(f"Created evaluation dataset with {len(eval_data)} examples at {output_path}")
        return str(output_path)


class ModelVersionManager:
    """Manage model versions and configurations"""
    
    def __init__(self, versions_dir: str = "./training/versions"):
        self.versions_dir = Path(versions_dir)
        self.versions_dir.mkdir(parents=True, exist_ok=True)
        self.versions_file = self.versions_dir / "versions.json"
        self.versions = self._load_versions()
    
    def _load_versions(self) -> Dict:
        """Load version history"""
        if self.versions_file.exists():
            with open(self.versions_file, 'r') as f:
                return json.load(f)
        return {"versions": [], "current": None}
    
    def _save_versions(self):
        """Save version history"""
        with open(self.versions_file, 'w') as f:
            json.dump(self.versions, f, indent=2)
    
    def register_version(
        self,
        version_name: str,
        model_id: str,
        description: str,
        metrics: Optional[Dict] = None,
        config: Optional[Dict] = None
    ) -> Dict:
        """Register a new model version"""
        version_info = {
            "version_name": version_name,
            "model_id": model_id,
            "description": description,
            "metrics": metrics or {},
            "config": config or {},
            "created_at": datetime.now().isoformat(),
            "is_current": False
        }
        
        self.versions["versions"].append(version_info)
        self._save_versions()
        
        logger.info(f"Registered version: {version_name}")
        return version_info
    
    def set_current_version(self, version_name: str):
        """Set a version as current"""
        for version in self.versions["versions"]:
            version["is_current"] = version["version_name"] == version_name
        
        self.versions["current"] = version_name
        self._save_versions()
        logger.info(f"Set current version to: {version_name}")
    
    def get_current_version(self) -> Optional[Dict]:
        """Get current version info"""
        if not self.versions["current"]:
            return None
        
        for version in self.versions["versions"]:
            if version["version_name"] == self.versions["current"]:
                return version
        return None
    
    def list_versions(self) -> List[Dict]:
        """List all versions"""
        return self.versions["versions"]
    
    def compare_versions(self, version1: str, version2: str) -> Dict:
        """Compare metrics between two versions"""
        v1_info = next((v for v in self.versions["versions"] if v["version_name"] == version1), None)
        v2_info = next((v for v in self.versions["versions"] if v["version_name"] == version2), None)
        
        if not v1_info or not v2_info:
            raise ValueError("One or both versions not found")
        
        comparison = {
            "version1": version1,
            "version2": version2,
            "metrics_comparison": {}
        }
        
        # Compare metrics
        for metric in v1_info["metrics"]:
            if metric in v2_info["metrics"]:
                comparison["metrics_comparison"][metric] = {
                    version1: v1_info["metrics"][metric],
                    version2: v2_info["metrics"][metric],
                    "difference": v2_info["metrics"][metric] - v1_info["metrics"][metric]
                }
        
        return comparison
