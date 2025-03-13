from flask import Flask, render_template, jsonify, request
import util
import parsing
from indexing import SearchEngine
import reranking
import logging
from flask_cors import CORS
import json
import os

se = SearchEngine()
app = Flask(__name__)
jdk = util.load_pkl('data/jdk_vocab.pkl')
CORS(app, supports_credentials=True)

# File paths
input_file_path = "/home/baoxuanlin/code/codematcher-demo/humaneval-java-parsed-problem.jsonl"
output_file_path = "/home/baoxuanlin/code/codematcher-demo/search_results.jsonl"

### Function to read descriptions from the input file
def read_descriptions_from_file(file_path):
    descriptions = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data = json.loads(line.strip())
            descriptions.append(data)
    return descriptions

@app.route('/')
def index():
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    app.logger.info(f"access from ip:{ip}")
    return render_template('index.html')

@app.route('/search/<query>', methods=['POST', 'GET'])
def search(query):
    app.logger.info("query" + "*" * 50)
    app.logger.info(query)
    query_parse = parsing.parse(query)

    data, cmds = se.fuzzy_search(query_parse, top_k=10)
    results = reranking.reranking(query_parse, data, cmds, jdk)
    app.logger.info("results" + "*" * 50)
    for result in results:
        app.logger.info(result)

    json = jsonify({"result": results})
    return json

### Function to process descriptions and write search results
def process_descriptions():
    # Read all descriptions from the input file
    descriptions = read_descriptions_from_file(input_file_path)
    
    # Open the output file for writing
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for desc in descriptions:
            print(desc)
            # Extract name and description, default to 'Unknown' if name is missing
            name = desc.get('name', 'Unknown')
            description = desc.get('description', '')
            
            # Use description as the query
            query = description
            query_parse = parsing.parse(query)
            print("解析结束")
            
            # Perform the search
            data, cmds = se.fuzzy_search(query_parse, top_k=5)
            print("模糊搜索结束")
            results = reranking.reranking(query_parse, data, cmds, jdk)
            print("重新排序结束")
            
            # Prepare the result entry
            result_entry = {
                'name': name,
                'description': description,
                'codematcher_results': results
            }
            
            # Write the result to the output file as a JSON line
            output_file.write(json.dumps(result_entry, ensure_ascii=False) + '\n')

### Logging configuration
def logging_setting():
    handler1 = logging.FileHandler(filename="flask.log", encoding="utf-8")
    app.logger.setLevel(logging.DEBUG)
    handler1.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s")
    handler1.setFormatter(formatter)
    app.logger.addHandler(handler1)

if __name__ == '__main__':
    logging_setting()
    # Process descriptions and write results when the app starts
    process_descriptions()
    # app.run(host='0.0.0.0')