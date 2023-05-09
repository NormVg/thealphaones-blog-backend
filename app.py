from flask import Flask, request , render_template , redirect, send_file
import os ,datetime
from app_manager import *
UPLOAD_FOLDER = "./static/data/"
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024


@app.before_request
def before_request():
  i = os.listdir("temp")
  if len(i)-1 != 0:
    os.remove("temp/data.zip")

@app.route('/')
def index():
  return '<-- thealphaones blog backend service --> '

@app.route('/endpoint')
def endpoints():
  return '<-- thealphaones blog backend service --> <br> endpints <br> /blog <br> /blog-upload <br> /get-all-data <br>  /remove-blog '

@app.route('/blog')
def sender_blog():
  id = request.args.get("id")
  return redirect(f"static/data/{id}/index.html")


@app.route('/blog-upload', methods=['GET', 'POST'])
def upload_file():
  if request.method == 'POST':
    files = request.files.getlist('file')
    writer = request.form.get("writer")
    title_blog = request.form.get("title-blog")
    email = request.form.get("email")
    message = request.form.get("message")
    date = datetime.date.today()
    time  = datetime.datetime.now().strftime("%H:%M:%S")
    
    id = blog_creator(writer=writer,title=title_blog,email=email,msg=message,date=date,time=time)
    for file in files:
        file.save(os.path.join(app.config['UPLOAD_FOLDER']+id, file.filename))
     
  return render_template("uploadfiles.html")

@app.route('/get-all-data')
def get_all_data():
  zip_data()
  return send_file("temp/data.zip")

@app.route('/remove-blog', methods=['GET', 'POST'])
def delete_blog():
  if request.method == 'POST':
    email = request.form.get('email')
    id_ = request.form.get("id")
    res = remove_blog(id=id_,email=email)
    if 200 == res :
      return "succesfully removed the blog"
    elif 301 == res:
      return "no blog found of that id"
    elif 302 ==  res:
      return "email not mached with email in the blog "
  return render_template("blog_delete.html")


if __name__ == '__main__':
   app.run(debug=True)
