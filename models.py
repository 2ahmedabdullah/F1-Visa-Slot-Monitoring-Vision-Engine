# models.py

import os
import re
import ollama 
import json
import base64
import pandas as pd
from groq import Groq
import sys
from dotenv import load_dotenv
from groq import AsyncGroq  

load_dotenv()

# Ensure standard Groq naming convention is respected
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or os.getenv("GROK_API_KEY")

if not GROQ_API_KEY:
    print("❌ Critical Error: Missing GROQ_API_KEY in environment variables.")
    sys.exit()

# Initialize clients explicitly with the validated key
client = Groq(api_key=GROQ_API_KEY)
llm_client = AsyncGroq(api_key=GROQ_API_KEY)

def encode_image_to_base64(image_path):
    """Encodes a local image file to a base64 string for Groq API ingestion."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# ==========================================
# EXTRACTION BLOCK SWAPPED TO GROQ CLOUD
# ==========================================

def fast_extract_table_groq(image_path):
    if not os.path.exists(image_path):
        print(f"Error: Image not found at {image_path}")
        return None, None
        
    prompt = """
    Analyze the image. If it contains a Cloudflare block page, an access denied / forbidden message, an error layout, or is completely blank/black, you must return exactly this structured JSON:
    {
      "table_data": [{"Visa Location": "ERROR_FORBIDDEN"}],
      "footer_timestamp": "Error Page"
    }
    
    Otherwise
    Extract the table rows and the bottom-most text timestamp line from the image exactly as they appear.
    You must output a structured JSON object with exactly these two keys:
    1. "table_data": An array of objects where each object contains:
       "Visa Location", "Visa Type", "Earliest Date", "Slots on Earliest Date", "Total Dates Available", "Last Seen At", "Relative Time"
    2. "footer_timestamp": The text string of the generation time row at the bottom.
    
    Return ONLY valid raw JSON data. Do not use markdown syntax block tags (```json).
    """
    
    try:
        print("⚡ Launching high-speed cloud LPU extraction matrix via meta-llama/llama-4-scout-17b-16e-instruct-preview...")
        
        # Convert local image to base64 data URI format for Groq
        base64_image = encode_image_to_base64(image_path)
        image_data_url = f"data:image/jpeg;base64,{base64_image}"
        
        # Call Groq API replacing ollama.generate
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",  # Ultra-fast, highly accurate vision model
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": image_data_url},
                        },
                    ],
                }
            ],
            temperature=0.0, # Strict accuracy, removes creative hesitation
            response_format={"type": "json_object"} # Guarantees structurally sound JSON output
        )
        
        # Extract the text content from Groq response object
        raw_text = response.choices[0].message.content.strip()

        # Remove markdown fences
        raw_text = re.sub(r"```(?:json)?", "", raw_text)
        raw_text = raw_text.replace("```", "").strip()

        # Extract JSON object only
        match = re.search(r"\{.*\}", raw_text, re.DOTALL)

        if not match:
            raise ValueError("No JSON object found in model output")

        json_text = match.group(0)
        json_text = re.sub(r",\s*([}\]])", r"\1", json_text) # Strip trailing commas

        result_json = json.loads(json_text)
        print(pd.DataFrame(result_json["table_data"]))
        return pd.DataFrame(result_json["table_data"]), result_json["footer_timestamp"]
        
    except Exception as e:
        print(f"⚠️ Local parser execution anomaly: {e}")
        try:
            print("\n===== RAW MODEL OUTPUT =====")
            print(raw_text)
            print("============================\n")
        except NameError:
            pass
            
        error_df = pd.DataFrame([{"Visa Location": "ERROR_PARSING_FAILED VAC"}])
        return error_df, "Error"
    

# ==========================================
# EXTRACTION BLOCK SWAPPED TO LOCAL CHIP
# ==========================================
def fast_extract_table(image_path, params, json_schema):
    if not os.path.exists(image_path):
        print(f"Error: Image not found at {image_path}")
        return None, None
        
    prompt = f"""
    Analyze the image.
       
    Otherwise
    Extract the table rows and the bottom-most text timestamp line from the image exactly as they appear.
    You must output a structured JSON object with exactly these two keys:
    1. "table_data": An array of objects where each object contains:
       "Visa Location", "Visa Type", "Earliest Date", "Slots on Earliest Date", "Total Dates Available", "Last Seen At", "Relative Time"
    2. "footer_timestamp": The text string of the generation time row at the bottom.
    
    Rules:
    - Do not stop until the JSON is fully complete
    - Do not truncate any field
    - Always close all brackets and braces
    - Output must be valid parsable JSON
    - No partial objects allowed

    Return ONLY valid raw JSON data. Do not use markdown syntax block tags (```json).

    Required JSON Schema:{json_schema}

    """
    
    try:
        print("🔮 Launching high-speed VRAM extraction matrix via qwen2.5vl:3b...")
        response = ollama.generate(
            model=params.get("model", "qwen2.5vl:3b"),
            prompt=prompt,
            format="json",
            images=[image_path],
            options={
                        "temperature": params.get("temperature"),
                        "num_predict": params.get("num_predict"),
                        "top_k": params.get("top_k"),
                        "top_p": params.get("top_p"),
                        "num_ctx": params.get("num_ctx"),
                        "num_gpu": -1,
                        "f16_kv": params.get("f16_kv"),
                        "stop": ["```"]
                    }
                )
        
        raw_text = response['response'].strip()

        # Remove markdown fences
        raw_text = re.sub(r"```(?:json)?", "", raw_text)
        raw_text = raw_text.replace("```", "").strip()
        print(type(raw_text))
        # Extract JSON object only
        match = re.search(r"\{.*\}", raw_text, re.DOTALL)

        if not match:
            raise ValueError("No JSON object found in model output")

        json_text = match.group(0)

        # Remove trailing commas before } or ]
        json_text = re.sub(r",\s*([}\]])", r"\1", json_text)

        # Debug output if needed
        # print(json_text)

        result_json = json.loads(json_text)
        print(type(result_json))

        table_key = "table_data" if "table_data" in result_json else "visa_rows"

        return pd.DataFrame(result_json.get(table_key, [])), result_json.get("footer_timestamp", "Error")
        
    except Exception as e:
        print(f"⚠️ Local parser execution anomaly: {e}")
        try:
            print("\n===== RAW MODEL OUTPUT =====")
            print(raw_text)
            print("============================\n")
        except:
            pass
        # Return a structured error fallback so the main loop triggers a 1-hour cooldown sleep
        error_df = pd.DataFrame([{"Visa Location": "ERROR_PARSING_FAILED VAC"}])
        return error_df, "Error"

