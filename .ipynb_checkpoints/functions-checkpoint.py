import objects

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
        intended_action = input("What would you like to do? Type 'explore' or 'examine' or 'move room':?").strip()
        if intended_action == "explore":
            explore_room(room)
            # play_room(room, game_state)
        # elif intended_action == "unlock door":
        #     unlock_door(room)
        elif intended_action == "move room":
            move_room(room, game_state)
            # play_room(room, game_state)
        elif intended_action == "examine":
            examine_item(input("What would you like to examine?").strip(), game_state)
        else:
            print("Not sure what you mean. Type 'explore' or 'examine'.")
            # play_room(room, game_state)
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
            # else:
            #     if(item["name"] in objects.object_relations and len(objects.object_relations[item["name"]])>0):
            #         item_found = objects.object_relations[item["name"]].pop()
            #         game_state["keys_collected"].append(item_found)
            #         output += "You find " + item_found["name"] + "."
            #     else:
            #         output += "There isn't anything interesting about it."
            else:
                if(item["name"] in objects.object_relations and len(objects.object_relations[item["name"]])>0):
                    #Change .pop () for [0] so the object will not disappear for the object once we interact with it
                    #Remove the line game_state["keys_collected"].append(item_found) so key will not be added to our objects founds  immediately once we interact with the furniture
                    item_found = objects.object_relations[item["name"]][0]
                    output += "You find " + item_found["name"] + "."

                    #We will be asked if we want to collect the key
                    collect_key = input(f"Do you want to collect the key '{item_found['name']}'? Write 'yes' or 'no': ").strip().lower()
                    #If we de not write a valid action it will keep asking
                    while collect_key not in ['yes', 'no']:
                        collect_key = input(f"Not a valid answer. Do you want to collect the key '{item_found['name']}'? Write 'yes' or 'no': ").strip().lower()

                    #If we say yes, key will be added to our list of objects founds and delate from the object relaction list (will not appear again in the piano)
                    if collect_key == 'yes':
                          game_state["keys_collected"].append(item_found)
                          output += "You collected it."
                          objects.object_relations[item["name"]].remove(item_found)
                    #If we say no, nothing happen.
                    else:
                          output += "You did not collect it."
                else:
                    output += "There isn't anything interesting about it."
            print(output)
            break

    if(output is None):
        print("The item you requested is not found in the current room.")

    # if(next_room and input("Do you want to go to the next room? Ener 'yes' or 'no'").strip() == 'yes'):
    #     play_room(next_room)
    # else:
    #     play_room(current_room, game_state)

def unlock_door(game_state, item, current_room, next_room, output, get_next_room_of_door, play_room):
    # print("check point inside unlock_door function")
    have_key = False
    for key in game_state["keys_collected"]:
        if(key["target"] == item):
            have_key = True
    # print("Have Key? ", have_key)
    if(have_key):
        output += "You unlock it with a key you have."
        item["locked"] = False
        print(output)
        # next_room = get_next_room_of_door(item, current_room)
        # if(next_room and input("Do you want to go to the next room? Ener 'yes' or 'no'").strip() == 'yes'):
        #   play_room(next_room, game_state)
    else:
        output += "It is locked but you don't have the key."
        print(output)

# def unlock_door(room):
#     """
#     Action to unlock doors
#     """
#     door_name = input("Which door would you like to unlock? ").strip() #Ask the player to choose a door to unlock.
#     for item in object_relations[room["name"]]: #search if the door is in this room
#         if item["type"] == "door" and item["name"] == door_name: #is the door locked?
#             if not item["locked"]: #the door is found and it is not locked (item["locked"] is False), the player is informed that the door is already unlocked, and the function exits.
#                 print(f"{door_name} is already unlocked.")
#                 return
#             have_key = any(key["target"] == item for key in game_state["keys_collected"]) #this line checks if the player has the key for that door
#             if have_key:
#                 item["locked"] = False  # Unlock the door
#                 print(f"You unlock {door_name} with a key you have.")
#                 return
#             else: #When player does not have the key :(
#                 print(f"{door_name} is locked, and you don't have the key.")
#                 return
#     print("The door you requested is not found in the current room.") #First ondition has not found the door in current objett_relations room

def move_room(current_room, game_state):
    """
    Move to other rooms, check if doors are unlocked
    """
    print("You can see doors leading to other rooms:")
    doors_in_room = [item for item in objects.object_relations[current_room["name"]] if item["type"] == "door"] #This line is designed to generate list of all the doors in the current room.

    # Display doors and their status
    for door in doors_in_room:
        if door["locked"]:
            print(f"{door['name']} is locked.")
        else:
            print(f"{door['name']} is unlocked.")

    # linebreak()
    # Player chooses a door
    chosen_door_name = input("Which door would you like to go through? Please type the door name exactly as shown above: ").strip()

    # Check if the door exists and if its locked or unlocked
    for door in doors_in_room:
        if door["name"].lower() == chosen_door_name.lower():
            if door["locked"]:
                print(f"Sorry, {chosen_door_name} is locked. You need to unlock it first if you have the key.")
            else:
                next_room = get_next_room_of_door(door, current_room)
                print(f"Moving through {chosen_door_name}, you enter {next_room['name']}.")
                play_room(next_room, game_state)
                return  # Ends the function after moving to the next room or informing about the locked status
        else:
            print("There doesn't seem to be a door by that name here. Please check the door name and try again.") #invalid door selection

def linebreak():
    """
    Print a line break
    """
    print("\n")