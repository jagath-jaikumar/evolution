from faker import Faker

from evolution_client import game, user

fake = Faker()

if __name__ == "__main__":
    # generate 3 new users and save their ids
    user_ids = []
    for _ in range(3):
        response = user.register_user(fake.user_name(), fake.email(), fake.password())
        user_ids.append(response["user_id"])

    # start a new game from the first user
    response = game.new_game(user_ids[0])

    game_id = response["game_id"]

    # join the game from the second user
    response = game.join_game(game_id, user_ids[1])
    response = game.join_game(game_id, user_ids[2])

    # get the game
    response = game.get_game(game_id)
    print(response)

    # start the game
    response = game.start_game(game_id)
    print(response)
