from modules import objects

def start_game(game_state):
    """
    Start the game
    """
    print("You wake up on a couch and find yourself in a strange house with no windows which you have never been to before. You don't remember why you are here and what had happened before. You feel some unknown danger is approaching and you must get out of the house, NOW!")
    play_room(game_state["current_room"], game_state)

def play_room(room, game_state):
    """
    Play a room. First check if the room being played is the target room.
    If it is, the game will end with success. Otherwise, let player either
    explore (list all items in this room) or examine an item found here.
    """
    game_state["current_room"] = room
    if(game_state["current_room"] == game_state["target_room"]):
        print("Congrats! You escaped the room!")
    else:
        print("You are now in " + room["name"])
        intended_action = input("What would you like to do? Type 'explore' or 'examine'?").strip()
        if intended_action == "explore":
            explore_room(room)
            play_room(room, game_state)
        elif intended_action == "examine":
            examine_item(input("What would you like to examine?").strip(), game_state)
        else:
            print("Not sure what you mean. Type 'explore' or 'examine'.")
            play_room(room, game_state)
        linebreak()

def explore_room(room):
    """
    Explore a room. List all items belonging to this room.
    """
    items = [i["name"] for i in objects.object_relations[room["name"]]]
    print("You explore the room. This is " + room["name"] + ". You find " + ", ".join(items))

def get_next_room_of_door(door, current_room):
    """
    From object_relations, find the two rooms connected to the given door.
    Return the room that is not the current_room.
    """
    connected_rooms = objects.object_relations[door["name"]]
    for room in connected_rooms:
        if(not current_room == room):
            return room

def examine_item(item_name, game_state):
    """
    Examine an item which can be a door or furniture.
    First make sure the intended item belongs to the current room.
    Then check if the item is a door. Tell player if key hasn't been
    collected yet. Otherwise ask player if they want to go to the next
    room. If the item is not a door, then check if it contains keys.
    Collect the key if found and update the game state. At the end,
    play either the current or the next room depending on the game state
    to keep playing.
    """
    current_room = game_state["current_room"]
    next_room = ""
    output = None

    for item in objects.object_relations[current_room["name"]]:
        if(item["name"] == item_name):
            output = "You examine " + item_name + ". "
            if(item["type"] == "door"):
                unlock_door(game_state, item, current_room, next_room, output, get_next_room_of_door, play_room)
                # print("check point after unlock door")
            else:
                if(item["name"] in objects.object_relations and len(objects.object_relations[item["name"]])>0):
                    item_found = objects.object_relations[item["name"]].pop()
                    game_state["keys_collected"].append(item_found)
                    output += "You find " + item_found["name"] + "."
                else:
                    output += "There isn't anything interesting about it."
            print(output)
            break

    if(output is None):
        print("The item you requested is not found in the current room.")

    # if(next_room and input("Do you want to go to the next room? Ener 'yes' or 'no'").strip() == 'yes'):
    #     play_room(next_room)
    else:
        play_room(current_room, game_state)

def unlock_door(game_state, item, current_room, next_room, output, get_next_room_of_door, play_room):
    # print("check point inside unlock_door function")
    have_key = False
    for key in game_state["keys_collected"]:
        if(key["target"] == item):
            have_key = True
    # print("Have Key? ", have_key)
    if(have_key):
        output += "You unlock it with a key you have."
        print(output)
        next_room = get_next_room_of_door(item, current_room)
        if(next_room and input("Do you want to go to the next room? Ener 'yes' or 'no'").strip() == 'yes'):
          play_room(next_room, game_state)
    else:
        output += "It is locked but you don't have the key."
        print(output)


def linebreak():
    """
    Print a line break
    """
    print("\n\n")