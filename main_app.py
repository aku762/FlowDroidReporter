from llm_analysis import summarize_sources_and_sinks, query_llm
from graph_generator import generate_static_graph_with_gdpr_caption
import xml.etree.ElementTree as ET
import pandas as pd


def print_source_and_sink_report(report):
    """
    Print the Source and Sink Report to the terminal in a grouped and summarized format.
    """
    print("\n--- Source and Sink Report ---\n")
    grouped_report = {}  # Group by source-sink pairs

    for item in report:
        # Use (source, sink) tuple as the key
        key = (item.get("source"), item.get("sink"))
        if key not in grouped_report:
            grouped_report[key] = {
                "description": item["description"],
                "probability": item["probability"]
            }

    # Generate output for each source-sink pair
    for (source, sink), details in grouped_report.items():
        print(f"Source: {source}")
        print(f"Sink: {sink}")
        print(f"  - Description: {details['description']}")
        risk_level = "Low" if details["probability"] <= 30 else "Medium" if details["probability"] <= 70 else "High"
        print(f"  - Risk Level: {risk_level} ({details['probability']}% probability)\n")



def print_gdpr_compliance_assessment(compliance):
    """
    Print the GDPR Compliance Assessment to the terminal.
    """
    print("\n--- GDPR Compliance Assessment ---\n")
    print(f"Compliance Status: {compliance['status'].capitalize()}")
    print(f"Reasoning: {compliance['reason']}\n")


def main(file_path):
    """
    Main function to parse XML, analyze sources and sinks, and generate graphs.
    """
    try:
        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Extract and structure data
        results = []
        for result in root.findall(".//Result"):
            sink = result.find(".//Sink")
            sources = result.findall(".//Source")
            for source in sources:
                results.append({
                    "SinkStatement": sink.get("Statement"),
                    "SinkMethod": sink.get("Method"),
                    "SourceStatement": source.get("Statement"),
                    "SourceMethod": source.get("Method"),
                })

        # Create a DataFrame
        df = pd.DataFrame(results)

        # Summarize sources, sinks, and edges for LLM analysis
        print("Summarizing sources and sinks...")
        summary = summarize_sources_and_sinks(df)

        # Query the LLM for insights
        print("Querying LLM for Source and Sink Report and GDPR compliance...")
        feedback = query_llm(summary["sources"], summary["sinks"], summary["edges"])  # Pass edges

        # Print Source and Sink Report to the terminal
        print_source_and_sink_report(feedback["report"])

        # Print GDPR Compliance Assessment to the terminal
        print_gdpr_compliance_assessment(feedback["gdpr_compliance"])

        # Generate a static graph
        print("Generating static graph...")
        generate_static_graph_with_gdpr_caption(df, file_path.split("/")[-1].split("\\")[-1], feedback["gdpr_compliance"])

        print("Done! Graph has been generated.")
    
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except ET.ParseError:
        print("Error: Failed to parse the XML file. Ensure it is a valid XML document.")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python main_app.py <path_to_xml_file>")
    else:
        main(sys.argv[1])
