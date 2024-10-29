from django.shortcuts import render
from .models import MaleTopSize, MaleBottomSize, FemaleTopSize, FemaleBottomSize
import logging

logger = logging.getLogger(__name__)

def chest_size_view(request):
    if request.method == 'POST':
        logger.debug(f"Request data: {request.POST}")

        try:
            # Retrieve POST data
            gender = request.POST.get('gender', '')
            clothing_type = request.POST.get('clothing_type', '')
            height_feet = request.POST.get('height_feet', '0')
            height_inches = request.POST.get('height_inches', '0')
            height_cm = request.POST.get('height_cm', '0')  # Get height in cm
            chest_size_in = request.POST.get('chest_size', '0')  # Get chest size from form
            waist_size_in = request.POST.get('waist_size_in', '0')  # Get waist size from form

            # Retrieve chest size in cm
            chest_size_cm = request.POST.get('chest_size_cm', '0')  # Get chest size in cm
            waist_size_cm = request.POST.get('waist_size_cm', '0')  # Get waist size in cm

            # Handle height in cm
            total_height_in_cm = 0
            if height_cm and height_cm.strip():
                total_height_in_cm = round(float(height_cm))
            else:
                # Convert height fields to integers if feet and inches are provided
                height_feet = int(height_feet) if height_feet.strip() else 0
                height_inches = int(height_inches) if height_inches.strip() else 0
                total_height_in_inches = (height_feet * 12) + height_inches
                total_height_in_cm = round(total_height_in_inches * 2.54)  # Convert inches to cm
            
            logger.debug(f'Total height in cm: {total_height_in_cm}')

            suggested_size = None

            # Normalize 'other' to 'male' for processing
            if gender == 'other':
                gender = 'male'
            logger.debug(f'Normalized gender: {gender}')

            # Convert chest size from inches to float
            chest_size = float(chest_size_in) if chest_size_in else None
            waist_size = float(waist_size_in) if waist_size_in else None

            chest_size_cm_float = float(chest_size_cm) if chest_size_cm and chest_size_cm.strip() else None
            waist_size_cm_float = float(waist_size_cm) if waist_size_cm and waist_size_cm.strip() else None

            # Check for valid clothing type
            if clothing_type == 'top':
                # Suggest size based on chest size
                if chest_size is not None and chest_size > 0:
                    suggested_size = get_top_size_suggestion(gender, chest_size)
                
                if chest_size_cm_float is not None and chest_size_cm_float > 0:
                    # Convert cm to inches
                    chest_size_in_inches = round(chest_size_cm_float / 2.54)
                    suggested_size = suggested_size or get_top_size_suggestion(gender, chest_size_in_inches)

            elif clothing_type == 'bottom':
                # Suggest size based on waist size
                waist_size = float(waist_size_in) if waist_size_in else None
                waist_size_cm_float = float(waist_size_cm) if waist_size_cm and waist_size_cm.strip() else None
                
                if waist_size is not None and waist_size > 0:
                    suggested_size = get_bottom_size_suggestion(gender, waist_size)
                
                if waist_size_cm_float is not None and waist_size_cm_float > 0:
                    waist_size_in_inches = round(waist_size_cm_float / 2.54)
                    suggested_size = suggested_size or get_bottom_size_suggestion(gender, waist_size_in_inches)

            suggestion_display = suggested_size if suggested_size else 'N/A'

            # Prepare the output based on the input units
            height_output = f"{total_height_in_cm} cm" if height_cm.strip() else f"{height_feet} feet {height_inches} inches"

            chest_output = f"{chest_size_cm_float} cm" if chest_size_cm_float and chest_size_cm_float > 0 else f"{chest_size} inches"

            waist_output = f"{waist_size_cm_float} cm" if waist_size_cm_float and waist_size_cm_float > 0 else f"{waist_size} inches"

            context = {
                'gender': gender,
                'clothing_type': clothing_type,
                'suggestion': suggestion_display,
                'height_output': height_output,
                'chest_output': chest_output,
                'waist_output': waist_output,
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


def get_top_size_suggestion(gender, chest_size):
    if gender == 'male':
        suggestion = MaleTopSize.objects.filter(chest=chest_size).first()
    elif gender == 'female':
        suggestion = FemaleTopSize.objects.filter(chest=chest_size).first()
    else:
        suggestion = None

    return suggestion.size if suggestion else None

def get_bottom_size_suggestion(gender, waist_size):
    if gender == 'male':
        suggestion = MaleBottomSize.objects.filter(waist=waist_size).first()
    elif gender == 'female':
        suggestion = FemaleBottomSize.objects.filter(waist=waist_size).first()
    else:
        suggestion = None

    return suggestion.size if suggestion else None
