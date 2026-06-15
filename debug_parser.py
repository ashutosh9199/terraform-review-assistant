import sys
import json
import os
sys.path.append(os.path.join(os.getcwd(), 'backend'))
from services.parser import TerraformParser

parser = TerraformParser(os.getcwd())
resources = parser.parse()

for res in resources:
    print(f"Type: {res.resource_type}, Name: {res.name}")
    print(f"Properties: {json.dumps(res.properties, indent=2)}")

