from django.shortcuts import render
from .models import FemaleTopSize, FemaleBottomSize, MaleTopSize, MaleBottomSize

def chest_size_view(request):
    suggestion = None
    gender = None
    clothing_type = None
    size_input = None
    height_feet = None
    height_inches = None
    fit_preference = None  # New variable to capture fit preference

    if request.method == 'POST':
        print(f"Request POST Data: {request.POST}")
        gender = request.POST.get('gender')
        clothing_type = request.POST.get('clothing_type')
        size_input = request.POST.get('size_input')
        height_feet = request.POST.get('height_feet')
        height_inches = request.POST.get('height_inches')
        fit_preference = request.POST.get('fit_preference')  # Capture fit preference

        try:
            size_input = int(size_input)
            height_feet = int(height_feet)
            height_inches = int(height_inches)
            height_total_inches = (height_feet * 12) + height_inches
            print(f"Received size input: {size_input}, height: {height_total_inches} inches, fit preference: {fit_preference}")

            # Determine size suggestion based on fit preference
            if gender == 'male' and clothing_type == 'top':
                suggestion = MaleTopSize.objects.filter(chest=size_input, fit_preference=fit_preference).first()
            elif gender == 'male' and clothing_type == 'bottom':
                suggestion = MaleBottomSize.objects.filter(waist=size_input, fit_preference=fit_preference).first()
            elif gender == 'female' and clothing_type == 'top':
                suggestion = FemaleTopSize.objects.filter(chest=size_input, fit_preference=fit_preference).first()
            elif gender == 'female' and clothing_type == 'bottom':
                suggestion = FemaleBottomSize.objects.filter(waist=size_input, fit_preference=fit_preference).first()

            print(f"Suggestion: {suggestion}")
        except (ValueError, TypeError):
            suggestion = None
            print("Invalid size input or height input")

        # Debugging prints
        print(f"Gender: {gender}, Clothing Type: {clothing_type}, Size Input: {size_input}, Height: {height_feet}ft {height_inches}in")
        if suggestion:
            print(f"Suggestion Size: {suggestion.size if hasattr(suggestion, 'size') else 'No size found'}")
        else:
            print("No suggestion found")

    return render(request, 'chest_size.html', {
        'suggestion': suggestion,
        'gender': gender,
        'clothing_type': clothing_type,
        'size_input': size_input,
        'height_feet': height_feet,
        'height_inches': height_inches,
        'fit_preference': fit_preference  # Pass fit preference to template if needed
    })
