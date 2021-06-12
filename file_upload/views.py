from django.shortcuts import render, redirect
from .models import File
from .forms import FileUploadForm, FileUploadModelForm
import os
import uuid
from django.http import JsonResponse
from django.template.defaultfilters import filesizeformat
from cryptography.fernet import Fernet
from file_download.forms import BlogForm

# Create your views here.

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
     
# Show file list
def file_list(request):
    files = File.objects.all().order_by("-id")
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            blog_item = form.save(commit=False)
            blog_item.save()
            return redirect('file_upload:file_list')
    else:
        form = BlogForm()
     
    return render(request, 'file_upload/file_list.html', {'files': files ,'form': form})


# Regular file upload without using ModelForm
def file_upload(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # get cleaned data
            name = form.cleaned_data.get("name")
            raw_file = form.cleaned_data.get("file")
            new_file = File() 
            new_file.file = handle_uploaded_file(raw_file)
            new_file.name = name
            new_file.save()
            return redirect("file_upload:file_list")
    else:
        form = FileUploadForm()

    return render(request, 'file_upload/upload_form.html', {'form': form,
                                                            'heading': 'Upload files with Regular Form'})


def handle_uploaded_file(file):
    ext = file.name.split('.')[-1]
    file_name = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    # file path relative to 'media' folder
    file_path = os.path.join('files', file_name)
    absolute_file_path = os.path.join('media', 'files', file_name)

    directory = os.path.dirname(absolute_file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(absolute_file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return file_path


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





write_key()
key = load_key()

def delete_book(request, pk):
    if request.method == 'POST':
        book = File.objects.get(pk=pk)
        book.delete()
    return redirect('file_upload:file_list')




from .models import active
from django.contrib.auth.models import User

# Upload File with ModelForm
def model_form_upload(request):
    all_User = User.objects.all()
    if request.method == "POST":
        form = FileUploadModelForm(request.POST, request.FILES)
        if form.is_valid():
            key =b'15aabnx7m8ju6F7XKS_hhGeBKsI-xDzkWyV9Pyj3qU4='
            gg = key.decode()
            print(gg)
            #f = Fernet(key)
            sec_key = form.cleaned_data.get('sec_key')
            dd = str(sec_key)
            f = Fernet(sec_key)
            file = request.FILES.get("file").read()

            cen=f.encrypt(file)
            file = request.FILES.get("file").seek(0)
            file = request.FILES['file'].write(cen)
            print(key)
            form.save()
            return redirect("file_upload:file_list")
    else:
        form = FileUploadModelForm()

    return render(request, 'file_upload/upload_form.html', {'form': form,
                                                            'heading': 'Upload files with ModelForm','Active':all_User})

def upload_book(request):
   
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            key = load_key()
            secret_key = form.cleaned_data.get('secret_key')
            f = Fernet(key)
            
            #request.FILES['pdf']
            #pdf = form.cleaned_data.get('pdf')
            
            pdf = request.FILES.get("pdf").read()

            cen=f.encrypt(pdf)
            pdf = request.FILES.get("pdf").seek(0)

            
            
            
    
            pdf = request.FILES['pdf'].write(cen)
            print('kr------NN:-',key)
            

            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'upload_book.html', {
        'form': form
    })




# Upload File with ModelForm
def ajax_form_upload(request):
    form = FileUploadModelForm()
    return render(request, 'file_upload/ajax_upload_form.html', {'form': form,
                                                            'heading': 'File Upload with AJAX'})


# handling AJAX requests
def ajax_upload(request):
    if request.method == "POST":
        # 1. Regular save method
        # name = request.POST.get("name")
        # raw_file = request.FILES.get("file")
        # new_file = File()
        # new_file.file = handle_uploaded_file(raw_file)
        # new_file.name = name
        # new_file.save()

        # 2. Use ModelForm als ok.
        form = FileUploadModelForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            # Obtain the latest file list
            files = File.objects.all().order_by('-id')
            data = []
            for file in files:
                data.append({
                    "url": file.file.url,
                    "size": filesizeformat(file.file.size),
                    "name": file.name,
                    })
            return JsonResponse(data, safe=False)
        else:
            data = {'error_msg': "Only jpg, pdf and xlsx files are allowed."}
            return JsonResponse(data)
    return JsonResponse({'error_msg': 'only POST method accpeted.'})
