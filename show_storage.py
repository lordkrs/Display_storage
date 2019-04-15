from bottle import *
import json
import os
import platform
import string

def get_html_table(data):
    html_code = "<html><head><style>table, th, td {border: 1px solid black;border-collapse: collapse;}</style></head>"
    html_code += '<body><h2>My Storage</h2><table style="width:100%">'
    html_code += '<tr><th>File_name</th><th>Download</th></tr>'
    dir_name = os.path.dirname(data[0])
    if platform.system().lower() == "windows":
            html_code += '<tr><td><a href="/storage">Home</a></td>'
    html_code += '<tr><td><a href="/storage?path={}">{}</a></td>'.format(os.path.dirname(dir_name),os.path.dirname(dir_name))
    for path in data:
        if os.path.isdir(path):
            html_code += '<tr><td><a href="/storage?path={}">{}</a></td>'.format(path,path)
        else:
            html_code += '<tr><td>' + path + '</td>'
        if os.path.isfile(path):
            html_code += '<td><a href="/download_file?path={}">Download</a></td></tr>'.format(path)
        else: 
            html_code += '<td>-</td>'
    html_code += '</table></body></html>'

    return html_code

@get("/storage")
def show_storage():
    path = request.query.path if request.query.path else "/"
    return_list = []
    if platform.system().lower() == "windows" and path == "/":
        for letter in string.ascii_uppercase:
            if not os.path.exists(letter+":\\"):
                continue
            return_list.append(letter+":\\")
            
        return get_html_table(return_list)
    

    try:
        if not os.path.exists(path):
            raise Exception("Invalid path")
        
        list_data = os.listdir(path)
        
        for data in list_data:
            if path == "/":
                return_list.append(path +data)
            else:
                return_list.append(path + os.path.sep + data)
    except Exception, ex:
        abort(400, json.dumps({"error": str(ex)}) )
    code = get_html_table(return_list)
    return code



@get("/download_file")
def download_file():
    path = request.query.path if request.query.path else "/"
    if os.path.isfile(path):
        return static_file(os.path.basename(path), os.path.dirname(path))
    return {path: "is directory"}

run(host="0.0.0.0",port=8989)
