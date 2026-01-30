"""
Fine-tuning Script for RAG Chatbot Models
"""
import os
from typing import Optional, Dict
from openai import OpenAI, AzureOpenAI
import logging
import time

logger = logging.getLogger(__name__)


class FineTuningManager:
    """Manage OpenAI model fine-tuning"""
    
    def __init__(
        self,
        use_azure: bool = False,
        azure_endpoint: Optional[str] = None,
        azure_api_key: Optional[str] = None,
        openai_api_key: Optional[str] = None,
    ):
        """
        Initialize fine-tuning manager
        
        Args:
            use_azure: Whether to use Azure OpenAI
            azure_endpoint: Azure OpenAI endpoint
            azure_api_key: Azure OpenAI API key
            openai_api_key: OpenAI API key
        """
        if use_azure and azure_endpoint:
            self.client = AzureOpenAI(
                azure_endpoint=azure_endpoint,
                api_key=azure_api_key,
                api_version="2025-04-01-preview"
            )
        else:
            self.client = OpenAI(api_key=openai_api_key)
        
        self.use_azure = use_azure
    
    def upload_training_file(self, file_path: str) -> str:
        """
        Upload training file to OpenAI
        
        Args:
            file_path: Path to training data file (JSONL format)
        
        Returns:
            File ID
        """
        logger.info(f"Uploading training file: {file_path}")
        
        with open(file_path, 'rb') as f:
            response = self.client.files.create(
                file=f,
                purpose="fine-tune"
            )
        
        logger.info(f"File uploaded successfully. File ID: {response.id}")
        return response.id
    
    def create_fine_tuning_job(
        self,
        training_file_id: str,
        model: str = "gpt-4o-mini-2024-07-18",
        validation_file_id: Optional[str] = None,
        hyperparameters: Optional[Dict] = None,
        suffix: Optional[str] = None
    ) -> str:
        """
        Create fine-tuning job
        
        Args:
            training_file_id: ID of uploaded training file
            model: Base model to fine-tune
            validation_file_id: Optional validation file ID
            hyperparameters: Fine-tuning hyperparameters
            suffix: Custom suffix for fine-tuned model name
        
        Returns:
            Fine-tuning job ID
        """
        logger.info(f"Creating fine-tuning job for model: {model}")
        
        job_params = {
            "training_file": training_file_id,
            "model": model,
        }
        
        if validation_file_id:
            job_params["validation_file"] = validation_file_id
        
        if hyperparameters:
            job_params["hyperparameters"] = hyperparameters
        
        if suffix:
            job_params["suffix"] = suffix
        
        response = self.client.fine_tuning.jobs.create(**job_params)
        
        logger.info(f"Fine-tuning job created. Job ID: {response.id}")
        return response.id
    
    def get_job_status(self, job_id: str) -> Dict:
        """
        Get fine-tuning job status
        
        Args:
            job_id: Fine-tuning job ID
        
        Returns:
            Job status information
        """
        response = self.client.fine_tuning.jobs.retrieve(job_id)
        
        status_info = {
            "id": response.id,
            "status": response.status,
            "model": response.model,
            "fine_tuned_model": response.fine_tuned_model,
            "created_at": response.created_at,
            "finished_at": response.finished_at,
        }
        
        return status_info
    
    def wait_for_completion(
        self,
        job_id: str,
        check_interval: int = 60,
        max_wait_time: int = 3600
    ) -> Dict:
        """
        Wait for fine-tuning job to complete
        
        Args:
            job_id: Fine-tuning job ID
            check_interval: Seconds between status checks
            max_wait_time: Maximum time to wait in seconds
        
        Returns:
            Final job status
        """
        logger.info(f"Waiting for fine-tuning job {job_id} to complete...")
        
        start_time = time.time()
        
        while True:
            status_info = self.get_job_status(job_id)
            status = status_info["status"]
            
            logger.info(f"Job status: {status}")
            
            if status == "succeeded":
                logger.info(f"Fine-tuning completed! Model: {status_info['fine_tuned_model']}")
                return status_info
            
            elif status in ["failed", "cancelled"]:
                logger.error(f"Fine-tuning {status}")
                return status_info
            
            # Check timeout
            elapsed = time.time() - start_time
            if elapsed > max_wait_time:
                logger.warning(f"Max wait time ({max_wait_time}s) exceeded")
                return status_info
            
            time.sleep(check_interval)
    
    def list_fine_tuning_jobs(self, limit: int = 10) -> list:
        """
        List fine-tuning jobs
        
        Args:
            limit: Maximum number of jobs to return
        
        Returns:
            List of job information
        """
        response = self.client.fine_tuning.jobs.list(limit=limit)
        
        jobs = []
        for job in response.data:
            jobs.append({
                "id": job.id,
                "status": job.status,
                "model": job.model,
                "fine_tuned_model": job.fine_tuned_model,
                "created_at": job.created_at,
            })
        
        return jobs
    
    def cancel_job(self, job_id: str):
        """Cancel a fine-tuning job"""
        self.client.fine_tuning.jobs.cancel(job_id)
        logger.info(f"Cancelled fine-tuning job: {job_id}")
    
    def delete_model(self, model_id: str):
        """Delete a fine-tuned model"""
        self.client.models.delete(model_id)
        logger.info(f"Deleted model: {model_id}")


def run_fine_tuning_pipeline(
    training_file_path: str,
    validation_file_path: Optional[str] = None,
    base_model: str = "gpt-4o-mini-2024-07-18",
    use_azure: bool = False,
    azure_endpoint: Optional[str] = None,
    azure_api_key: Optional[str] = None,
    openai_api_key: Optional[str] = None,
    wait_for_completion: bool = True
) -> Dict:
    """
    Complete fine-tuning pipeline
    
    Args:
        training_file_path: Path to training data
        validation_file_path: Optional path to validation data
        base_model: Base model to fine-tune
        use_azure: Whether to use Azure OpenAI
        azure_endpoint: Azure OpenAI endpoint
        azure_api_key: Azure OpenAI API key
        openai_api_key: OpenAI API key
        wait_for_completion: Whether to wait for job completion
    
    Returns:
        Job information
    """
    # Initialize manager
    manager = FineTuningManager(
        use_azure=use_azure,
        azure_endpoint=azure_endpoint,
        azure_api_key=azure_api_key,
        openai_api_key=openai_api_key
    )
    
    # Upload training file
    training_file_id = manager.upload_training_file(training_file_path)
    
    # Upload validation file if provided
    validation_file_id = None
    if validation_file_path:
        validation_file_id = manager.upload_training_file(validation_file_path)
    
    # Create fine-tuning job
    job_id = manager.create_fine_tuning_job(
        training_file_id=training_file_id,
        model=base_model,
        validation_file_id=validation_file_id,
        suffix="rag-chatbot"
    )
    
    # Wait for completion if requested
    if wait_for_completion:
        result = manager.wait_for_completion(job_id)
        return result
    else:
        return manager.get_job_status(job_id)
