from django.shortcuts import render
from .models import MaleTopSize, MaleBottomSize, FemaleTopSize, FemaleBottomSize
import logging

logger = logging.getLogger(__name__)

def chest_size_view(request):
    maleBottomSize = MaleBottomSize.objects.all().values()
    if request.method == 'POST':
        logger.debug(f"Request data: {request.POST}")

        try:
            gender = request.POST.get('gender', '')
            clothing_type = request.POST.get('clothing_type', '')
            height_feet = request.POST.get('height_feet', '0')
            height_inches = request.POST.get('height_inches', '0')
            height_cm = request.POST.get('height_cm', '0')

            # Convert height fields to integers, handling empty strings
            height_feet = int(height_feet) if height_feet.strip() else 0
            height_inches = int(height_inches) if height_inches.strip() else 0
            height_cm = int(height_cm) if height_cm.strip() else 0

            # Convert height from cm to feet and inches if cm is provided
            if height_cm > 0:
                total_height_in_inches = height_cm / 2.54  # Convert cm to inches
                height_feet = int(total_height_in_inches // 12)
                height_inches = round(total_height_in_inches % 12)
                
                # Adjust if height_inches is 12 or more (e.g., 5 feet 12 inches should be 6 feet 0 inches)
                if height_inches == 12:
                    height_feet += 1
                    height_inches = 0
            else:
                total_height_in_inches = (height_feet * 12) + height_inches

            logger.debug(f'Total height in inches: {total_height_in_inches}')

            # Normalize 'other' to 'male' for processing
            if gender == 'other':
                gender = 'male'
            logger.debug(f'Normalized gender: {gender}')

            suggested_size = None
            chest_size = waist_size = None

            # Retrieve size based on clothing type
            if clothing_type == 'top':
                chest_size = int(request.POST.get('chest_size', '0')) if request.POST.get('chest_size') else 0
                if chest_size % 2 != 0:
                    chest_size += 1
                suggested_size = get_top_size_suggestion(gender, chest_size)
            elif clothing_type == 'bottom':
                waist_size = int(request.POST.get('waist_size', '0')) if request.POST.get('waist_size') else 0
                if waist_size % 2 != 0:
                    waist_size += 1
                suggested_size = get_bottom_size_suggestion(gender, waist_size)
                logger.debug(f'Suggested Size: {suggested_size}')

            suggestion_display = suggested_size if suggested_size else 'N/A'

            context = {
                'gender': gender,
                'clothing_type': clothing_type,
                'suggestion': suggestion_display,
                'height_feet': height_feet,
                'height_inches': height_inches,
                'chest_size': chest_size,
                'waist_size': waist_size,
                'height_cm': height_cm if height_cm > 0 else None,  # Pass height_cm if it's provided

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





def get_top_size_suggestion(gender, chest_size, ):
    if gender == 'male':
        suggestion =  MaleTopSize.objects.filter(chest=chest_size).first()
    elif gender == 'female':
        suggestion =  FemaleTopSize.objects.filter(chest=chest_size).first()
    else:
        suggestion =  None

    return suggestion.size if suggestion else None

def get_bottom_size_suggestion(gender, waist_size, ):
    if gender == 'male':
        suggestion = MaleBottomSize.objects.filter(waist=waist_size).first()
    elif gender == 'female':
        suggestion = FemaleBottomSize.objects.filter(waist=waist_size).first()
    else:
        suggestion = None

    # Return the size if a suggestion is found; otherwise, return None to handle it in the view.
    return suggestion.size if suggestion else None

