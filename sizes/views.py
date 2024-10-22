from django.shortcuts import render
from .models import MaleTopSize, MaleBottomSize, FemaleTopSize, FemaleBottomSize
import logging

logger = logging.getLogger(__name__)

def chest_size_view(request):
    malebottomsize = MaleBottomSize.objects.all().values()
    if request.method == 'POST':
        logger.debug(f"Request data: {request.POST}")

        try:
            # Retrieve form data
            gender = request.POST.get('gender')
            clothing_type = request.POST.get('clothing_type')
            height_feet = int(request.POST.get('height_feet', 0))
            height_inches = int(request.POST.get('height_inches', 0))
            fit_preference = request.POST.get('fit_preference', 'avg')

            # Convert height to total inches
            total_height_in_inches = (height_feet * 12) + height_inches
            logger.debug(f'Total height in inches: {total_height_in_inches}')

            # Normalize 'other' to 'male' for processing
            if gender == 'other':
                gender = 'male'
            logger.debug(f'Normalized gender: {gender}')

            # Initialize suggested size variable
            suggested_size = None
            chest_size = waist_size = None
            
            # Retrieve size based on clothing type
            if clothing_type == 'top':
                chest_size = int(request.POST.get('chest_size', 0))
                suggested_size = get_top_size_suggestion(gender, chest_size, fit_preference)
            elif clothing_type == 'bottom':
                waist_size = int(request.POST.get('waist_size', 0))
                suggested_size = get_bottom_size_suggestion(gender, waist_size, fit_preference)
                print(f"{suggested_size}")
            logger.debug(f'Suggested Size: {suggested_size}')

            # Handle cases where no suggestion is found
            suggestion_display = suggested_size if suggested_size else 'N/A'

            context = {
                'gender': gender,
                'clothing_type': clothing_type,
                'suggestion': suggestion_display,
                'height_feet': height_feet,
                'height_inches': height_inches,
                'chest_size': chest_size,
                'waist_size': waist_size,
            }
            
            return render(request, 'chest_size.html', context)
        except ValueError as ve:
            logger.error(f'ValueError processing request: {ve}')
            context = {'error_message': 'Invalid input values. Please check your entries.'}
            return render(request, 'chest_size.html', context)
        except Exception as e:
            logger.error(f'Error processing request: {e}')
            context = {'error_message': 'An error occurred while processing your request.'}
            return render(request, 'chest_size.html', context)

    return render(request, 'chest_size.html')






def get_top_size_suggestion(gender, chest_size, fit_preference):
    if gender == 'male':
        suggestion =  MaleTopSize.objects.filter(chest=chest_size, fit_preference=fit_preference).first()
    elif gender == 'female':
        suggestion =  FemaleTopSize.objects.filter(chest=chest_size, fit_preference=fit_preference).first()
    else:
        suggestion =  None

    return suggestion.size if suggestion else None

def get_bottom_size_suggestion(gender, waist_size, fit_preference):
    if gender == 'male':
        suggestion = MaleBottomSize.objects.filter(waist=waist_size, fit_preference=fit_preference).first()
    elif gender == 'female':
        suggestion = FemaleBottomSize.objects.filter(waist=waist_size, fit_preference=fit_preference).first()
    else:
        suggestion = None

    # Return the size if a suggestion is found; otherwise, return None to handle it in the view.
    return suggestion.size if suggestion else None

