from llm_analysis import summarize_sources_and_sinks, query_llm
from graph_generator import generate_static_graph_with_gdpr_caption
import xml.etree.ElementTree as ET
import pandas as pd


def print_source_and_sink_report(report):
    """
    Print the Source and Sink Report to the terminal.
    """
    print("\n--- Source and Sink Report ---\n")
    for item in report:
        if "source" in item:
            print(f"Source: {item['source']}")
            print(f"  Description: {item['description']}")
            print(f"  Malware Risk Probability: {item['probability']}%\n")
        if "sink" in item:
            print(f"Sink: {item['sink']}")
            print(f"  Description: {item['description']}")
            print(f"  Malware Risk Probability: {item['probability']}%\n")


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

        # Summarize sources and sinks for LLM analysis
        print("Summarizing sources and sinks...")
        summary = summarize_sources_and_sinks(df)

        # Query the LLM for insights
        print("Querying LLM for Source and Sink Report and GDPR compliance...")
        feedback = query_llm(summary["sources"], summary["sinks"])

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
