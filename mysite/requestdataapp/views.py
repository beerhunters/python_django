from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render

from requestdataapp.forms import UserBioForm, UploadFileForm


# Create your views here.
def process_get_view(request: HttpRequest) -> HttpResponse:
    a = request.GET.get('a', '')
    b = request.GET.get('b', '')
    result = a + b
    context = {
        'a': a,
        'b': b,
        'result': result,
    }
    return render(request, 'requestdataapp/request-query-params.html', context=context)


def user_form(request: HttpRequest) -> HttpResponse:
    context = {
        'form': UserBioForm(),
    }
    return render(request, 'requestdataapp/user-bio-form.html', context=context)


def handle_file_upload(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # myfile = request.FILES['myfile']
            myfile = form.cleaned_data['file']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            print('Saved file', filename)
    else:
        form = UploadFileForm()
    context = {
        'form': form
    }
    return render(request, 'requestdataapp/file-upload.html', context=context)


def upload_file(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST' and request.FILES.get('myfile'):
        file = request.FILES['myfile']
        # Проверяем размер файла
        if file.size > 1 * 1024 * 1024:  # 1 MB
            return HttpResponseBadRequest('The file is too big.')
        # Сохраняем файл
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        print('Saved file', filename)
        return HttpResponse('File successfully uploaded.')
    return render(request, 'requestdataapp/file-upload.html')