from faker import Faker

from evolution_client import game, register, observe

fake = Faker()

if __name__ == "__main__":
    # generate 3 new users and save their ids
    user_ids = []
    player_ids = []
    for _ in range(3):
        response = register.register_user(
            fake.user_name(),
            fake.email(),
            fake.password(),
        )
        user_ids.append(response["user_id"])

    # start a new game
    response = game.new_game(user_ids[0])

    game_id = response["id"]

    # join the game
    for user_id in user_ids:
        response = game.join_game(game_id, user_id)
        player_ids.append(response["id"])
    # get the game
    response = observe.get_game(game_id)
    print(response)

    # start the game
    response = game.start_game(game_id)
    print(response)

    # get the game again
    response = observe.get_game(game_id)
    print(response)

    # get the player
    response = observe.get_player(game_id, player_ids[0])
    print(response)
