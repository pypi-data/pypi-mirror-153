""" spell checker bot based on Peter Norvig's spell checker """

from qary.etl.spell import make_spelling_corrections


class Skill:
    def reply(self, statement):
        r""" Chatbot "main" function to respond to a user command or statement

        >>> skill = Skill()
        >>> skill.reply('What is probabillity?')
        [(1.0, '\n Original: What is probabillity?\nCorrected: What is probability?')]
        >>> skill.reply('When was the telefone inventid?')
        [(1.0, '\n Original: When was the telefone inventid?\nCorrected: When was the telephone invented?')]
        >>> skill.reply('When was the telephone invented?')
        [(0.33, "I can't find any misspelled words.")]
        """
        corrected_statement = make_spelling_corrections(statement)
        confidence = 1.0 if corrected_statement.strip().lower() != statement.strip().lower() else 0.33
        if confidence == 1:
            return [(confidence, f"\n Original: {statement}\nCorrected: {corrected_statement}")]
        else:
            return [(confidence, f"I can't find any misspelled words.")]
