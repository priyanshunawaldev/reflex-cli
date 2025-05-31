from setuptools import setup, find_packages
import os

# Read README for long description
def read_readme():
    try:
        with open("README.md", "r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        return "🧠 Reflex - AI-Powered Terminal Productivity Tracker\n\nA powerful CLI tool that tracks your tasks, focus sessions, and work logs with AI-powered insights to help you improve your productivity over time."

# Read version from __init__.py or set default
def get_version():
    try:
        with open("reflex/__init__.py", "r") as f:
            for line in f:
                if line.startswith("__version__"):
                    return line.split("=")[1].strip().strip('"').strip("'")
    except FileNotFoundError:
        pass
    return "1.0.0"

setup(
    name="reflex_cli",
    version=get_version(),
    author="Priyanshu Nawal",
    author_email="priyanshu.nawal.dev@gmail.com",
    description="🧠 Reflex - AI-Powered Terminal Productivity Tracker",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/priyanshunawaldev/reflex-cli",
    project_urls={
        "Bug Tracker": "https://github.com/priyanshunawaldev/reflex-cli/issues",
        "Documentation": "https://github.com/priyanshunawaldev/reflex-cli#readme",
        "Source Code": "https://github.com/priyanshunawaldev/reflex-cli",
    },
    packages=find_packages(),
    package_dir={"": "."},
    classifiers=[
        "Development Status :: Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Environment :: Console",
    ],
    keywords="productivity, cli, ai, tasks, focus, terminal, tracking, pomodoro",
    
    # Core dependencies - minimal for basic functionality
    install_requires=[
        "typer>=0.9.0",
        "rich>=13.0.0",
        "python-dotenv>=1.0.0",
        "requests>=2.28.0",  # For Ollama and general HTTP requests
    ],
    
    # Optional dependencies for different AI providers and features
    extras_require={
        # All AI providers
        "ai": [
            "openai>=1.0.0",
            "anthropic>=0.7.0", 
            "google-generativeai>=0.3.0",
        ],
        
        # Individual AI providers
        "openai": ["openai>=1.0.0"],
        "anthropic": ["anthropic>=0.7.0"],
        "gemini": ["google-generativeai>=0.3.0"],
        "ollama": [],  # No extra deps needed, uses requests
        
        # Development dependencies
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "isort>=5.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "pre-commit>=3.0.0",
        ],
        
        # Documentation dependencies
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
        
        # All optional dependencies
        "all": [
            "openai>=1.0.0",
            "anthropic>=0.7.0", 
            "google-generativeai>=0.3.0",
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "isort>=5.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    
    # Console scripts
    entry_points={
        "console_scripts": [
            "reflex=main:app",
        ],
    },
    
    # Include additional files
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yml", "*.yaml"],
    },
    
    # Metadata
    license="MIT",
    platforms=["any"],
    zip_safe=False,
    
    # Python version compatibility
    python_requires=">=3.8",
)