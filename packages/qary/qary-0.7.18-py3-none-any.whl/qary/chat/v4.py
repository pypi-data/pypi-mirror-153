# qary.chat.v3
""" Load *.v3.dialog.yml files and execute recognize_intent() function:

  Inputs:
    lang (str): e.g. 'en', 'zh', 'es'
    state name (str): e.g. 'language-selected-english'
    user utterance (str): 'Hello chatobt'
  Outputs:
    id (str): state name
    text: bot utterance
"""
from collections import abc
import io
import logging
from pathlib import Path
from qary.init import maybe_download
import time
import yaml

import numpy as np
import pandas as pd

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

DEFAULT_LANG = 'en'
DEFAULT_LANG = 'en'
DIALOG_TREE_FILEPATH = maybe_download(filename=Path('chat/example-multilingual.v4.dialog.yml'))

# TODO see ISO_LANG codes in constants for nessvec or qary package
LANGS = {
    'en': 'en',
    'english': 'en',
    'es': 'es',
    'spanish': 'es',
    'zh': 'zh',
    'zho': 'zh',
    'chinese': 'zh',
    'chinese-simplified': 'zh',
    'zht': 'zht',
    'chinese-traditional': 'zht',
    'traditional chinese': 'zht',
    'traditional-chinese': 'zht',
}


def normalize_state_name(name):
    return str(name).strip().lower()


def normalize_user_text(text):
    return str(text).strip().lower()


def normalize_intent_texts(states):
    for name, state in states.items():
        for lang, intents in state.get('triggers', {}).items():
            if lang not in LANGS:
                continue
            try:
                states[name]['triggers'][lang].update({
                    normalize_user_text(i): v for (i, v) in intents.items()
                })
            except AttributeError as e:
                log.warning(e)
                log.warning(f"states[name]['triggers'][lang] = {states[name]['triggers'][lang]}")
    return states


def update_node_with_buttons(node, **context):
    """ Use lang in context dict to add button text to bot_text attribute of node """
    lang = context.get('lang', DEFAULT_LANG)
    log.debug(node)
    lang_buttons = node.get('buttons', {})
    node['actions_with_buttons'] = {}
    for lang, buttons in lang_buttons.items():
        if isinstance(buttons, str):
            buttons = [buttons]
        buttons = list(buttons)

        log.debug('=' * 80)
        log.debug(f'Updating bot_text for "{lang}" in node named "{node["name"]}" with {len(buttons)} buttons')
        bot_text = node['actions'].get(lang, '')
        for button_text in buttons:
            bot_text += f'\n  > {button_text}'
        log.debug(bot_text)
        log.debug('=' * 80)
        node['actions_with_buttons'][lang] = bot_text
    log.debug(node)
    return node


def update_state_list_with_buttons(states):
    log.warning(type(states))
    if isinstance(states, abc.Mapping):
        for state_name in states:
            states[state_name] = update_node_with_buttons(states[state_name])
    elif isinstance(states, (list, pd.Series)):
        for i, node in enumerate(states):
            states[i] = update_node_with_buttons(node)

    return states


def coerce_dialog_tree_series(states: (str, dict, Path, io.TextIOWrapper, pd.Series, list, np.ndarray, pd.Series)):
    """ Ensure that (yamlfilepath | list) -> dict -> Series """
    if isinstance(states, pd.Series):
        return states
    if isinstance(states, (str, Path)):
        with Path(states).open() as fin:
            states = yaml.full_load(fin)
    if isinstance(states, io.TextIOWrapper):
        states = yaml.full_load(states)
    if isinstance(states, abc.Mapping):
        return pd.Series(states)
    if isinstance(states, (list, np.ndarray)):
        states = pd.Series(
            states,
            index=[s.get('name', str(i)) for (i, s) in enumerate(states)])
        states.index.name = 'name'
        return states
    raise ValueError(f"Unable to coerce {type(states)} into pd.Series:\n  states={str(states)[:130]}...")


