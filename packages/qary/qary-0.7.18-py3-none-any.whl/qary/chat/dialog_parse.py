"""
   Class for parsing simple text files with transcripts of dialogs

    See docstring of class DialogTurns below

    Examples:
        See the doctests for the class DialogTurns as well as the pytests for this file in
        `tests/test_dialog_parse.py`

"""
import json
from pathlib import Path
import re

import pandas as pd
import yaml


class DialogTurns:
    r"""Class for parsing simple text files with transcripts of dialogs

    The format of the dialog text is  similar to- `Bot: Welcome\nPlayer: Thanks` and put it in a
    list of dictionaries. This may then be converted to multiple formats liks json, yaml,
    csv etc. The FSM state that a turn belongs to may be specified using a # comment prefix
    similar to:  `state: welcome` Other comments which could be embedded in the text file are
    currently ignored.

    Examples:
        >>> import os
        >>> input_turns = ['#state:welcome', 'Bot: Hi', '#state:play', '#player:how many cats']
        >>> outfile = open('./dialog.txt', 'w')
        >>> _ = outfile.write('\n'.join(input_turns)) # doctest:+ELLIPSIS
        >>> outfile.close()
        >>> dlg = DialogTurns('./dialog.txt')
        >>> dlg.parse_dialog_lines()
         [{'state': 'welcome', 'player': [], 'bot': ['Hi']}]
        >>> dlg.convert_turns_format(turns_format='csv', ) #doctest:+ELLIPSIS
         "state,player,bot..."
        >>> os.remove('./dialog.txt')

    TODO:
        * This class will eventually have the ability to parse meta information beyond just
            states. However at the moment only state information is parsed.

    """

    REGEX_STMT = r'(?P<speaker>([Bb]ot)|([Pp]layer)):\s*(?P<statement>.*)'
    REGEX_META = r'(\s*)(?P<meta_name>\w+)\s*:\s*(?P<meta_val>.*)\s*'

    def __init__(self, dialog_file, sticky_state=True):
        """Initialize a DialogTurns object

        Args:
            dialog_file: text file where the dialog may be found. pass None if a set of input
                lines will be fed to the parse method
            sticky_state: If the last meta (state) information should be carried over to new
                turns till a new meta information line is encountered (default: True)

        """
        self._dialog_file = dialog_file
        self.turns = []
        self._dialog_lines = None
        self.sticky_state = sticky_state
        # self.last_state = None
        return

    def _read_dialog_file(self, filepath=None):
        """Reads a text file  and returns a list of lines

        Empty lines are removed along with any end of line characters for each line

        Args:
            filepath: text file where the dialog if stored

        Returns:
            list:  list of lines (strings)
        """
        filepath = filepath or self._dialog_file
        with open(filepath) as infile:
            inlines = infile.readlines()
        inlines = [inline.strip() for inline in inlines if inline.strip()]
        self._dialog_lines = inlines
        return inlines

    def _parse_comment_line(self, line):
        """Extracts any embedded meta information like an FSM state from the comment line.

        Both the meta name and value are extracted from the comment.

        Args:
            line: input string to extract comments from

        Returns:
            dict: dictionary of meta information (Empty if none)
        """
        meta_dict = {}
        if not line.lstrip().startswith('#'):
            return meta_dict
        line = line.lstrip('# \t')
        match = re.search(self.REGEX_META, line)
        if match:
            name = match.group('meta_name')
            val = match.group('meta_val')
            meta_dict[name] = val
        return meta_dict

    def _extract_state(self, line):
        """Convenience function to just return the 'state' key in a meta_dict.

        Since only states are supported at the moment, only that part of a meta dict need to be
        used

        Args:
            line: line starting with '#' from which state should be extracted

        Returns:
             Dict of extracted state, such as {'state': 'welcome'}
              If line was not a comment or no state was present, an empty dict is returned.

        TODO:
            Reevaluate the returned object and see if it makes sense to return something simpler
            since only the state is returned. Is there need for a dict?
        """
        meta_dict = self._parse_comment_line(line)
        return meta_dict.get('state', None)

    def parse_dialog_lines(self, dialog_lines=None):
        """Parse lines from a standard dialog type text file

        Returns a list of dictionaries, each dictionary containing conversation for one turn

        Args:
            dialog_lines: optional list of lines of text to be parsed for turns. If not supplied,
            the method will try to get the value of the property _dialog_lines. If that is also
            empty, the dialog file will be opened and lines of text read from that

        Returns:
            object: list of dictionaries, each with state and text spoken by the bot or the player

        """
        if not dialog_lines and not self._dialog_lines:
            self._read_dialog_file()
        dlg_lines = dialog_lines or self._dialog_lines
        turns = []  # list of all turns
        turn = {'state': None, 'player': [], 'bot': []}  # individual turn
        last_spkr = 'player'  # the first turn contains only bot statements
        new_state = None
        for i, line in enumerate(dlg_lines):
            if line.lstrip().startswith('#'):
                state = self._extract_state(line)
                if state:  # if something other than a state, disregard
                    new_state = state
                    # the very first turn is created outside of this loop and thus the state is
                    # unassigned; Later turns have state initialized further down. So if the very
                    # first non comment line encountered is a state, we need to initialize that
                    # state of the turn
                    if not turns and (not turn['player']) and (not turn['bot']):
                        turn['state'] = new_state
                        if not self.sticky_state:
                            new_state = None
                continue
            else:
                match = re.search(self.REGEX_STMT, line)
            if match:
                spkr = match.group('speaker').lower()
                statement = match.group('statement')
                if spkr == 'player':
                    if last_spkr == 'bot':
                        turns.append(turn)
                        turn = {'state': new_state, 'player': [], 'bot': []}  # individual turn
                        # if state is not sticky, the next turn should have its state reset to None
                        if not self.sticky_state:
                            new_state = None
                    if statement:
                        turn['player'].append(statement)
                    last_spkr = 'player'
                elif spkr == 'bot':
                    if statement:
                        turn['bot'].append(statement)
                    last_spkr = 'bot'
        if turn['player'] or turn['bot']:  # situation where the last turn was never added to turns
            turns.append(turn)
        self.turns = turns
        return turns

    @staticmethod
    def _get_formatted_data(
        turns,
        turns_format=None,
    ):
        """Returns the turns in the specified format

        This is considered a private method and should Typically be called from the
        convert_turns_format() method.

        Args:
            turns: list of dictionaries with turns
            turns_format: string corresponding to desired format - json, yaml or csv(default)

        Returns:
            string: formatted string corresponding to the specified format
        """
        data = turns  # for default turns_format of list
        if turns_format == 'json':
            data = json.dumps(turns)
        elif turns_format == 'yaml':
            data = yaml.dump(turns)
        else:  # default : 'csv'
            df = pd.DataFrame(turns)
            data = df.to_csv(index=False)
        return data

    def convert_turns_format(self, turns_format=None, save_filepath=None, turns=None):
        """Converts the format of the dialog data structure to a specfied format

        And optionally saves it to a specified file. This is the public method which is called to
        convert to other formats

        Args:
            turns_format: string corresponding to desired format - json, yaml or csv(default)
                save_filepath: Optional file to save it to. If data_format is omitted and this is
                specified, the file extension is used to determine the format. If both are omitted,
                a csv format is returned
            turns: Optional list of dictionaries (useful for unit testing). Defaults to the
                object properaty turns which may already have been constructed

        Returns:
            string: formatted string corresponding to the specified format
        """
        file_ext = None
        turns = turns or self.turns
        if save_filepath:
            save_filepath = Path(save_filepath)
            file_ext = save_filepath.suffix.lstrip('.')
        if (not turns_format) and file_ext:
            if file_ext == 'json':
                turns_format = 'json'
            elif file_ext in ['yaml', 'yml']:
                turns_format = 'yaml'
            else:
                turns_format = 'csv'
        turns = self._get_formatted_data(turns, turns_format=turns_format)
        if save_filepath:
            with open(save_filepath, 'w') as outfile:
                outfile.writelines(turns)
        return turns


if __name__ == '__main__':
    # TODO:
    pass
