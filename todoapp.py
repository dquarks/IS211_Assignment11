import re
import pickle
import os.path as opath
from flask import Flask, request, redirect, render_template

app = Flask(__name__)
cache_file = opath.isfile('cache.pkl')
if cache_file: #    Check if the list exists on initialization.
    try:
        with open('cache.pkl',  'rb') as f:
            todolist = pickle.load(f)
    except Exception as e:
        print('Something went wrong: ' + str(e))
        todolist = []
else:
    todolist = []

@app.route('/')
def main():
    return render_template('index.html', todolist=todolist)

@app.route('/submit', methods = ['POST'])
def submission():
    task = request.form['task']
    email = request.form['email']
    priority = request.form['priority']
    #   Not the best regex for email addresses, but the actual regex is much too complicated.
    if re.match(r"^[^@\s]+@[^@\s\.]+\.[^@\.\s]+$", email) and priority.lower() in ['low', 'medium', 'high']:
        todolist.append(task)
        return redirect('/')
    else:
        print('Submission failed.')
        return redirect('/')

@app.route('/clear')
def clear_list():
    todolist.clear()
    return redirect('/')

@app.route('/delete', methods = ['GET'])
def delete_item():
    item = request.args.get('item')
    todolist.remove(item)
    return redirect('/')

@app.route('/save')
def save_list():
    try:
        with open('cache.pkl', 'wb') as f: #     Create the file if it doesn't exist at saving.
            pickle.dump(todolist, f)
    except Exception as e:
        print('Something went wrong: ' + str(e))
    return redirect('/')

if __name__ == '__main__':
    app.run()
