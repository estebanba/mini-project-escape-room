# define rooms and items

couch = {
    "name": "couch",
    "type": "furniture",
}
piano = {
    "name": "piano",
    "type": "furniture",
}
queen_bed = {
    "name": "queen bed",
    "type": "furniture"
}
double_bed =  {
    "name": "double bed",
    "type": "furniture"
}
dresser = {
    "name": "dresser",
    "type": "furniture"
}
dining_table = {
    "name": "dining table",
    "type": "furniture"
}
# ---------------------------------------------------------------------------------------------------------------------------------------------------------

door_a = {
    "name": "door a",
    "type": "door",
}

door_b = {
    "name": "door b",
    "type": "door",
}
door_c = {
    "name": "door c",
    "type": "door",
}
door_d = {
    "name": "door d",
    "type": "door",
}

# ---------------------------------------------------------------------------------------------------------------------------------------------------------

key_a = {
    "name": "key for door a",
    "type": "key",
    "target": door_a,
}
key_b = {
    "name": "key for door b",
    "type": "key",
    "target": door_b,
}

key_c = {
    "name": "key for door c",
    "type": "key",
    "target": door_c,
}

key_d = {
    "name": "key for door d",
    "type": "key",
    "target": door_d,
}



game_room = {
    "name": "game room",
    "type": "room",
}
bedroom_1 = {
    "name": "bedroom 1",
    "type": "room",
}
bedroom_2 = {
    "name": "bedroom 2",
    "type": "room",
}
living_room = {
    "name": "living room",
    "type": "room",
}

outside = {
  "name": "outside"
}

all_rooms = [game_room, bedroom_1, bedroom_2, living_room, outside]

all_doors = [door_a, door_b, door_c, door_d]

# define which items/rooms are related

object_relations = {
    "game room": [couch, piano, door_a],
    "piano": [key_a],
    "door a": [game_room, bedroom_1],
    "bedroom 1": [door_a, queen_bed, door_b, door_c],
    "queen bed": [key_b],
    "door b": [bedroom_1, bedroom_2],
    "bedroom 2": [door_b, double_bed, dresser],
    "double bed": [key_c],
    "dresser": [key_d],
    "door c": [bedroom_1, living_room],
    "living room": [dining_table, door_d],
    "door d": [living_room, outside],
    "outside": [door_d],
}