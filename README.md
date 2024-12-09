# FlowDroidReporter

FlowDroidReporter is a Python-based analysis tool designed to process and visualize the output of FlowDroid scans for Android applications. It extracts data flows (sources and sinks), generates interactive and static visualizations, and provides insights on potential malware risks and GDPR compliance using an integrated LLM (Large Language Model).

---

## Features

- **Source and Sink Analysis**:
  - Extracts source-sink relationships from FlowDroid XML output.
  - Provides detailed descriptions and risk assessments using an LLM.

- **Visualization**:
  - Generates **static visualizations** with `matplotlib` and `networkx`.
  - Supports **interactive graph layouts** (using PyVis in earlier versions, optional).

- **LLM Integration**:
  - Analyzes the purpose of sources and sinks.
  - Estimates the probability of data leakage or malware risk.
  - Evaluates GDPR compliance based on app functionality.

- **Customizable Graph Layouts**:
  - Supports spring, circular, shell, and Kamada-Kawai layouts for enhanced clarity.
  - Adjustable spacing and scaling to prevent label and node overlap.

---

## Files and Structure

| File                   | Description                                                                                   |
|------------------------|-----------------------------------------------------------------------------------------------|
| `main_app.py`          | Main entry point for running the tool. Parses FlowDroid XML, integrates LLM, and generates reports and graphs. |
| `config.py`            | Stores the OpenAI API key for LLM queries securely.                                           |
| `graph_generator.py`   | Contains functions for generating static visualizations with various layouts.                 |
| `llm_analysis.py`      | Handles LLM queries to analyze sources, sinks, and compliance assessments.                    |
| `xml_check.py`         | Script for testing and parsing FlowDroid XML outputs.                                         |
| `requirements.txt`     | Lists required Python packages for the project.                                               |

---

## Installation

### Prerequisites

- **Python**: Make sure Python 3.10 or higher is installed.
- **FlowDroid**: The tool processes XML outputs generated by FlowDroid scans.

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/aku762/FlowDroidReporter.git
   cd FlowDroidReporter
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the OpenAI API key:
   - Edit the `config.py` file and add your API key:
     ```python
     OPENAI_API_KEY = "your_openai_api_key_here"
     ```

---

## Usage

### Running the Tool

To analyze a FlowDroid XML file, run the following command:

```bash
python main_app.py <path_to_xml_file>
```

For example:
```bash
python main_app.py ./apks/Output/com.example.app.xml
```

### Output

1. **Source and Sink Report**:
   - Printed to the terminal with descriptions, risk probabilities, and GDPR compliance evaluations.

2. **Static Graph**:
   - A visualization of the data flow graph with labeled nodes and edges.

---

## Example Workflow

### Input: Sample FlowDroid XML

The tool processes XML files containing source-sink pairs from FlowDroid scans.

### Output: Terminal and Graph

#### Terminal Output

```plaintext
--- Source and Sink Report ---

Source: <com.example.Foo: void doSomething(android.content.Context)>
Sink: <com.example.Bar: void saveData(android.content.Context)>
  - Description: Captures user data and saves it to storage.
  - Risk Level: Medium (60% probability)

--- GDPR Compliance Assessment ---
- Status: Potentially Non-Compliant
- Reasoning: Captures user data but lacks mechanisms for deletion.
```

#### Static Graph

- A graph with labeled nodes (sources and sinks) and color-coded roles:
  - **Green**: Source
  - **Red**: Sink
  - **Purple**: Source + Sink
  - **Blue**: Intermediate Nodes

---

## Layout Options

When generating static graphs, you can choose from multiple layout algorithms:

- **Spring Layout**: Force-directed layout for general-purpose visualization.
- **Circular Layout**: Nodes arranged in a circle for smaller graphs.
- **Kamada-Kawai Layout**: Optimized spacing based on graph distances.

Example usage with different layouts:
```python
generate_static_graph(df, "output_graph", layout_type="circular")
```

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push to your branch and open a pull request.

---

## License

This project is licensed under the MIT License. See `LICENSE` for details.

---

## Acknowledgments

- **FlowDroid**: For providing the static analysis tool that generates the XML outputs.
- **OpenAI**: For the LLM integration enabling insightful analyses.
- **Matplotlib and NetworkX**: For graph visualization tools.

---

### Let me know if you'd like further edits!