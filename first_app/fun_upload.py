def handle_uploaded_file(f):  
    with open('first_app/static/upload/'+f.name, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)  