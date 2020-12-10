import os
def handle_uploaded_file(f):  
    with open(os.getcwd()+'/first_app/static/upload/'+f.name, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)       