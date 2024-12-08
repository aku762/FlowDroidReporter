import openai
import json
from config import OPENAI_API_KEY  # Use external API key

def summarize_sources_and_sinks(df):
    """
    Summarize source and sink data for LLM analysis.
    """
    sources = df["SourceMethod"].unique().tolist()
    sinks = df["SinkMethod"].unique().tolist()

    return {
        "sources": sources,
        "sinks": sinks,
    }

def query_llm(sources, sinks):
    """
    Query the LLM to analyze sources, sinks, and GDPR compliance.
    """
    openai.api_key = OPENAI_API_KEY  # Use external API key

    prompt = f"""
    Analyze the following data flow from a mobile app:

    Sources:
    {sources}

    Sinks:
    {sinks}

    1. Provide a short description for each source and sink, including its purpose.
    2. Estimate the probability (0-100%) that this source/sink combination could lead to a malware data leak.
    3. Assess whether the app complies with GDPR's "right to erasure" (true/false/potentially) and provide reasoning.

    Return results in the following format:
    {{
      "report": [
        {{"source": "SourceMethod1", "description": "...", "probability": 85}},
        {{"sink": "SinkMethod1", "description": "...", "probability": 70}}
      ],
      "gdpr_compliance": {{"status": "true/false/potentially", "reason": "..."}}
    }}
    """
    try:
        print("\n--- Sending Query to LLM ---\n")
        print(f"Prompt:\n{prompt[:500]}...")  # Only show the first 500 characters

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a security and GDPR compliance expert."},
                {"role": "user", "content": prompt}
            ]
        )

        content = response['choices'][0]['message']['content'].strip()

        # Debugging: Log the raw content
        print("\n--- Raw API Response ---\n")
        print(content)

        # Extract JSON-like portion from the response
        start_idx = content.find("{")
        end_idx = content.rfind("}")
        if start_idx != -1 and end_idx != -1:
            json_content = content[start_idx:end_idx + 1]
            return json.loads(json_content)

        raise ValueError("No JSON content found in the response.")

    except openai.error.OpenAIError as e:
        print(f"OpenAI API Error: {e}")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    # Return a default fallback in case of failure
    return {"report": [], "gdpr_compliance": {"status": "potentially", "reason": "LLM query failed"}}
