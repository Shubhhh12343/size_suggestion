from django.shortcuts import render
from .models import FemaleTopSize, FemaleBottomSize, MaleTopSize, MaleBottomSize

def chest_size_view(request):
    suggestion = None
    chest_size = None
    gender = None
    clothing_type = None
    error_message = None
    size_input = None

    if request.method == 'POST':
        gender = request.POST.get('gender')
        clothing_type = request.POST.get('clothing_type')
        size_input = request.POST.get('size_input')

        try:
            size_input = int(size_input)

            if gender == 'male' and clothing_type == 'top':
                suggestion = MaleTopSize.objects.filter(chest=size_input).first()
            elif gender == 'male' and clothing_type == 'bottom':
                suggestion = MaleBottomSize.objects.filter(waist=size_input).first()
            elif gender == 'female' and clothing_type == 'top':
                suggestion = FemaleTopSize.objects.filter(chest=size_input).first()
            elif gender == 'female' and clothing_type == 'bottom':
                suggestion = FemaleBottomSize.objects.filter(waist=size_input).first()

            # If no size is found, set an error message
            if not suggestion:
                error_message = f"No matching size found for {size_input}."
        except (ValueError, TypeError):
            error_message = "Invalid size input. Please enter a valid number."

    return render(request, 'chest_size.html', {
        'suggestion': suggestion,
        'gender': gender,
        'clothing_type': clothing_type,
        'error_message': error_message,
        'size_input': size_input  # For displaying the entered size in case of error
    })
