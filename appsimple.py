import sys,os
from flask import Flask, render_template, request, abort, send_file
from werkzeug.utils import secure_filename
from argparse import ArgumentParser


#def createapp(directory):
app = Flask(__name__)
if os.environ['FLASK_DIR']:
    app.config['UPLOAD_FOLDER']=os.environ['FLASK_DIR']
else:
    app.config['UPLOAD_FOLDER']="./"
app.config['MAX_CONTENT_PATH'] = 204800 #200MB
  #  return app

@app.route('/upload')
def upload():
   #return render_template('upload.html')
   return '''
   <html>
   <body>
      <form action = "uploader" method = "POST" 
         enctype = "multipart/form-data">
         <input type = "file" name = "file" />
         <input type = "submit" name="Upload"/>
      </form>   
   </body>
   </html>'''

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully'

@app.route('/', defaults={'req_path': ''})
@app.route('/<path:req_path>')
def list(req_path=''):
    base_dir = os.path.normpath(app.config['UPLOAD_FOLDER'])

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
        #print(os.path.join(abs_path,item))
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
    for f in files:
        if f != sys.argv[0]:
            output+="<li><a href="+f+">"+f+"</a><br>"
    return '''
    <html>
    <body>
    <h2>Directory Listing For %s:</h2>
    <hr>
    <ul>
    %s
    </ul>
    <hr>
    </body>
    </html>
    ''' % (req_path, output)


@app.errorhandler(404)
def not_found(error):
    return "Not Found", 404

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-h')
    parser.add_argument('-p')
    parser.add_argument('-d')
    args = parser.parse_args()
    if args.h:
        host=args.h
    else:
        host="0.0.0.0"
    if args.p:
        port=args.p
    else:
        port=int(80)
    if args.d:
        directory=args.d
    else:
        directory="./"
    app.config['UPLOAD_FOLDER']=directory
#    app=createapp(directory)
    app.run(host=host,port=port,debug = False)

