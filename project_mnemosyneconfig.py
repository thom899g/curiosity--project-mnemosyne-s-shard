"""
Configuration module for Project Mnemosyne's Shard
Centralized configuration management with type safety and validation
"""
import os
import json
from dataclasses import dataclass
from typing import Optional, Dict, Any
from pathlib import Path
import logging

@dataclass
class MnemosyneConfig:
    """Configuration dataclass with validation"""
    # RAM monitoring
    ram_threshold_percent: float = 95.0
    check_interval_seconds: int = 5
    ram_smoothing_window: int = 3
    
    # Shard creation
    max_shard_size_mb: int = 50
    compression_level: int = 6
    encryption_algorithm: str = "AES-GCM"
    
    # Firebase
    firebase_project_id: str = "evolution-ecosystem"
    firestore_collection: str = "cognition_fragments"
    
    # Marketplace
    base_price_sats: int = 1000  # Base price in satoshis
    urgency_multiplier: float = 1.5
    
    # Paths
    log_directory: str = "/var/log/mnemosyne"
    shard_storage_path: str = "/var/lib/mnemosyne/shards"
    pid_file: str = "/var/run/mnemosyne.pid"
    
    @classmethod
    def from_env(cls) -> 'MnemosyneConfig':
        """Load configuration from environment variables with fallbacks"""
        config = cls()
        
        # RAM settings
        if ram_thresh := os.getenv('MNEMOSYNE_RAM_THRESHOLD'):
            config.ram_threshold_percent = float(ram_thresh)
        
        if interval := os.getenv('MNEMOSYNE_CHECK_INTERVAL'):
            config.check_interval_seconds = int(interval)
            
        # Firebase settings
        if project_id := os.getenv('FIREBASE_PROJECT_ID'):
            config.firebase_project_id = project_id
            
        if collection := os.getenv('FIRESTORE_COLLECTION'):
            config.firestore_collection = collection
            
        # Path validation
        Path(config.log_directory).mkdir(parents=True, exist_ok=True)
        Path(config.shard_storage_path).mkdir(parents=True, exist_ok=True)
        
        return config
    
    def validate(self) -> bool:
        """Validate configuration values"""
        if not 0 < self.ram_threshold_percent <= 100:
            raise ValueError(f"RAM threshold must be between 0-100%, got {self.ram_threshold_percent}")
        
        if self.check_interval_seconds < 1:
            raise ValueError(f"Check interval must be >=1 second, got {self.check_interval_seconds}")
            
        if self.max_shard_size_mb <= 0:
            raise ValueError(f"Max shard size must be positive, got {self.max_shard_size_mb}")
            
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary for logging"""
        return {
            'ram_threshold_percent': self.ram_threshold_percent,
            'check_interval_seconds': self.check_interval_seconds,
            'max_shard_size_mb': self.max_shard_size_mb,
            'firebase_project_id': self.firebase_project_id,
            'firestore_collection': self.firestore_collection
        }