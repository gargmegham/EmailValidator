from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.urls import reverse
from .models import emailFiles
import pandas as pd
from validate_email import validate_email
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import os
import requests
from django.conf import settings

def valid_email(email_address):
    # response = requests.get(
    #     "https://isitarealemail.com/api/email/validate",
    #     params = {'email': email_address})
    # try:
    #     print(response.json())
    #     status = response.json()['status']
    #     if status == "valid" or status == "invalid":
    #         return status
    #     else:
    #         return "unknown"
    # except Exception:
    #     return "unknown"
    return validate_email(email_address=email_address,
        check_format=True,
        check_blacklist=True,
        check_dns=True, dns_timeout=10,
        check_smtp=True, smtp_timeout=30, smtp_helo_host='my.host.name', smtp_debug=False)#, smtp_from_address='my@from.addr.ess'

def index(request):
    if "GET" == request.method:
        files = emailFiles.objects.all()
        context = {
            'files':files
        }
        return render(request, "index.html", context=context)
    try:
        file = request.FILES["inputFile"]
        if not file.name.endswith('.csv'):
            messages.error(request,'File is not CSV type')
            return HttpResponseRedirect(reverse("index"))
        if file.multiple_chunks():
            messages.error(request,"Uploaded file is too big (%.2f MB)." % (file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("index"))
        try:
            document = emailFiles.objects.create(file=file, name=file.name)
            document.save()
        except IntegrityError as ee:
            messages.error(request,'File with same name already present')
            return HttpResponseRedirect(reverse("index"))
        messages.success(request, f"Yout file {file.name} was saved.")
        return HttpResponseRedirect(reverse("index"))
    except Exception:
        messages.error(request,"Unable to upload, invalid file")
        return HttpResponseRedirect(reverse("index"))

def deleteFile(request):
    if "GET" == request.method:
        messages.info(request, "Don't try to get this view")
        return HttpResponseRedirect(reverse("index"))
    try:
        fileName = request.POST.get('fileName', None)
        emailFile = emailFiles.objects.get(name=fileName)
        emailFile.file.delete()
        emailFile.delete()
        if f'processed_{fileName}' in os.listdir(os.path.join(settings.MEDIA_ROOT)):
            os.remove(os.path.join(settings.MEDIA_ROOT, f'processed_{fileName}'))
        messages.success(request, f"Yout file {fileName} was deleted.")
        return HttpResponseRedirect(reverse("index"))
    except ObjectDoesNotExist:
        messages.error(request, f"file {fileName} not present")
        return HttpResponseRedirect(reverse("index"))
    except Exception as e:
        messages.error(request,"Unable to delete file due to -- {}" + repr(e))
        return HttpResponseRedirect(reverse("index"))

def processFile(request):
    if "GET" == request.method:
        messages.info(request, "Don't try to get this view")
        return HttpResponseRedirect(reverse("index"))
    try:
        fileName = request.POST.get('fileName', None)
        file = emailFiles.objects.get(name=fileName)
        if file.is_processed:
            messages.info(request, f"file {fileName} is already processed.")
            return HttpResponseRedirect(reverse("index"))
        df = pd.read_csv(file.file)
        emailList = df['email'].to_list()
        validStatus = list()
        for email in emailList:
            stat = valid_email(email)
            print(stat)
            validStatus.append(stat)
        df = df.assign(valid_status = validStatus)
        df.to_csv(os.path.join(settings.MEDIA_ROOT, f'processed_{fileName}'), index=False)
        file.file.close()
        file.is_processed=True
        file.save()
        messages.success(request, f"Yout file {fileName} was processed.")
        return HttpResponseRedirect(reverse("index"))
    except ObjectDoesNotExist:
        messages.error(request, "Invalid file name or file not present")
        return HttpResponseRedirect(reverse("index"))
    except Exception as err:
        messages.error(request, f"Some error occured {err}")
        return HttpResponseRedirect(reverse("index"))

def downloadFile(request):
    if "GET" == request.method:
        messages.info(request, "Don't try to get this view")
        return HttpResponseRedirect(reverse("index"))
    try:
        fileName = request.POST.get('fileName', None)
        file = emailFiles.objects.get(name=fileName)
        if file.is_processed:
            with open(os.path.join(settings.MEDIA_ROOT, f'processed_{fileName}')) as response_file:
                response = HttpResponse(
                    response_file,
                    content_type='text/csv',
                    headers={'Content-Disposition': f'attachment; filename="processed_{fileName}"'},
                )        
        else:
            response = HttpResponse(
                file.file,
                content_type='text/csv',
                headers={'Content-Disposition': f'attachment; filename="{fileName}"'},
            )
        return response
    except ObjectDoesNotExist:
        messages.error(request, "Invalid file name or file not present")
        return HttpResponseRedirect(reverse("index"))
    except Exception as err:
        messages.error(request, f"Some error occured {err}")
        return HttpResponseRedirect(reverse("index"))
