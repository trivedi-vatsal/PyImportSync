#!/usr/bin/env python3
"""
Sample Python application that imports various packages.
This is used to test the dependency checker.
"""

import os
import sys
import json
from pathlib import Path

# Third-party imports that should be in requirements.txt
import requests
import flask
import click
from pydantic import BaseModel

# This import is missing from requirements.txt (for testing)
# import numpy  # Uncomment to test missing dependency detection


class User(BaseModel):
    name: str
    email: str


def main():
    """Main application function."""
    print("Sample application running...")

    # Use some imports to avoid unused import warnings
    app = flask.Flask(__name__)

    @app.route("/")
    def hello():
        user = User(name="Test", email="test@example.com")
        response = requests.get("https://httpbin.org/json")
        return f"Hello {user.name}! Status: {response.status_code}"

    print("Application configured successfully!")


if __name__ == "__main__":
    main()
