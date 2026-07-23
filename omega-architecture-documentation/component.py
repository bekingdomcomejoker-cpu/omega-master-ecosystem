#!/usr/bin/env python3
"""
Component module
"""
import json
from datetime import datetime

class Component:
    def __init__(self):
        self.initialized = True
        self.timestamp = datetime.now().isoformat()
    
    def get_status(self):
        return {"status": "ready", "timestamp": self.timestamp}

if __name__ == "__main__":
    comp = Component()
    print(json.dumps(comp.get_status(), indent=2))
