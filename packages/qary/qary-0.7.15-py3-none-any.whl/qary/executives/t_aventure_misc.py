""" notes

adventure = Adventure()


#  current state = [list, of, actions]
start = [adventure.cottage]
cottage = [adventure.hometown, adventure.back_to_full_health, adventure.check_stats]
hometown =  [adventure.cottage, adventure.forest, adventure.coast, adventure.check_stats]
forest =  [adventure.hometown, adventure.find_stones, adventure.battle, adventure.check_stats, adventure.forest]
battle = [adventure.forest, adventure.battle_injured, adventure.battle_injured]
coast = [adventure.hometown, adventure.fishconvo, adventure.find_stones, adventure.check_stats, adventure.coast]
fishconvo = [adventure.fishconvo_yes, adventure.fishconvo_no, adventure.coast, adventure.coast]


current_state_actions = {"start": [adventure.cottage],
                         "cottage": [adventure.hometown, adventure.back_to_full_health, adventure.check_stats],
                         "hometown": [adventure.cottage, adventure.forest, adventure.coast, adventure.check_stats],
                         "forest": [adventure.hometown, adventure.find_stones, adventure.battle, adventure.check_stats, adventure.forest],
                         "battle": [adventure.forest, adventure.battle_injured, adventure.battle_injured],
                         "coast": [adventure.hometown, adventure.fishconvo, adventure.find_stones, adventure.check_stats, adventure.coast],
                         "fishconvo": [adventure.fishconvo_yes, adventure.fishconvo_no, adventure.coast, adventure.coast]}


possible_actions = namedtuple("possible_actions", ["current_state", "condition", "action"])

data_table = [
        possible_actions(df['current_state'][0],
                   df['condition'][0] or None,
                   # getattr(adventure, df['action'][0], df['action'][0])),

        possible_actions(df['current_state'][1], df['condition'][1] or None, df['action'][0]),





# nested_dict = { 'dictA': {'key_1': 'value_1'},
#                 'dictB': {'key_2': 'value_2'}}


# current_state_actions = {"start": {'1': adventure.cottage},
#                          "cottage": {'1': adventure.hometown, '2': adventure.back_to_full_health, '9': adventure.check_stats,
#                          "hometown": [adventure.cottage, adventure.forest, adventure.coast, adventure.check_stats],
#                          "forest": [adventure.hometown, adventure.find_stones, adventure.battle, adventure.check_stats, adventure.forest],
#                          "battle": [adventure.forest, adventure.battle_injured, adventure.battle_injured],
#                          "coast": [adventure.hometown, adventure.fishconvo, adventure.find_stones, adventure.check_stats, adventure.coast],
#                          "fishconvo": [adventure.fishconvo_yes, adventure.fishconvo_no, adventure.coast, adventure.coast]}
"""
