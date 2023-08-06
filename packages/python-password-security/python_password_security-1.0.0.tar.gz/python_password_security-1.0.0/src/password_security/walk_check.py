#     Author for this part of the script: Rich Kelley, rk5devmail@gmail.com, @RGKelley5

def walk_checker(password, length=4, strict=True, loop=False):
    with open("graph.py", "r") as fin:
        graph = eval(fin.read())

    result = False
    path_length = 1

    if strict and len(password) != length:
        return result

    for i in range(len(password)):
        current_letter = password[i]

        if i < len(password) - 1:
            next_letter = password[i + 1]

            if current_letter in graph:
                if loop:
                    if next_letter in graph[current_letter].values():
                        path_length += 1

                        if path_length == length:
                            result = True

                    else:
                        result = False
                        path_length = 1

                else:
                    if next_letter in graph[current_letter].values() and next_letter.lower() != current_letter.lower():
                        path_length += 1

                        if path_length == length:
                            result = True

                    else:
                        result = False
                        path_length = 1

    return result
