from django.shortcuts import render
from .models import FemaleTopSize, FemaleBottomSize, MaleTopSize, MaleBottomSize

def chest_size_view(request):
    suggestion = None
    gender = None
    clothing_type = None
    size_input = None  # Initialize size_input with None to avoid UnboundLocalError

    if request.method == 'POST':
        print(f"{request.POST=}")
        gender = request.POST.get('gender')
        clothing_type = request.POST.get('clothing_type')
        size_input = request.POST.get('size_input')

        try:
            size_input = int(size_input)
            print(f"Received size input: {size_input}")

            # Check which model to filter based on gender and clothing type
            if gender == 'male' and clothing_type == 'top':
                suggestion = MaleTopSize.objects.filter(chest=size_input).first()
            elif gender == 'male' and clothing_type == 'bottom':
                suggestion = MaleBottomSize.objects.filter(waist=size_input).first()
            elif gender == 'female' and clothing_type == 'top':
                suggestion = FemaleTopSize.objects.filter(chest=size_input).first()
            elif gender == 'female' and clothing_type == 'bottom':
                suggestion = FemaleBottomSize.objects.filter(waist=size_input).first()

            print(f"Suggestion: {suggestion}")
        except (ValueError, TypeError):
            suggestion = None  # Handle invalid inputs
            print("Invalid size input")

        # Debugging prints
        print(f"Gender: {gender}, Clothing Type: {clothing_type}, Size Input: {size_input}")
        if suggestion:
            print(f"Suggestion Size: {suggestion.size if hasattr(suggestion, 'size') else 'No size found'}")
        else:
            print("No suggestion found")

    return render(request, 'chest_size.html', {
        'suggestion': suggestion,
        'gender': gender,
        'clothing_type': clothing_type,
        'size_input': size_input  # Fixing to pass the correct size_input
    })
