import sys
import os
import json
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from services.parser import TerraformParser
from services.rule_engine import RuleEngine

# Hardcoding a recent upload directory to see what it found
upload_dir = os.path.join(os.getcwd(), "backend", "uploads")
# Find the latest project dir
dirs = [os.path.join(upload_dir, d) for d in os.listdir(upload_dir) if os.path.isdir(os.path.join(upload_dir, d))]
latest_dir = max(dirs, key=os.path.getmtime)

print("Checking:", latest_dir)

parser = TerraformParser(latest_dir)
resources = parser.parse()

print(f"Found {len(resources)} resources.")
for res in resources:
    print(res.resource_type, res.name)

rule_engine = RuleEngine()
findings = rule_engine.analyze(resources)
print(f"Found {len(findings)} findings.")
for f in findings:
    print(f.issue)
