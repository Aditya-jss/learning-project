"""
Guardrails System for RAG Chatbot
"""
import re
from typing import Dict, List, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class GuardrailViolation:
    """Represents a guardrail violation"""
    rule: str
    message: str
    severity: str  # 'low', 'medium', 'high'


class GuardrailsManager:
    """Manage input and output guardrails"""
    
    def __init__(
        self,
        max_input_length: int = 2000,
        max_output_length: int = 2000,
        enable_content_filter: bool = True,
        enable_pii_detection: bool = True,
    ):
        self.max_input_length = max_input_length
        self.max_output_length = max_output_length
        self.enable_content_filter = enable_content_filter
        self.enable_pii_detection = enable_pii_detection
        
        # Blocked patterns
        self.blocked_patterns = [
            r'\b(hack|exploit|bypass|jailbreak)\b',
            r'\b(password|secret|token)\s*[:=]',
        ]
        
        # PII patterns
        self.pii_patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'credit_card': r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
        }
        
        # Toxic content keywords
        self.toxic_keywords = [
            'hate', 'violence', 'harassment', 'discrimination',
            'illegal', 'harmful', 'dangerous'
        ]
    
    def validate_input(self, text: str) -> Dict:
        """Validate input text against guardrails"""
        violations = []
        
        # Check length
        if len(text) > self.max_input_length:
            violations.append(GuardrailViolation(
                rule="max_length",
                message=f"Input exceeds maximum length of {self.max_input_length} characters",
                severity="high"
            ))
        
        # Check for empty input
        if not text.strip():
            violations.append(GuardrailViolation(
                rule="empty_input",
                message="Input cannot be empty",
                severity="high"
            ))
        
        # Check for blocked patterns
        if self.enable_content_filter:
            for pattern in self.blocked_patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    violations.append(GuardrailViolation(
                        rule="blocked_content",
                        message="Input contains blocked content",
                        severity="high"
                    ))
        
        # Check for PII
        if self.enable_pii_detection:
            pii_found = self._detect_pii(text)
            if pii_found:
                violations.append(GuardrailViolation(
                    rule="pii_detected",
                    message=f"PII detected: {', '.join(pii_found)}",
                    severity="medium"
                ))
        
        # Check for toxic content
        toxic_found = self._detect_toxic_content(text)
        if toxic_found:
            violations.append(GuardrailViolation(
                rule="toxic_content",
                message="Potentially toxic content detected",
                severity="high"
            ))
        
        return {
            "is_valid": len([v for v in violations if v.severity == "high"]) == 0,
            "violations": violations,
            "sanitized_text": self._sanitize_text(text) if self.enable_pii_detection else text
        }
    
    def validate_output(self, text: str) -> Dict:
        """Validate output text against guardrails"""
        violations = []
        
        # Check length
        if len(text) > self.max_output_length:
            violations.append(GuardrailViolation(
                rule="max_length",
                message=f"Output exceeds maximum length of {self.max_output_length} characters",
                severity="medium"
            ))
            text = text[:self.max_output_length] + "..."
        
        # Check for PII in output
        if self.enable_pii_detection:
            pii_found = self._detect_pii(text)
            if pii_found:
                violations.append(GuardrailViolation(
                    rule="pii_detected",
                    message=f"PII detected in output: {', '.join(pii_found)}",
                    severity="high"
                ))
                text = self._sanitize_text(text)
        
        # Check for harmful content
        toxic_found = self._detect_toxic_content(text)
        if toxic_found:
            violations.append(GuardrailViolation(
                rule="toxic_content",
                message="Potentially toxic content detected in output",
                severity="high"
            ))
        
        return {
            "is_safe": len([v for v in violations if v.severity == "high"]) == 0,
            "violations": violations,
            "sanitized_text": text
        }
    
    def _detect_pii(self, text: str) -> List[str]:
        """Detect PII in text"""
        found = []
        for pii_type, pattern in self.pii_patterns.items():
            if re.search(pattern, text):
                found.append(pii_type)
        return found
    
    def _sanitize_text(self, text: str) -> str:
        """Remove PII from text"""
        sanitized = text
        for pii_type, pattern in self.pii_patterns.items():
            sanitized = re.sub(pattern, f"[REDACTED_{pii_type.upper()}]", sanitized)
        return sanitized
    
    def _detect_toxic_content(self, text: str) -> bool:
        """Detect toxic content in text"""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.toxic_keywords)


class GuardrailsWrapper:
    """Wrapper to apply guardrails to chatbot"""
    
    def __init__(self, chatbot, guardrails_manager: GuardrailsManager):
        self.chatbot = chatbot
        self.guardrails = guardrails_manager
    
    def chat(self, query: str) -> Dict:
        """Chat with guardrails applied"""
        # Validate input
        input_validation = self.guardrails.validate_input(query)
        
        if not input_validation["is_valid"]:
            high_violations = [v for v in input_validation["violations"] if v.severity == "high"]
            return {
                "query": query,
                "response": f"I cannot process this request due to: {high_violations[0].message}",
                "guardrails_violations": input_validation["violations"],
                "blocked": True
            }
        
        # Use sanitized input
        sanitized_query = input_validation["sanitized_text"]
        
        # Get response from chatbot
        response = self.chatbot.chat(sanitized_query)
        
        # Validate output
        output_validation = self.guardrails.validate_output(response["response"])
        
        if not output_validation["is_safe"]:
            response["response"] = "I apologize, but I cannot provide this response due to safety concerns."
            response["guardrails_violations"] = output_validation["violations"]
            response["blocked"] = True
        else:
            response["response"] = output_validation["sanitized_text"]
            if output_validation["violations"]:
                response["guardrails_warnings"] = output_validation["violations"]
        
        return response
