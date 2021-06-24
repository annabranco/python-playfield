from flask import Flask, render_template

# __name__ creates an app named after the file (app.py)
app = Flask(__name__)

# render_template may pass a variable to be used inside the template (2nd argument)
@app.route('/')
def index():
  return render_template('index.html', data=[
    { 'description': 'Todo 1' },
    { 'description': 'Todo 2' },
    { 'description': 'Todo 3' }
  ])

if __name__ == '__main__':
    app.run(
        debug=True,
        port=5000,
        host='0.0.0.0'
    )