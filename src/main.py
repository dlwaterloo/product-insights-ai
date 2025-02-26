#!/usr/bin/env python3
import os
import argparse
from pathlib import Path
from dotenv import load_dotenv
import logging
from datetime import datetime
import shutil

from video_analysis import generate as analyze_video
from video_screenshots import extract_screenshots_from_json
from generate_docs import create_product_research

def setup_logging():
    """Configure logging based on environment variables"""
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    log_file = os.getenv('LOG_FILE', 'logs/app.log')
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(log_file)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def setup_directories():
    """Create necessary directories if they don't exist"""
    dirs = ['input', 'output', 'logs']
    for dir_path in dirs:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

def main():
    # Load environment variables
    load_dotenv()
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Generate product documentation from demonstration.')
    parser.add_argument('--input', required=True, help='Input file name (from input directory)')
    args = parser.parse_args()
    
    try:
        # Setup directories
        setup_directories()
        
        # Generate timestamp for this run
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Set up paths
        input_file = Path('input') / args.input
        temp_dir = Path('temp')
        output_dir = Path('output')
        
        # Create temporary directory for intermediate files
        temp_dir.mkdir(exist_ok=True)
        
        # Set up output paths
        json_output = temp_dir / f'analysis_{timestamp}.json'
        screenshots_dir = temp_dir / 'screenshots'
        doc_output = output_dir / f'product_research_{timestamp}.docx'
        
        logger.info(f"Starting analysis of {input_file}")
        
        # Run analysis
        analyze_video(input_file, json_output)
        logger.info(f"Analysis complete. JSON output saved to {json_output}")
        
        # Extract screenshots
        extract_screenshots_from_json(input_file, json_output, screenshots_dir)
        logger.info(f"Screenshots extracted to {screenshots_dir}")
        
        # Generate documentation
        create_product_research(json_output, screenshots_dir, doc_output)
        logger.info(f"Documentation generated at {doc_output}")
        
        # Move analysis file to output
        shutil.copy2(json_output, output_dir / f'analysis_{timestamp}.json')
        
        # Move screenshots to output
        screenshots_output_dir = output_dir / f'screenshots_{timestamp}'
        if screenshots_dir.exists():
            shutil.copytree(screenshots_dir, screenshots_output_dir)
        
        # Clean up temporary files
        shutil.rmtree(temp_dir)
        
        logger.info("Process completed successfully!")
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        raise

if __name__ == "__main__":
    main()
