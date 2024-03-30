from django.http import JsonResponse
from django.views import View
from .models import GameState

class ValidateStringView(View):
    def post(self, request, *args, **kwargs):
       
        input_string = request.POST.get('input_string')

     
        game_state = GameState.objects.last()

        
        is_valid = validate_input_string(input_string, game_state.correct_answer)

        
        response_data = {
            'is_valid': is_valid,
            'game_won': check_game_won(is_valid),
        }

        return JsonResponse(response_data)

def validate_input_string(input_string, correct_answer):
    """
    Validates the user's input string against the correct answer.

    Args:
        input_string (str): The user's input string.
        correct_answer (str): The correct answer for the game.

    Returns:
        bool: True if the input string matches the correct answer, False otherwise.
    """
    
    return input_string == correct_answer

def check_game_won(is_valid):
    """
    Determines if the game has been won based on the validity of the user's input string.

    Args:
        is_valid (bool): Whether the user's input string is valid.

    Returns:
        bool: True if the game has been won (input string is valid), False otherwise.
    """
    return is_valid