DIALOG_TREE = coerce_dialog_tree_series(states=DIALOG_TREE_FILEPATH)
DIALOG_TREE_DICT = {node['name']: node for node in DIALOG_TREE}


def preprocess_dialog_tree_series(states=DIALOG_TREE):
    """ Ensure that all dialog tree index values are normalized strs: Series.index.str.lower().str.strip()."""

    states = coerce_dialog_tree_series(states)
    states = update_state_list_with_buttons(states)
    states = normalize_intent_texts(states)

    # make sure state['name'] is used to overwrite the index
    states.index = [normalize_state_name(s.get('name', i)) for (i, s) in states.items()]
    states.index.name = 'name'

    is_dupe = states.index.duplicated()
    if sum(is_dupe) > 0:
        log.error(f'State pd.Series contains {sum(is_dupe)} duplicate index values!\n'
                  f'The following duplicates will be deleted:\n{states.index[is_dupe].to_series()}'
                  )
    states = pd.Series(states[~is_dupe])
    states_list = []
    for i, (idx, s) in enumerate(states.items()):
        s = dict(s)
        s['name'] = str(idx)
        s['iloc'] = i
        states_list.append((idx, s))
        # states_list.append(i, s)
    return pd.Series(dict(states_list))


# this is the canonical dialog v3 data structure:
DIALOG_TREE_SERIES = coerce_dialog_tree_series(DIALOG_TREE_FILEPATH)


def await_timeout(seconds=0, milliseconds=0):
    time.sleep(seconds + milliseconds / 1000.0)


def next_state_context(states=DIALOG_TREE_SERIES, state_name=None, user_text='', **context):
    r""" Recognize desired state transition trigger and return next_state name

      Inputs:
        lang (str): e.g. 'en', 'zh', 'es'
        state name (str): e.g. 'language-selected-english'
        user utterance (str): 'Hello chatobt'
      Outputs:
        name (str): state name
        text: bot utterance

    >>> next_state_context(state_name='is-this-your-first-time', user_text='yes')
    {'lang': 'en',
     'state_name': 'is-this-your-first-yes',
     'bot_text': 'Which of the following do you represent?\n'}
    """

    context['lang'] = context.get('lang', DEFAULT_LANG)

    state_name = states[0]['name'] if state_name is None else state_name
    # default_response = dict(
    #     state_name=states[0]['name'],
    #     bot_text=states[0].get('actions', {}).get(lang, states[0].get('en', '')),
    #     lang=lang)
    if state_name is None:
        return None
    # if str(state_name).lower().strip() in ('__start__', '__welcome__'):
    #     return default_response
    log.debug('\n' + str(states))

    # detect intent from text message
    try:
        node = states[state_name]
    except KeyError as e:
        log.error(e)
        log.error(f"Invalid state_name '{state_name}'. It is not among states.index:\n  {states.index}")

    if state_name != node['name']:
        log.debug(f' states[name]:{node.get("name")} != {state_name}:state_name')

    triggers = node.get('triggers', {})
    log.debug(f'    triggers for node name {node["name"]}:\n{triggers}')

    user_intents = triggers.get(context['lang'], triggers.get(DEFAULT_LANG, {}))  # fallback to English
    log.debug(f"    Triggers for node name {state_name} and lang {context['lang']}:\n{triggers}")

    buttons = node.get('buttons', {})
    buttons = buttons.get(context['lang'], buttons.get('en', {}))  # fallback to English
    log.debug(f"    Buttons for node name {state_name} and lang {context['lang']}:\n{buttons}")

    # want to check both button text values and user_intent text values
    buttons.update(user_intents)

    if user_text in buttons:
        new_state_name = buttons[user_text]
        if new_state_name:
            context['state_name'] = new_state_name
            context['bot_text'] = states[new_state_name].get('actions', {}).get(context['lang'], '')
    else:
        timeout = triggers.get('timeout')
        if isinstance(timeout, list):
            log.debug(f"Awaiting timeout {timeout}")
            await_timeout(seconds=timeout[0])
            new_state_name = timeout[1]
            context['state_name'] = new_state_name
            context['bot_text'] = states[new_state_name].get('actions', {}).get(context['lang'], '')
        elif isinstance(timeout, (float, int)):
            await_timeout(timeout)
    if list(context.keys()) == ['lang']:
        log.error(f"Intent {user_text} not found in state {node['name']}!")
    return context


