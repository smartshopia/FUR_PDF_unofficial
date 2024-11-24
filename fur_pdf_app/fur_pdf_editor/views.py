from django.shortcuts import render, redirect
from .forms import *
from .models import *
import fitz

# Create your views here.

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
    return render(request, 'bootstrap.html')

def pricing(request):
    return render(request, 'bootstrap.html')

def about(request):
    return render(request, 'bootstrap.html')

def contact(request):
    return render(request, 'bootstrap.html')

def upload_pdf(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('pdf_list')
    else:
        form = PDFUploadForm()
    return render(request, 'upload_pdf.html', {'form': form})

def pdf_list(request):
    pdfs = PDF.objects.all()
    return render(request, 'pdf_list.html', {'pdfs': pdfs})

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
