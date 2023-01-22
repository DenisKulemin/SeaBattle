"""This file contains configuration classes for Prod and Dev environments."""
import os


class Config:
    """Base config class."""

    SECRET_KEY = os.environ.get("SEABATTLE_SECRET_KEY")
    HOST = os.environ.get("SEABATTLE_HOST", "0.0.0.0")
    PORT = os.environ.get("SEABATTLE_PORT", 8080)


class DevConfig(Config):
    """Class for Dev environment configuration."""

    ENV = "development"
    DEBUG = True
    TESTING = True


class ProdConfig(Config):
    """Class for Prod environment configuration."""

    ENV = "production"
    DEBUG = False
    TESTING = False
