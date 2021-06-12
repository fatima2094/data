import os
from django.http import HttpResponse, Http404, StreamingHttpResponse, FileResponse
from cryptography.fernet import Fernet
from six.moves import urllib
from .forms import FileDawnloadModelForm,BlogForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.
# Case 1: simple file download, very bad
# Reason 1: loading file to memory and consuming memory
# Can download all files, including raw python .py codes


def file_download(request, file_path):
    # do something...
    with open(file_path) as f:
        c = f.read()
    return HttpResponse(c)


# Case 2 Use HttpResponse to download a small file
# Good for txt, not suitable for big binary files
def media_file_download(request, file_path):
    with open(file_path, 'rb') as f:
        try:
            response = HttpResponse(f)
            response['content_type'] = "application/octet-stream"
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
        except Exception:
            raise Http404


# Case 3 Use StreamingHttpResponse to download a large file
# Good for streaming large binary files, ie. CSV files
# Do not support python file "with" handle. Consumes response time
def stream_http_download(request, file_path):
    try:
        response = StreamingHttpResponse(open(file_path, 'rb'))
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
        return response
    except Exception:
        raise Http404


# Case 4 Use FileResponse to download a large file
# It streams the file out in small chunks
# It is a subclass of StreamingHttpResponse
# Use @login_required to limit download to logined users
def file_response_download1(request, file_path):
    try:
        response = FileResponse(open(file_path, 'rb'))
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
        return response
    except Exception:
        raise Http404


def write_key():
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)


def load_key():
    """
    Loads the key from the current directory named `key.key`
    """
    return open("key.key", "rb").read()





def encrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it encrypts the file and write it
    """
    f = Fernet(key)
    #with open(filename, "rb") as file:
        # read all file data
    file_data = filename.read()

    encrypted_data = f.encrypt(file_data)
    #with open(filename, "wb") as file:
    filename.write(encrypted_data)

write_key()
key = load_key()
def decrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it decrypts the file and write it
    """
    f = Fernet(key)
    with open(filename, "rb") as file:
        # read the encrypted data
        encrypted_data = file.read()
    # decrypt data
    decrypted_data = f.decrypt(encrypted_data)
    # write the original file
    with open(filename, "wb") as file:
        file.write(decrypted_data)




# Case 5 Limit file download type - recommended
from django.core.files.temp import NamedTemporaryFile
    
def add(request):
    if request.method == 'POST':
        form = FileDawnloadModelForm(request.POST)
        if form.is_valid():

            form.save()
            return redirect('file_upload:file_list')
    return render(request, 'file_upload/ddd.html', {
        'formm': FileDawnloadModelForm()
    })
    
def add_blog(request):
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            blog_item = form.save(commit=False)
            blog_item.save()
            return redirect('file_upload:file_list')
    else:
        form = BlogForm()
    return render(request, 'file_upload/file_list.html', {'form': form})
           

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = FileDawnloadModelForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = FileDawnloadModelForm()

    return render(request, 'file_upload/ddd.html', {'form': form})
from file_upload.models import File
from .models import Downkey
from django.contrib import messages

def file_response_download(request, file_path):

    ext = os.path.basename(file_path).split('.')[-1].lower()
    # cannot be used to download py, db and sqlite3 files.
    sefile = File.objects.get(file=file_path)
    kee = Downkey.objects.all().last()
    
    me = kee.sec_key
    print('www',me)
    ser = sefile.sec_key
    print('dddd',ser)
    response = HttpResponse()  
    if me == ser :
        decFile = open(file_path, 'rb')
        key =b'xpB3tjKoCFwVVRx0X891gof8g_7if-yVT_KOYZZMmBs='
        sec = request.user.get_short_name()
        f = Fernet(ser)
        dec= decFile.read()
        cen=f.decrypt(dec)
        decFile = open(file_path, 'wb')
        dec= decFile.seek(0)
        dec= decFile.write(cen)
        dec=decFile.close()
        response = HttpResponse()                                                            

        with open(file_path,'rb') as fsock:

            #filename = urllib.parse.quote(fsock)                                                     
            response = HttpResponse()                                                            
            response['content_type'] = 'text/plain'                                              
            response['Content-Disposition'] = "attachment; fsock='{}'; fsock*=UTF-8''{}".format(fsock,fsock)
            response.write(fsock.read())

            decFile = open(file_path, 'rb')
            dec= decFile.read()
            cen=f.encrypt(dec)
            decFile = open(file_path, 'wb')
            dec= decFile.seek(0)
            dec= decFile.write(cen)
            dec=decFile.close()
                                                            
            return response
    else :
        messages.error(request, 'Wrong Secret Key :( ')
        return redirect('file_upload:file_list')
        
                                                        


    
  
 