import sys,os,time
#from termcolor import colored
from flask import Flask, render_template, request, abort, send_file, redirect, url_for
from werkzeug.utils import secure_filename
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = "./"
app.config['MAX_CONTENT_PATH'] = 204800 #200MB
unlisted=[".gitignore","app.py","key","hosts","README.md","requirements",".git",".vscode","env","envwsl","oryx-manifest.toml","antenv.tar.gz",".github","__pycache__"]

try:
    with open("hosts","r") as f:
        allowed_addresses=[host.rstrip("\n") for host in f.readlines()]
except:
    allowed_addresses=[]
print("Allowed Hosts: {}".format(allowed_addresses))

login_form='''
    <html>
    <body>
    <form action = "%s" method = "POST">
      <label>Password: </label>
      <input type = "password" name = "key" />
      <input type = "submit"/>
    </form>
    </body>
    </html>'''

change_password_form= '''
        <html>
        <body>
        <form action = "adm" method = "POST">
         <label> Old Password: </label>
         <input type = "password" name = "key" /><br>
         <label> New Password: </label>
         <input type = "password" name = "newkey" /><br>
         <input type = "submit"/>
        </form>
        </body>
        </html>'''

upload_form='''
        <html>
        <body>
        <form action = "uploader" method = "POST"
         enctype = "multipart/form-data">
         <label> File: </label>
         <input type = "file" name = "file" />
         <input type = "text" hidden name="key" value="%s" />
         <input type = "submit"/>
        </form>
        </body>
        </html>'''
list_content='''
    <html>
    <head>
    <link href = "https://fonts.googleapis.com/icon?family=Material+Icons" rel = "stylesheet">
    <style>
    i {font-size: 6em; color: green;}
    </style>
    </head><body>
    <h2>Directory Listing:</h2>
    <hr>
    %s
    <hr>
    </body>
    </html>
    ''' 

try:
    with open("key","r") as f:
        key = f.read().strip()
except:
    key=None

@app.before_request
def limit_remote_addr():
    if not allowed_addresses:
        pass
    elif request.remote_addr not in allowed_addresses:
        abort(403)  # Forbidden
        #print("Accepting connections from the following addresses:")
        print(colored("Accepting connections from the following addresses:","cyan"))
        for a in allowed_addresses:
            print(colored(a+ " ","red"),end="")
        print("")

@app.route('/up',methods = ['GET', 'POST'])
def upload():
   #return render_template('upload.html')
    k=request.form.get("key")
    if k==key:
        return upload_form % k
    else:
       return login_form % "up"

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if key==None or request.method == 'POST' and request.form.get("key")==key:
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return 'file uploaded successfully'
    else:
        return redirect(url_for('upload')) 

@app.route('/adm',methods = ['GET', 'POST'])
def admin():
   #return render_template('upload.html')
    global key
    k=request.form.get("key")
    nk=request.form.get("newkey")
    if k==key and nk==None or nk=="" and k==key:
        return change_password_form 
    elif k==key and nk!="":
        with open("key","w") as f:
            key=str(nk)
            f.write(key)
        return "Key Changed"
    else:
       return login_form % "adm" 

@app.route('/',methods=["GET"])
def checkip():
    proxy_address = request.remote_addr
    client_ip = request.access_route[0]

    output="<html>Your IP Address: {} <br> Proxy Address: {}</html>".format(client_ip,request.remote_addr)
    return output, 200
    #return request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

@app.route('/down', defaults={'req_path': ''})
@app.route('/down/<path:req_path>')
def list(req_path=''):
    route="/down/" #change this to match @app.route above
    base_dir = os.path.normpath('./')
    # Joining the base and the requested path
    abs_path = os.path.normpath(os.path.join(base_dir, req_path))
    #print(abs_path)
    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)
    if os.path.isfile(abs_path):
        if req_path != sys.argv[0]:
            return send_file(abs_path)
        else:
            return abort(404)
    
    files=[]
    folders=[]
    items = sorted(os.listdir(abs_path),key=lambda f: os.path.getctime("{}/{}".format(abs_path, f)), reverse=True)
    for item in items:
        #print item
        #print(os.path.join(abs_path,item))
        if item not in unlisted:
            if os.path.isfile(os.path.join(abs_path, item)):
                files.append(item)
            #   print(files)
            else: #if os.path.isdir(os.path.join(abs_path, file)):
                folders.append(item)
            #  print(folders)

    parent = os.path.split(req_path)
    if abs_path == base_dir:
        req_path = ""
    elif req_path[-1:] != "/":
        req_path = req_path + "/"


    #print(files)
    #print(folders)
    output=""
    for f in folders:
        output+="<i class=\"material-icons\">folder</i><a href="+route+req_path+f+">"+f+"</a><br>"
    for f in files:
        if f != sys.argv[0]:
            output+="<i class=\"material-icons\">insert_drive_file</i><a href="+route+req_path+f+">"+f+"</a><br>"
    return list_content % output


@app.errorhandler(404)
def not_found(error):
    return "Not Found", 404

if __name__ == '__main__':
    host="0.0.0.0"
    port=80
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if ':' in arg:
            host, port = arg.split(':')
            port = int(port)
        else:
            try:
                port = int(sys.argv[1])
            except:
                host = sys.argv[1]
    app.run(host=host,debug = False,port=port)
