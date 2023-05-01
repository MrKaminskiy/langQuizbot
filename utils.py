import os


def save_word(user_id, word, translation):
    file_name = f"data/{user_id}.txt"
    with open(file_name, "a") as f:
        f.write(f"{word}:{translation}\n")


def delete_word(user_id, word_to_delete):
    with open(f"data/{user_id}.txt", "r") as f:
        lines = f.readlines()
    with open(f"{user_id}.txt", "w") as f:
        for line in lines:
            if line.strip().split(",")[0] != word_to_delete:
                f.write(line)
    return True



def modify_word(user_id, word, new_translation):
    file_name = f"data/{user_id}.txt"
    with open(file_name, "r") as f:
        lines = f.readlines()

    with open(file_name, "w") as f:
        for line in lines:
            w, translation = line.strip().split(":")
            if w == word:
                f.write(f"{word}:{new_translation}\n")
            else:
                f.write(line)


def get_all_words(user_id):
    file_name = f"data/{user_id}.txt"
    if not os.path.exists(file_name):
        return []

    with open(file_name, "r") as f:
        lines = f.readlines()
        return [line.strip().split(":") for line in lines]
