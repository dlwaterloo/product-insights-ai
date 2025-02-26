import base64
import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

def generate(input_file, output_file):
    """Generate analysis from video file"""
    # Load environment variables
    load_dotenv()

    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    # Upload file and wait briefly to ensure it's ready
    print("Uploading video file...")
    file = client.files.upload(file=str(input_file))
    print("Video file uploaded successfully.")

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_uri(
                    file_uri=file.uri,
                    mime_type=file.mime_type,
                ),
                types.Part.from_text(
                    text="""Please analyze this product and provide a detailed research output in JSON format. Include the following:

{
  "product_name": "Name of the product being demonstrated",
  "product_category": "Category of the product (e.g., Mobile App, Web Service, Hardware)",
  "executive_summary": "A brief overview of what the product does and its key features",
  "product_overview": {
    "description": "Detailed description of the product",
    "target_audience": "Who this product is designed for",
    "key_features": ["List of main features shown"]
  },
  "workflow_steps": [
    {
      "timestamp": "MM:SS",
      "description": "What happens at this step",
      "is_major_step": boolean,
      "ui_elements": ["List of UI elements visible/interactive in this step"],
      "user_interaction": "Description of how user interacts at this step",
      "design_analysis": "Analysis of the design decisions and UX implications",
      "technical_observations": "Any technical details or implementation notes visible"
    }
  ],
  "key_findings": {
    "usability_insights": ["List of insights about usability"],
    "design_patterns": ["Notable design patterns used"],
    "technical_highlights": ["Key technical features observed"]
  }
}

Please ensure:
1. Timestamps are in MM:SS format
2. Descriptions are detailed and analytical
3. Analysis focuses on both UX/UI and technical aspects"""
                ),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=0.1,  # Lower temperature for more structured output
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        response_mime_type="text/plain",
    )

    try:
        print("Generating analysis...")
        full_response = ""
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            chunk_text = chunk.text
            print(chunk_text, end="")
            full_response += chunk_text
        
        # Extract just the JSON part from the response
        json_start = full_response.find('{')
        json_end = full_response.rfind('}') + 1
        if json_start >= 0 and json_end > json_start:
            json_content = full_response[json_start:json_end]
            # Ensure the output directory exists
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, 'w') as f:
                f.write(json_content)
            print("\nAnalysis complete and saved to", output_file)
        else:
            print("\nError: Could not find valid JSON in the response")
    except Exception as e:
        print(f"\nError during analysis: {str(e)}")
        raise

if __name__ == "__main__":
    input_file = "path_to_your_video_file.mp4"
    output_file = "path_to_your_output_file.json"
    generate(input_file, output_file)