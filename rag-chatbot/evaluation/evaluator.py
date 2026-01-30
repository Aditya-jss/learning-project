"""
Comprehensive Evaluation System for RAG Chatbot using Azure AI Evaluation SDK
"""
import os
import json
from typing import Dict, List, Optional
from pathlib import Path
from azure.ai.evaluation import (
    evaluate,
    RelevanceEvaluator,
    GroundednessEvaluator,
    CoherenceEvaluator,
    FluencyEvaluator,
    SimilarityEvaluator,
    RetrievalEvaluator,
    AzureOpenAIModelConfiguration,
    OpenAIModelConfiguration
)
from azure.identity import DefaultAzureCredential
import logging

logger = logging.getLogger(__name__)


class CustomAnswerLengthEvaluator:
    """Custom code-based evaluator for answer length"""
    
    def __init__(self, min_length: int = 10, max_length: int = 500):
        self.min_length = min_length
        self.max_length = max_length
    
    def __call__(self, *, response: str, **kwargs) -> Dict:
        """Evaluate answer length"""
        length = len(response)
        is_appropriate = self.min_length <= length <= self.max_length
        
        return {
            "answer_length": length,
            "length_appropriate": is_appropriate,
            "length_score": 1.0 if is_appropriate else 0.5
        }


class CustomContextRelevanceEvaluator:
    """Custom code-based evaluator for context relevance"""
    
    def __init__(self):
        pass
    
    def __call__(self, *, query: str, context: str, **kwargs) -> Dict:
        """Evaluate if context is relevant to query"""
        query_words = set(query.lower().split())
        context_words = set(context.lower().split())
        
        # Calculate overlap
        overlap = len(query_words & context_words)
        relevance_score = min(overlap / max(len(query_words), 1), 1.0)
        
        return {
            "context_relevance_score": relevance_score,
            "query_words_in_context": overlap
        }


