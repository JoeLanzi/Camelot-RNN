from action import action

def set_character_position(character_name, target_position):
    action('SetPosition(' + character_name  + ',' + target_position + ')')


def set_item_position(item_name, item_type, target_position, effect=None):
    action('CreateItem(' + item_name + ',' + item_type +')')
    action('SetPosition(' + item_name  + ',' + target_position + ')')
    if effect is not None:
        action('EnableEffect(' + item_name + ',' + effect + ')')