import openai
import json
from config import OPENAI_API_KEY  # Use external API key

def sanitize_method_names(methods):
    """
    Sanitize method names to remove or escape problematic characters.
    """
    sanitized_methods = []
    for method in methods:
        sanitized_method = (
            method.replace("<", "[")
                  .replace(">", "]")
                  .replace(":", " -")
        )
        sanitized_methods.append(sanitized_method)
    return sanitized_methods


def summarize_sources_and_sinks(df):
    """
    Summarize source and sink data for LLM analysis, including their connections.
    """
    sources = df["SourceMethod"].unique().tolist()
    sinks = df["SinkMethod"].unique().tolist()
    edges = df[["SourceMethod", "SinkMethod"]].apply(tuple, axis=1).tolist()  # Extract connections

    return {
        "sources": sources,
        "sinks": sinks,
        "edges": edges,  # Include connections
    }


def query_llm(sources, sinks, edges):
    """
    Query the LLM to analyze sources, sinks, their connections, and GDPR compliance.
    """
    openai.api_key = OPENAI_API_KEY  # Use external API key

    # Truncate the lists and connections to avoid overly long prompts
    truncated_sources = sources[:10]
    truncated_sinks = sinks[:10]
    truncated_edges = edges[:10]

    # Format sources, sinks, and edges for clarity
    sources_text = "\n".join([f"- {src}" for src in truncated_sources])
    sinks_text = "\n".join([f"- {snk}" for snk in truncated_sinks])
    edges_text = "\n".join([f"- {src} -> {snk}" for src, snk in truncated_edges])

    prompt = f"""
    Analyze the following data flow from a mobile app:

    Sources:
    {sources_text}

    Sinks:
    {sinks_text}

    Connections:
    {edges_text}

    1. Provide a short description for each source and sink, including its purpose.
    2. Describe the significance of each connection and whether it poses a potential data leak risk.
    3. Estimate the probability (0-100%) that this source/sink combination could lead to a malware data leak.
    4. Assess whether the app complies with GDPR's "right to erasure" (true/false) and provide reasoning.

    Return results in the following format:
    {{
      "report": [
        {{"source": "SourceMethod1", "sink": "SinkMethod1", "description": "...", "probability": 85}},
        ...
      ],
      "gdpr_compliance": {{"status": "true/false", "reason": "..."}}
    }}
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a security and GDPR compliance expert with in-depth knowledge of malware forensics on Android applications."},
                {"role": "user", "content": prompt}
            ]
        )

        content = response['choices'][0]['message']['content'].strip()

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
