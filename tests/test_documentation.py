import unittest
import os
import json
from pathlib import Path
from src.generate_docs import create_product_research

class TestDocumentation(unittest.TestCase):
    def setUp(self):
        self.test_data_dir = Path('tests/test_data')
        self.test_data_dir.mkdir(exist_ok=True)
        
        self.test_json = {
            "product_name": "Test Product",
            "product_category": "Test Category",
            "executive_summary": "Test summary",
            "product_overview": {
                "description": "Test description",
                "target_audience": "Test audience",
                "key_features": ["Feature 1", "Feature 2"]
            },
            "workflow_steps": [
                {
                    "description": "Test step",
                    "is_major_step": True,
                    "ui_elements": ["Element 1"],
                    "user_interaction": "Test interaction",
                    "design_analysis": "Test analysis",
                    "technical_observations": "Test observation"
                }
            ],
            "key_findings": {
                "usability_insights": ["Insight 1"],
                "design_patterns": ["Pattern 1"],
                "technical_highlights": ["Highlight 1"]
            }
        }
        
        # Save test JSON
        with open(self.test_data_dir / 'test_analysis.json', 'w') as f:
            json.dump(self.test_json, f)
            
        # Create test screenshots directory
        self.screenshots_dir = self.test_data_dir / 'screenshots'
        self.screenshots_dir.mkdir(exist_ok=True)
    
    def test_document_creation(self):
        """Test that document is created successfully"""
        output_file = self.test_data_dir / 'test_output.docx'
        
        # Generate document
        create_product_research(
            self.test_json,
            str(self.screenshots_dir),
            str(output_file)
        )
        
        # Check if document was created
        self.assertTrue(output_file.exists())
    
    def tearDown(self):
        # Clean up test files
        import shutil
        if self.test_data_dir.exists():
            shutil.rmtree(self.test_data_dir)

if __name__ == '__main__':
    unittest.main()
