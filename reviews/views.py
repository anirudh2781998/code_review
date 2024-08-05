import os
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import CodeFile
from transformers import pipeline,AutoTokenizer,AutoModelForSequenceClassification
from .forms import CodeFileForm
import torch
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

# Load the Hugging Face model for code review
code_review_pipeline = pipeline('text-classification', model='distilbert-base-uncased')
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('upload_code')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def reviews_code(request, code_file_id):
    code_file = get_object_or_404(CodeFile, id=code_file_id)
    with open(code_file.file.path, 'r') as file:
        code_content = file.read()
    
    # Generate a code review
    review_result = code_review_pipeline(code_content[:512])  # Process only the first 512 characters for simplicity
    review = review_result[0]['label'] if review_result else 'No review available'
    
    context = {
        'code_file': code_file,
        'review': review,
    }
    return render(request, 'reviews/reviews_code.html', context)

def upload_code(request):
    if request.method == 'POST':
        form = CodeFileForm(request.POST, request.FILES)
        if form.is_valid():
            code_file = form.save(commit=False)
            code_file.user = request.user
            code_file.save()
            return redirect('reviews_code', code_file.id)
    else:
        form = CodeFileForm()
    return render(request, 'reviews/upload_code.html', {'form': form})

