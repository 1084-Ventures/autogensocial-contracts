"""
AutoGenSocial Contracts

API contracts and data schemas for the AutoGenSocial platform.
"""

__version__ = "0.1.0"
__author__ = "1084 Ventures"
__email__ = "info@1084ventures.com"

# Import all models for easy access
from .models import Brand, Post, PostPlan, SocialAccount

# Make submodules available
from . import models
from . import schemas
from . import openapi

__all__ = [
    # Version info
    "__version__",
    "__author__", 
    "__email__",
    
    # Main models
    "Brand",
    "Post", 
    "PostPlan",
    "SocialAccount",
    
    # Submodules
    "models",
    "schemas", 
    "openapi",
]