class Engine:  # Engine(pd.Series)
    """ A state machine designed for managing the dialog for a rule-based chatbot """

    def __init__(self, states=DIALOG_TREE_SERIES, **context):
        self.hist = []
        self.context = {}
        self.states = preprocess_dialog_tree_series(states)

        self.hist_append_context()  # '__init__.enter')
        self.update_context(context)

        state_name = self.context.get('state_name') or self.states.index[0]
        self.set_state_name(state_name)

        lang = self.context.get('lang') or DEFAULT_LANG
        self.set_lang(lang)

        # Unused side-effect
        actions = self.states[state_name]['actions']
        actions_with_buttons = self.states[state_name]['actions_with_buttons']
        self.bot_text_with_buttons = actions_with_buttons.get(lang, actions[lang])

    def set_state_name(self, state_name):
        """ Skip to arbitrary state_name. """
        state_name = normalize_state_name(state_name)
        if state_name is None or state_name not in self.states.index:
            log.warning(f"New state_name {state_name} not found in states.index")
            state_name = self.states.index[0]
        self.context['state_name'] = state_name  # self.default_states = {None: self.states.index[0]}
        log.info(f"Setting state_name={self.context['state_name']}")
        return state_name

    def set_lang(self, lang):
        lang = self.context.get('lang') if lang is None else DEFAULT_LANG
        lang = LANGS.get(lang)
        lang = DEFAULT_LANG if not lang else lang
        self.context['lang'] = lang
        return lang

    def update_context(self, context_changes):
        """ Update self.context with context_changes dict """
        # self.context['context_changes'] = context_changes
        self.context.update(context_changes)
        return self.context

    def normalize_user_text(self, user_text):
        if isinstance(user_text, str):
            return user_text.lower().strip()
        return user_text

    def do_user_intent(self, **context):
        self.update_context(context)
        user_text = self.context.get('user_text')
        state_name = self.context.get('state_name')
        node = self.states[state_name]
        triggers = node['triggers']
        lang = self.context.get('lang', DEFAULT_LANG)
        intents = triggers[lang]
        user_intent_text = self.normalize_user_text(user_text)
        self.set_state_name(intents[user_intent_text])
        return self.context

    def hist_append_context(self, substate=None):
        """ Append self.context to a running log of the context variable

        TODO: record only the diff/patch (`context_updates`) with `replay_context_updates()` method
        """
        if substate is not None:
            self.context['substate'] = substate
        self.hist.append(self.context)
        return self.context

    def run(self, **context_changes):
        """ Move to next state based on user action/text

        Inputs:
          user_text (str): whatever message user typed for the current state_name
          state_name (str): skip the current state and go to state_name before processing user_text
          lang (str): en, zh, zht, es, etc

        Returns dict(
          name="name-of-new-state",
          bot_text="Whatever the bot should say in response to this user action or message.",
          lang="en"|"es"|"zh"|... ,
          )
        """
        self.context = self.update_context(context_changes)  # default_lang, default_state_name
        self.hist_append_context()  # '__init__.after_update_context')
        self.update_context(context_changes)
        self.hist.append(self.context)
        self.set_state_name(self.get_next_state_name())
        return self.context

    def execute_actions(self, actions):
        if actions is None:
            return
        if 'update_context' in actions:
            self.update_context(actions['update_context'])
        if self.context['lang'] in actions:
            self.update_context(dict(bot_text=actions[self.context['lang']]))
        return self.context

    def update_intent_triggers_with_buttons(self):
        node = self.states[self.context['state_name']]
        triggers = node['triggers']
        buttons = node.get('buttons', {})
        user_intents = triggers.get(
            self.context['lang'], triggers.get(DEFAULT_LANG, {}))  # fallback to English
        log.debug(f"    Triggers for node name {self.context['state_name']} and lang {self.context['lang']}:\n{user_intents}")

        # TODO?: copy.deepcopy(buttons)
        buttons = buttons.get(self.context['lang'], buttons.get('en', {}))  # fallback to English

        # want to check both button text values and user_intent text values
        buttons.update(user_intents)
        buttons_and_intents = buttons
        log.debug(f"    Buttons and intents for node name {self.context['state_name']} and lang {self.context['lang']}:\n{buttons_and_intents}")
        return buttons_and_intents

    def detect_triggers(self):
        node = self.states[self.context['state_name']]
        triggers = node['triggers']
        state_name = self.context['state_name']
        log.debug(f"    triggers for node name {state_name}:\n{triggers}")
        context = self.context

        user_text = context.get('user_text')
        new_state_name = None

        buttons_and_intents = self.update_intent_triggers_with_buttons()

        log.warning(buttons_and_intents.keys())
        user_text = context.get('user_text', '')
        if user_text in buttons_and_intents:
            state_name = self.set_state_name(buttons_and_intents[user_text])
            node = self.states[state_name]
            self.execute_actions(node.get('actions'))
        if 'timeout' in triggers:
            if new_state_name:
                log.error('Undefined behavior when both timeout and user_text (intent) trigger a state change')
            timeout = triggers['timeout']
            if isinstance(timeout, dict):
                log.debug(f"Awaiting timeout {timeout}")
                timeout = list(list(timeout.items())[0])
            if isinstance(timeout, (list, tuple)):
                await_timeout(seconds=timeout[0])
                new_state_name = timeout[1]
                context['state_name'] = new_state_name
                context['bot_text'] = self.states[new_state_name].get('actions', {}).get(context['lang'], '')
            # FIXME: this seems useless and an anti-pattern:
            elif isinstance(timeout, (float, int)):
                await_timeout(timeout)
        if new_state_name is None:
            log.warning(f"No state change was triggered by user_text {user_text} for state_name {node['name']}!")
            new_state_name = context.get('state_name')
            log.warning(f"    Remaining in state_name {new_state_name}!")
        self.context = context
        return new_state_name

    def get_next_state_name(self):
        r""" Recognize desired state transition trigger and return next_state name

          Inputs:
            lang (str): e.g. 'en', 'zh', 'es'
            state name (str): e.g. 'language-selected-english'
            user utterance (str): 'Hello chatobt'
          Outputs:
            name (str): state name
            text: bot utterance

        >>> eng = Engine()

        FIXME:
        >> eng.get_next_state_name()
        'selected-language-welcome'
        """
        state_name = self.context['state_name']
        log.warning(f"Trying to find next state after {state_name}")
        # default_response = dict(
        #     state_name=states[0]['name'],
        #     bot_text=states[0].get('actions', {}).get(lang, states[0].get('en', '')),
        #     lang=lang)
        if state_name is None:
            return None
        # if str(state_name).lower().strip() in ('__start__', '__welcome__'):
        #     return default_response
        log.debug('\n' + str(self.states))

        try:
            node = self.states[state_name]
        except KeyError as e:
            log.error(e)
            log.error(f"Invalid state_name '{state_name}'. It is not among states.index:\n  {self.states.index}")

        if state_name != node['name']:
            log.debug(f' states[name]:{node.get("name")} != {state_name}:state_name')

        # detect intent from user text message
        new_state_name = self.detect_triggers()

        return new_state_name


"""
>>> from qary.chat.v3 import *
>>> e = Engine()
>>> e.run('English')
{'lang': 'en',
 'state_name': 'selected-english',
 'bot_text': 'Hello, my name is POLY - short for Polyglot, which means I can speak many languages!'
             '\n\nPlease select which language you would like me to help you in:\n'}
>>> e.state_name
'selected-english'
>>> e.states[e.state_name]
{'name': 'selected-english',
 'level': 1,
 'actions': {'update_context': {'lang': 'en'}},
 'triggers': {'timeout': {0: 'selected-language-welcome'}},
 'actions_with_buttons': {},
 'iloc': 2}
"""
