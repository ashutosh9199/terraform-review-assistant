import os
import hcl2
from typing import List, Dict, Any
from models.domain import Resource

class TerraformParser:
    def __init__(self, project_dir: str):
        self.project_dir = project_dir

    def parse(self) -> List[Resource]:
        resources: List[Resource] = []
        for root, _, files in os.walk(self.project_dir):
            for file in files:
                if file.endswith('.tf'):
                    file_path = os.path.join(root, file)
                    parsed_resources = self._parse_file(file_path)
                    resources.extend(parsed_resources)
        return resources

    def _parse_file(self, file_path: str) -> List[Resource]:
        resources = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                obj = hcl2.load(f)
                
            if 'resource' in obj:
                for res_block in obj['resource']:
                    # res_block is typically a dict like {'azurerm_storage_account': {'name': {...}}}
                    for res_type, res_dict in res_block.items():
                        # hcl2 sometimes leaves quotes around keys
                        clean_type = res_type.strip('"')
                        for res_name, res_props in res_dict.items():
                            clean_name = res_name.strip('"')
                            resources.append(Resource(
                                resource_type=clean_type,
                                name=clean_name,
                                properties=res_props,
                                file_path=file_path
                            ))
        except Exception as e:
            print(f"Error parsing file {file_path}: {e}")
        return resources
