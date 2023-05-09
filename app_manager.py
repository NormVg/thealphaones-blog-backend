import shortuuid,os,json,zipfile



def blog_creator(writer,title,msg,date, time,email):
    used_id = os.listdir("static/data")
    id = None
    while True:
        id_ = shortuuid.uuid()
        if id not in used_id:
            id  = id_
            break
    os.mkdir("static/data/"+id)
    data = {
        "id":id,
        "author":writer,
        "title-blog":title,
        "disc":msg,
        "date":str(date),
        "time":time,
        "email":email
    }

    with open(f"static/data/{id}/metadata.json", "w") as outfile:
        json.dump(data, outfile ,indent=4)



    return id


def zip_data():
    zf = zipfile.ZipFile("temp/data.zip", "w")
    for dirname, subdirs, files in os.walk("static/data/"):
        zf.write(dirname)
        for filename in files:
            zf.write(os.path.join(dirname, filename))
    zf.close()

def remove_blog(id,email):
    used_id = os.listdir("static/data")
    if id in used_id:
        f = open(f"static/data/{id}/metadata.json")
        data = json.load(f)
        f.close()
        print(data["email"],email)
        if email == data["email"]:
            for i in os.listdir(f"static/data/{id}"):
                os.remove(f"static/data/{id}/"+i)
            os.rmdir(f"static/data/{id}")
            return 200
        else:
            return 302
    else:
        return 301