class RAGEvaluator:
    """Comprehensive evaluator for RAG chatbot"""
    
    def __init__(
        self,
        use_azure: bool = False,
        azure_endpoint: Optional[str] = None,
        azure_api_key: Optional[str] = None,
        azure_deployment: Optional[str] = None,
        openai_api_key: Optional[str] = None,
        openai_model: str = "gpt-4o-mini",
        openai_base_url: Optional[str] = None,
    ):
        """
        Initialize RAG Evaluator with model configuration
        
        Args:
            use_azure: Whether to use Azure OpenAI
            azure_endpoint: Azure OpenAI endpoint (use Azure OpenAI endpoint, NOT Microsoft Foundry endpoint)
            azure_api_key: Azure OpenAI API key
            azure_deployment: Azure OpenAI deployment name
            openai_api_key: OpenAI API key
            openai_model: OpenAI model name
            openai_base_url: OpenAI base URL for compatible endpoints
        """
        # Configure model for prompt-based evaluators
        if use_azure and azure_endpoint:
            self.model_config = AzureOpenAIModelConfiguration(
                azure_endpoint=azure_endpoint,
                api_key=azure_api_key,
                azure_deployment=azure_deployment,
                api_version="2025-04-01-preview"
            )
        else:
            self.model_config = OpenAIModelConfiguration(
                type="openai",  # Required for OpenAI config
                model=openai_model,
                api_key=openai_api_key,
                base_url=openai_base_url
            )
        
        # Initialize built-in evaluators
        self._initialize_evaluators()
    
    def _initialize_evaluators(self):
        """Initialize all evaluators"""
        # RAG-specific evaluators
        self.groundedness_evaluator = GroundednessEvaluator(
            model_config=self.model_config
        )
        self.relevance_evaluator = RelevanceEvaluator(
            model_config=self.model_config
        )
        self.retrieval_evaluator = RetrievalEvaluator(
            model_config=self.model_config
        )
        
        # General quality evaluators
        self.coherence_evaluator = CoherenceEvaluator(
            model_config=self.model_config
        )
        self.fluency_evaluator = FluencyEvaluator(
            model_config=self.model_config
        )
        
        # Similarity evaluator (code-based, no model config needed)
        self.similarity_evaluator = SimilarityEvaluator()
        
        # Custom evaluators
        self.answer_length_evaluator = CustomAnswerLengthEvaluator()
        self.context_relevance_evaluator = CustomContextRelevanceEvaluator()
        
        logger.info("All evaluators initialized successfully")
    
    def evaluate_rag_system(
        self,
        test_data_path: str,
        output_path: str = "./evaluation/results",
        include_similarity: bool = False
    ) -> Dict:
        """
        Evaluate RAG system using Azure AI Evaluation SDK
        
        Args:
            test_data_path: Path to JSONL file with test data
                           Required columns: query, response, context
                           Optional columns: ground_truth (for similarity)
            output_path: Path to save evaluation results
            include_similarity: Whether to include similarity evaluation (requires ground_truth)
        
        Returns:
            Evaluation results with metrics and scores
        """
        logger.info(f"Starting RAG evaluation with data: {test_data_path}")
        
        # Prepare evaluators dictionary
        evaluators = {
            "groundedness": self.groundedness_evaluator,
            "relevance": self.relevance_evaluator,
            "retrieval": self.retrieval_evaluator,
            "coherence": self.coherence_evaluator,
            "fluency": self.fluency_evaluator,
            "answer_length": self.answer_length_evaluator,
            "context_relevance": self.context_relevance_evaluator,
        }
        
        # Prepare evaluator config with column mappings
        evaluator_config = {
            "groundedness": {
                "column_mapping": {
                    "query": "${data.query}",
                    "response": "${data.response}",
                    "context": "${data.context}"
                }
            },
            "relevance": {
                "column_mapping": {
                    "query": "${data.query}",
                    "response": "${data.response}"
                }
            },
            "retrieval": {
                "column_mapping": {
                    "query": "${data.query}",
                    "context": "${data.context}"
                }
            },
            "coherence": {
                "column_mapping": {
                    "query": "${data.query}",
                    "response": "${data.response}"
                }
            },
            "fluency": {
                "column_mapping": {
                    "response": "${data.response}"
                }
            },
            "answer_length": {
                "column_mapping": {
                    "response": "${data.response}"
                }
            },
            "context_relevance": {
                "column_mapping": {
                    "query": "${data.query}",
                    "context": "${data.context}"
                }
            }
        }
        
        # Add similarity evaluator if ground truth is available
        if include_similarity:
            evaluators["similarity"] = self.similarity_evaluator
            evaluator_config["similarity"] = {
                "column_mapping": {
                    "query": "${data.query}",
                    "response": "${data.response}",
                    "ground_truth": "${data.ground_truth}"
                }
            }
        
        # Run evaluation using evaluate() API
        result = evaluate(
            data=test_data_path,
            evaluators=evaluators,
            evaluator_config=evaluator_config,
            output_path=output_path
        )
        
        logger.info("Evaluation completed successfully")
        logger.info(f"Results saved to: {output_path}")
        
        return result
    
    def create_test_dataset(
        self,
        chatbot,
        test_queries: List[str],
        output_path: str = "./evaluation/test_data.jsonl",
        include_ground_truth: bool = False,
        ground_truths: Optional[List[str]] = None
    ) -> str:
        """
        Create test dataset by running chatbot on test queries
        
        Args:
            chatbot: RAG chatbot instance
            test_queries: List of test queries
            output_path: Path to save test dataset
            include_ground_truth: Whether to include ground truth answers
            ground_truths: List of ground truth answers (same order as queries)
        
        Returns:
            Path to created test dataset
        """
        logger.info(f"Creating test dataset with {len(test_queries)} queries")
        
        test_data = []
        
        for i, query in enumerate(test_queries):
            # Get response from chatbot
            result = chatbot.chat(query)
            
            # Combine context from source documents
            context = "\n\n".join([
                doc.get("content", "") for doc in result.get("source_documents", [])
            ])
            
            data_point = {
                "query": query,
                "response": result["response"],
                "context": context
            }
            
            # Add ground truth if available
            if include_ground_truth and ground_truths and i < len(ground_truths):
                data_point["ground_truth"] = ground_truths[i]
            
            test_data.append(data_point)
        
        # Save as JSONL
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            for item in test_data:
                f.write(json.dumps(item) + '\n')
        
        logger.info(f"Test dataset saved to: {output_path}")
        return output_path


def run_comprehensive_evaluation(
    chatbot,
    test_queries: List[str],
    ground_truths: Optional[List[str]] = None,
    use_azure: bool = False,
    azure_endpoint: Optional[str] = None,
    azure_api_key: Optional[str] = None,
    azure_deployment: Optional[str] = None,
    openai_api_key: Optional[str] = None,
) -> Dict:
    """
    Convenience function to run complete evaluation pipeline
    
    Args:
        chatbot: RAG chatbot instance
        test_queries: List of test queries
        ground_truths: Optional ground truth answers
        use_azure: Whether to use Azure OpenAI for evaluation
        azure_endpoint: Azure OpenAI endpoint
        azure_api_key: Azure OpenAI API key
        azure_deployment: Azure OpenAI deployment name
        openai_api_key: OpenAI API key
    
    Returns:
        Evaluation results
    """
    # Initialize evaluator
    evaluator = RAGEvaluator(
        use_azure=use_azure,
        azure_endpoint=azure_endpoint,
        azure_api_key=azure_api_key,
        azure_deployment=azure_deployment,
        openai_api_key=openai_api_key
    )
    
    # Create test dataset
    test_data_path = evaluator.create_test_dataset(
        chatbot=chatbot,
        test_queries=test_queries,
        include_ground_truth=ground_truths is not None,
        ground_truths=ground_truths
    )
    
    # Run evaluation
    results = evaluator.evaluate_rag_system(
        test_data_path=test_data_path,
        include_similarity=ground_truths is not None
    )
    
    return results
