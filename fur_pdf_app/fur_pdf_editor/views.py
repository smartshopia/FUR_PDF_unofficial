from django.shortcuts import render, redirect
from .forms import *
from .models import *
import fitz
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.urls import reverse
from django.http import HttpResponse
from django.utils.crypto import get_random_string
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

# Create your views here.
#pages
def home(request):
    return render(request, 'home.html')

def tailwind(request):
    return render(request, 'tailwind.html')

def boot(request):
    return render(request, 'bootstrap.html')

def login_view(request):
    return render(request, 'login.html')

def signup_view(request):
    return render(request, 'signup.html')

def features(request):
    return render(request, 'features.html')

def pricing(request):
    return render(request, 'pricing.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')


#functions
def upload_pdf(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('pdf_list')
    else:
        form = PDFUploadForm()
    return render(request, 'upload_pdf.html', {'form': form})

@login_required
def pdf_list(request):
    pdfs = PDF.objects.all()
    return render(request, 'pdf_list.html', {'pdfs': pdfs})

@login_required
def view_pdf(request, pdf_id):
    pdf = PDF.objects.get(id=pdf_id)
    return render(request, 'view_pdf.html', {'pdf': pdf})

def view_pdf_old(request, pdf_id):
    pdf = PDF.objects.get(id=pdf_id)
    # Extract the first page of the PDF for preview
    doc = fitz.open(pdf.file.path)
    page = doc.load_page(0)  # Load the first page
    pix = page.get_pixmap()  # Render the page to an image
    image_path = f'media/pdf_images/{pdf_id}.png'
    pix.save(image_path)  # Save the image to disk
    return render(request, 'view_pdf.html', {'image_path': image_path, 'pdf': pdf})

@login_required
def convert_pdf_to_images(pdf_file_path):
    doc = fitz.open(pdf_file_path)
    images = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        image_path = f'media/pdf_images/page_{page_num}.png'
        pix.save(image_path)
        images.append(image_path)
    return images

# authentication

#magic link authentication
User = get_user_model()

def send_magic_link(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            token = get_random_string(32)
            user.profile.magic_token = token
            user.profile.token_created_at = timezone.now()
            user.profile.save()

            current_site = get_current_site(request)
            mail_subject = 'Your magic login link'
            message = render_to_string('magic_link_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token,
            })
            send_mail(mail_subject, message, 'no-reply@example.com', [email])
            return render(request, 'magic_link_sent.html', {'email': email})
        else:
            return HttpResponse('No user found with that email.')

"""  if user:
            token = get_random_string(32)
            user.profile.magic_token = token
            user.profile.token_created_at = timezone.now()
            user.profile.save()

            current_site = get_current_site(request)
            mail_subject = 'Your magic login link'
            message = render_to_string('magic_link_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token,
            })
            send_mail(mail_subject, message, 'no-reply@example.com', [email])

            return HttpResponse('A magic link has been sent to your email.')
    return render(request, 'send_magic_link.html') """


def verify_magic_link(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and user.profile.magic_token == token:
        user.profile.magic_token = None
        user.profile.save()
        login(request, user)
        return render(request, 'magic_link_success.html', {'user': user})
    else:
        return render(request, 'magic_link_invalid.html')