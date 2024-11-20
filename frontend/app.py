# frontend/app.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import requests  # We will use this to make HTTP requests to the FastAPI backend

# Initialize Dash app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div([
    html.H1("Quiz Question Generator"),
    dcc.Input(id='topic-input', type='text', placeholder="Enter a topic", debounce=True),
    html.Button('Generate Question', id='submit-button', n_clicks=0),
    html.Div(id='question-output'),
    html.Div(id='answers-output')
])

# Callback function to generate question and answers
@app.callback(
    [Output('question-output', 'children'),
     Output('answers-output', 'children')],
    [Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('topic-input', 'value')]
)
def generate_question(n_clicks, topic):
    if n_clicks > 0 and topic:
        # Send POST request to FastAPI backend
        response = requests.post("http://127.0.0.1:8000/generate_question/", json={"topic": topic})
        
        # Process the response
        if response.status_code == 200:
            data = response.json()
            question = data.get('question', 'No question generated.')
            answers = data.get('answers', [])
            return f"Question: {question}", f"Answers: {', '.join(answers)}"
        else:
            return "Error generating question", ""
    
    return "", ""

if __name__ == "__main__":
    app.run_server(debug=True)
