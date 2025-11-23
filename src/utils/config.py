"""
Configuration management utilities
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional

try:
    from dotenv import load_dotenv
except ImportError:
    # Fallback when python-dotenv is not installed
    def load_dotenv(dotenv_path=None):
        """Mock load_dotenv function"""
        pass


class Config:
    """
    Configuration manager for the tax automation system
    """
    
    def __init__(self, env_file: Optional[str] = None):
        """
        Initialize configuration
        
        Args:
            env_file: Optional path to .env file
        """
        # Load environment variables
        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv()
        
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from environment variables"""
        return {
            # API Keys
            "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
            "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY", ""),
            
            # Vector Store
            "vector_store_type": os.getenv("VECTOR_STORE_TYPE", "chroma"),
            "vector_store_path": os.getenv("VECTOR_STORE_PATH", "./data/vector_store"),
            
            # Agent Configuration
            "max_parallel_agents": int(os.getenv("MAX_PARALLEL_AGENTS", "5")),
            "agent_timeout": int(os.getenv("AGENT_TIMEOUT", "300")),
            
            # Tax Documents
            "tax_documents_path": os.getenv("TAX_DOCUMENTS_PATH", "./data/tax_documents"),
            "tax_rules_path": os.getenv("TAX_RULES_PATH", "./data/tax_rules"),
            
            # Logging
            "log_level": os.getenv("LOG_LEVEL", "INFO"),
            "log_file": os.getenv("LOG_FILE", "./logs/tax_automation.log"),
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any):
        """
        Set configuration value
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self._config[key] = value
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration values"""
        return self._config.copy()
    
    def validate(self) -> bool:
        """
        Validate configuration
        
        Returns:
            True if configuration is valid
        """
        required_keys = ["vector_store_type", "max_parallel_agents"]
        
        for key in required_keys:
            if key not in self._config or not self._config[key]:
                return False
        
        return True
