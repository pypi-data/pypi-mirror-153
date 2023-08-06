""" A text adventure game that uses a FSM data structure to scale

Based on Aaron's Text Adventure that he used to learn Python.

https://codereview.stackexchange.com/questions/155661/text-adventure-game
"""
from pathlib import Path
import yaml
from collections import namedtuple
from textwrap import dedent

import pandas as pd

DATA_DIR = Path('~/code/tangibleai/qary/qary/data/').expanduser()
if not DATA_DIR.is_dir():
    from qary.config import DATA_DIR

Transition = namedtuple("Transition", ["start_state", "end_state", "condition", "action"])


class Executive:
    pass


class Adventure(Executive):
    def __init__(self, **kwargs):
        # TODO 1 (done): load state transitions here rather than in main()

        self.msg = yaml.safe_load(open(Path(DATA_DIR, 'factquest', 'default-text-adventure-messages.yml')))
        self._curr_state = None
        self._transitions = {}
        df = read_adventure_yml()
        transition_table = [Transition(
            row['start_state'],
            row['end_state'],
            row['condition'] or None,
            getattr(self, row['action'])) for (i, row) in df.iterrows()]
        self.setup(transition_table)

        state = dict(
            gold=2, health=10, energy=10, melee=1, ranged=0, ammo=0, full_health=10, attack_num=0)
        state.update(kwargs)
        for k, v in state.items():
            setattr(self, k, v)

    def setup(self, transitions):
        for transition in transitions:
            self._transitions[(transition.start_state, transition.condition)] = transition
        self._curr_state = transitions[0].start_state

    def trigger(self, command):
        if command:
            command = command.lower()
        can_continue = True
        print(f'current state name: {self._curr_state}')
        for key in self._transitions:
            if key[0] == self._curr_state:
                if key[1] != None and command in key[1].lower().split("|"):
                    command = key[1]
        key = self._curr_state, command
        if key not in self._transitions:
            print("Unknown command '{}' in current state '{}'".format(command, self._curr_state))
            return can_continue
        while key in self._transitions:
            transition = self._transitions[key]
            can_continue = transition.action()
            self._curr_state = transition.end_state
            key = self._curr_state, None
        return can_continue

    def run(self):
        can_continue = self.trigger(None)
        while can_continue:
            command = input(self.msg['all']['prompt'])
            if command.lower() == 'q':
                print(self.msg['all']['command__eq_q'])
                return
            can_continue = self.trigger(command)

    def start(self):
        print(dedent(self.msg['start']))
        return True

    def check_stats(self):
        msg = dedent("""\
        ********

        Gold:   {gold}
        Health: {health}/{full_health}
        Melee:  {melee}
        Energy: {energy}
        """)
        if self.ranged:
            msg += dedent("""\
            Ranged: {ranged}
            Ammo:   {ammo}
            """)
        msg = msg.format(gold=self.gold,
                         health=self.health,
                         full_health=self.full_health,
                         melee=self.melee,
                         energy=self.energy,
                         ranged=self.ranged,
                         ammo=self.ammo)
        print(msg)
        return True

    def location(self):
        print(dedent(self.msg[self._]['description']))
        return True

    def cottage(self):
        print(dedent(self.msg['cottage']['description']))
        return True

    def back_to_full_health(self):
        self.health = self.full_health
        print(dedent(self.msg['back_to_full_health']))
        return True

    def hometown(self):
        print(dedent(self.msg['hometown']['description']))
        return True

    def forest(self):
        print(dedent(self.msg['forest']['root']['description']))
        if self.attack_num == 0:
            print(dedent(self.msg['forest']['attack_num__gt_0']))
            self.attack_num += 1
            self.health -= 1
            if self.health < 0:
                print(self.msg['forest']['end'])
                return False
        print(dedent(self.msg['forest']['menu']))
        return True

    def coast(self):
        print(dedent(self.msg['coast']['description']))
        return True

    def find_stones(self):
        if self.ranged == 0:
            print(dedent(self.msg['find_stones']['ranged__eq_0']))
            self.ranged = 1
            self.ammo = 5
            return True

        elif self.ranged >= 1 and self.ammo < 5:
            print(dedent(self.msg['find_stones']['ranged__ge_1__and__ammo_lt_5']))
            self.ammo = 5
            return True

        elif self.ranged >= 1 and self.ammo > 4:
            print(dedent(self.msg['find_stones']['ranged__ge_1__and__ammo_gt_4']))
            return True

    def battle(self):
        # TODO 2 (DONE): move to yml
        print(dedent(self.msg['battle']))
        return True

    def battle_injured(self):
        # TODO 2 (DONE): move to yml
        print(dedent(self.msg['battle_injured']))
        return False

    def fishconvo(self):
        # TODO 2 (DONE): move to yml
        print(dedent(self.msg['fishconvo']))
        return True

    def fishconvo_yes(self):
        # TODO 3(DONE): use nested dict in messages.yml
        if self.melee == 1:
            print(dedent(self.msg['fishconvo_yes']['melee__eq_1']))
            self.melee += 1
        else:
            print(dedent(self.msg['fishconvo_yes']['melee__gt_1']))
        return True

    def fishconvo_no(self):
        # TODO 3 (DONE): use nested dict in messages.yml
        if self.melee == 1:
            print(dedent(self.msg['fishconvo_no']['melee__eq_1']))
            self.melee += 1
        else:
            print(dedent(self.msg['fishconvo_no']['melee__gt_1']))
        return True


# def read_adventure_csv(filepath=Path(DATA_DIR, 'factquest', 'default-text-adventure.csv')):
#     df = pd.read_csv(filepath)
#     conditions = []
#     for c in df['condition']:
#         if c:
#             try:
#                 conditions.append(str(int(c)))
#             except (TypeError, ValueError):
#                 conditions.append(c or None)
#         else:
#             conditions.append(None)
#     df['condition'] = conditions
#     df = df.fillna("")
#     return df

def read_adventure_yml(filepath=Path(DATA_DIR, 'factquest', 'default-text-adventure.yml')):
    with open(filepath) as data:
        df = pd.DataFrame(yaml.safe_load(data))
    conditions = []
    for c in df['condition']:
        if c:
            try:
                conditions.append(str(int(c)))
            except (TypeError, ValueError):
                conditions.append(c or None)
        else:
            conditions.append(None)
    df['condition'] = conditions
    df = df.fillna("")
    return df

def main():
    # TODO 5: DRY data in yml file for 1st 4 simpler rooms
    # TODO 5a (done): nested dict for 'menu' and 'description' separately in py and yml
    # TODO 5b: one fun for 1st 4 rooms, no nested dicts
    # TODO 5c: use varable name to dicide what to do (conditional expression)
    # TODO 6: (done) convert csv to yml
    # TODO 6a: 2 files
    # TODO 6b: combine yml files: messages.yml inside adventure.yml with messages: and transitions: keys

    adventure = Adventure()
    adventure.run()


if __name__ == '__main__':
    main()
