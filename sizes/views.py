from django.shortcuts import render
from .models import MaleTopSize, MaleBottomSize, FemaleTopSize, FemaleBottomSize
import logging

logger = logging.getLogger(__name__)

def chest_size_view(request):
    maleBottomSize = MaleBottomSize.objects.all().values()
    femaleBottomSize = FemaleBottomSize.objects.all().values()

    if request.method == 'POST':
        logger.debug(f"Request data: {request.POST}")

        try:
            # Retrieve POST data
            gender = request.POST.get('gender', '')
            clothing_type = request.POST.get('clothing_type', '')
            fit_preference = request.POST.get('fit_preference', 'avg')
            height_feet = request.POST.get('height_feet', '0')
            height_inches = request.POST.get('height_inches', '0')
            height_cm = request.POST.get('height_cm', '0')
            chest_size_in = request.POST.get('chest_size', '0')
            waist_size_in = request.POST.get('waist_size_in', '0')
            chest_size_cm = request.POST.get('chest_size_cm', '0')
            waist_size_cm = request.POST.get('waist_size_cm', '0')

            # Determine if height is in cm or inches and convert accordingly
            total_height = 0
            input_in_cm = False
            if height_cm and height_cm.strip():
                total_height = round(float(height_cm))
                input_in_cm = True
            else:
                height_feet = int(height_feet) if height_feet.strip() else 0
                height_inches = int(height_inches) if height_inches.strip() else 0
                total_height = (height_feet * 12) + height_inches

            # Log the total height
            total_height_in_cm = round(total_height * 2.54) if not input_in_cm else total_height
            logger.debug(f'Total height in cm: {total_height_in_cm}')

            # Suggested pants length based on height input
            suggested_length = get_bottom_length_suggestion(total_height, input_in_cm)

            # Process clothing type and fit preference for sizing
            def adjust_size_for_fit(size, fit_preference):
                # Adjust based on fit preference
                if fit_preference == 'slim':
                    size -= 2
                elif fit_preference == 'loose':
                    size += 2
                # Round up to the nearest even number if the size is odd
                return size + 1 if size % 2 != 0 else size

            suggested_size = None
            if gender == 'other':
                gender = 'male'
            logger.debug(f'Normalized gender: {gender}')

            # Convert sizes to floats
            chest_size = float(chest_size_in) if chest_size_in else None
            waist_size = float(waist_size_in) if waist_size_in else None
            chest_size_cm_float = float(chest_size_cm) if chest_size_cm and chest_size_cm.strip() else None
            waist_size_cm_float = float(waist_size_cm) if waist_size_cm and waist_size_cm.strip() else None

            if clothing_type == 'top':
                if chest_size is not None and chest_size > 0:
                    chest_size_adjusted = adjust_size_for_fit(chest_size, fit_preference)
                    suggested_size = get_top_size_suggestion(gender, chest_size_adjusted)

                if chest_size_cm_float is not None and chest_size_cm_float > 0:
                    chest_size_in_inches = round(chest_size_cm_float / 2.54)
                    chest_size_adjusted_in = adjust_size_for_fit(chest_size_in_inches, fit_preference)
                    suggested_size = suggested_size or get_top_size_suggestion(gender, chest_size_adjusted_in)

            elif clothing_type == 'bottom':
                if waist_size is not None and waist_size > 0:
                    waist_size_adjusted = adjust_size_for_fit(waist_size, fit_preference)
                    suggested_size = get_bottom_size_suggestion(gender, waist_size_adjusted)

                if waist_size_cm_float is not None and waist_size_cm_float > 0:
                    waist_size_in_inches = round(waist_size_cm_float / 2.54)
                    waist_size_adjusted_in = adjust_size_for_fit(waist_size_in_inches, fit_preference)
                    suggested_size = suggested_size or get_bottom_size_suggestion(gender, waist_size_adjusted_in)

            # Prepare outputs
            suggestion_display = suggested_size if suggested_size else 'N/A'
            height_output = f"{total_height_in_cm} cm" if input_in_cm else f"{height_feet} feet {height_inches} inches"
            chest_output = f"{int(chest_size_cm_float)} cm" if chest_size_cm_float and chest_size_cm_float > 0 else (f"{int(chest_size)} inches" if chest_size and chest_size > 0 else 'N/A')
            waist_output = f"{int(waist_size_cm_float)} cm" if waist_size_cm_float and waist_size_cm_float > 0 else (f"{int(waist_size)} inches" if waist_size and waist_size > 0 else 'N/A')

            context = {
                'gender': gender,
                'clothing_type': clothing_type,
                'suggestion': suggestion_display,
                'height_output': height_output,
                'chest_output': chest_output,
                'waist_output': waist_output,
                'suggested_length': f"{suggested_length} cm" if input_in_cm else f"{suggested_length} inches"
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
        size_queryset = MaleTopSize.objects.filter(chest__gte=chest_size - 1, chest__lte=chest_size + 1)
    elif gender == 'female':
        size_queryset = FemaleTopSize.objects.filter(chest__gte=chest_size - 1, chest__lte=chest_size + 1)
    else:
        size_queryset = None

    if size_queryset:
        closest_match = min(size_queryset, key=lambda x: abs(x.chest - chest_size))
        return closest_match.size if closest_match else None
    return None

def get_bottom_size_suggestion(gender, waist_size):
    if gender == 'male':
        size_queryset = MaleBottomSize.objects.filter(waist__gte=waist_size - 1, waist__lte=waist_size + 1)
    elif gender == 'female':
        size_queryset = FemaleBottomSize.objects.filter(waist__gte=waist_size - 1, waist__lte=waist_size + 1)
    else:
        size_queryset = None

    if size_queryset:
        closest_match = min(size_queryset, key=lambda x: abs(x.waist - waist_size))
        return closest_match.size if closest_match else None
    return None

def get_bottom_length_suggestion(total_height, input_in_cm=True):
    # Define height ranges with corresponding length estimates
    if input_in_cm:  # User entered height in cm, so we return length in cm
        if total_height < 160:
            return 96.5  # 38 inches in cm
        elif 160 <= total_height < 170:
            return 101.6  # 40 inches in cm
        elif 170 <= total_height < 180:
            return 106.7  # 42 inches in cm
        elif 180 <= total_height < 190:
            return 109.2  # 43 inches in cm
        else:
            return 111.8  # 44 inches in cm
    else:  # User entered height in ft/inches, so we return length in inches
        if total_height < 63:  # equivalent to 160 cm
            return 38
        elif 63 <= total_height < 67:  # equivalent to 160-170 cm
            return 40
        elif 67 <= total_height < 71:  # equivalent to 170-180 cm
            return 42
        elif 71 <= total_height < 75:  # equivalent to 180-190 cm
            return 43
        else:
            return 44