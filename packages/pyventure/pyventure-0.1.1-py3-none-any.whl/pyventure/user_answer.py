from .message import msg

def get_answer_confirm():
    while True:
        answer = input('> ')
        confirmation = input(f'Are you happy with "{answer}"?: ')
        if confirmation == 'yes':
            return answer
        else:
            msg.orange('Okay, try again.')
            continue

def get_answer_no_confirm(valid_responses: tuple[str]):
    while True:
        answer = input('> ')
        if answer.lower() == 'help':
            msg.help_text()
            continue
        if answer in valid_responses:
            return answer
        else:
            msg.plain(f"That wasn't one of the following valid responses: {valid_responses}")