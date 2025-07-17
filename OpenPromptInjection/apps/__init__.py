from .Application import Application
from .DataSentinelDetector import DataSentinelDetector, DataSentinelDetector_with_key

def create_app(task, model, defense='no'):
    return Application(task, model, defense)