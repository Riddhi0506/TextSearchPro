from flask import Flask, render_template, request
import os
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import nltk

nltk.download('stopwords')

# nltk.data.path.append("/path/to/nltk_data")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/search1', methods=['GET','POST'])
def search1():
    if request.method == 'POST':
        data = {}
        count = 0
        word = request.form['search'].lower()
        path = 'static'
        files = os.listdir(path)
        stop_words = set(stopwords.words('english'))
        ps = PorterStemmer()

        for file_name in files:
            if file_name.endswith('.txt'):
                lines_with_match = []
                with open(os.path.join(path, file_name), 'r') as file:
                    lines = file.readlines()
                    for line_number, line in enumerate(lines, 1):
                        # Preprocessing steps
                        line = line.lower()
                        tokens = word_tokenize(line)
                        tokens = [ps.stem(token) for token in tokens if token.isalnum() and token not in stop_words]
                        line = ' '.join(tokens)

                        if word in line:
                            lines_with_match.append(f'Line {line_number} - {line.strip()}')

                if lines_with_match:
                    data[file_name] = lines_with_match
                    count = len(lines_with_match)
                else:
                    data[file_name] = [f"Word - '{word}' not found in '{file_name}' file"]

        return render_template('search.html', data=data, count=count, search=word)
    
# def search1():
#     if request.method == 'POST':
#         data = {}
#         count = 0
#         word = request.form['search'].lower()
#         path = 'static'
#         files = os.listdir(path)

#         for file_name in files:
#             if file_name.endswith('.txt'):
#                 lines_with_match = []
#                 with open(os.path.join(path, file_name), 'r') as file:
#                     lines = file.readlines()
#                     for line_number, line in enumerate(lines, 1):
#                         if word in line.lower():
#                             lines_with_match.append(f'Line {line_number} - {line.strip()}')

#             if lines_with_match:
#                     data[file_name] = lines_with_match
#                     count = len(lines_with_match)
#             else:
#                 data[file_name] = ["Word - (" + str(word) + ") not found in " + str(file_name) + " file"]

#         return render_template('search.html', data=data,count=count,search=word)



if __name__ == '__main__':
    app.run(port=8000,debug=True)