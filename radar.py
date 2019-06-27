from time import sleep
import subprocess
import platform


X_SIZE, Y_SIZE = 28, 28
Screen = [['' for x in range(Y_SIZE)] for y in range(X_SIZE)]


def print_screen():
    # str_format = "{:" + str(X_SIZE - 1) + "}"
    str_format = "{:" + "1" + "}"
    print('\n'.join([''.join([str_format.format(item) for item in row])
                     for row in Screen]))
    if platform.system() == "Windows":
        subprocess.Popen("cls", shell=True).communicate()
    else:  # Linux and Mac
        print("\033c", end="")


def gen_borders():
    for i in range(X_SIZE):
        for j in range(Y_SIZE):
            Screen[i][j] = ''
    for i in range(X_SIZE):
        Screen[i][0] = Screen[i][Y_SIZE - 1] = '#'

    for j in range(Y_SIZE):
        Screen[0][j] = Screen[X_SIZE - 1][j] = '#'


def fill_cursor():
    center_x = X_SIZE // 2
    center_y = Y_SIZE // 2
    # check if there are more '+' es to be added  to the cursor
    # vertical axis
    for i in range(center_x - 1, 1, -1):
        if Screen[i][center_y - 1] == '+':
            for j in range(i + 1, center_x, 1):
                Screen[j][center_y - 1] = '+'
            return

    for i in range(center_x - 1, X_SIZE - 1, 1):
        if Screen[i][center_y - 1] == '+':
            for j in range(i - 1, center_x, -1):
                Screen[j][center_y - 1] = '+'
            return

    # horizontal axis
    for j in range(center_y - 1, 1, -1):
        if Screen[center_x - 1][j] == '+':
            for i in range(j + 1, center_y, 1):
                Screen[center_x - 1][i] = '+'
            return

    for j in range(center_y - 1, Y_SIZE - 1, 1):
        if Screen[center_x - 1][j] == '+':
            for i in range(j - 1, center_y, 1):
                Screen[center_x - 1][i] = '+'
            return

# def ascii_radar():
#     turn = Y_SIZE // 2
#     while True:
#         if Y_SIZE // 2 <= turn < Y_SIZE:
#             # quad 1
#             # how much does the cursor turn on the radar depending
#             # on the clock cycle we're in
#             segments = split_arr(X_SIZE // 2, turn - Y_SIZE // 2)
#             print_list(segments)
#             tmp_i = 0
#             tmp_turn = turn
#
#             gen_borders()
#             for i in segments:
#                 for j in range(i):
#                     if tmp_i != 0 and tmp_i != X_SIZE - 1 and tmp_turn != 0 and tmp_turn != Y_SIZE - 1:
#                         Screen[tmp_i][tmp_turn] = '+'
#                     tmp_i = tmp_i + 1
#                 tmp_turn = tmp_turn - 1
#
#             print_screen()
#             # sleep sleeps in seconds
#             sleep(0.5)
#             # quad 2
#             turn = turn + 1


def print_screen_re(quad1_swipe):
    # remove dupes
    for i in range(0, len(quad1_swipe) - 1, 1):
        if quad1_swipe[i] == quad1_swipe[i + 1]:
            quad1_swipe[i] = []

    quad1_swipe = [turn for turn in quad1_swipe if turn != []]

    for turn in quad1_swipe:
        gen_borders()
        for step in turn:
            Screen[step[0]][step[1]] = "+"
        print_screen()


def ascii_radar_re():
    center_x = X_SIZE // 2
    center_y = Y_SIZE // 2
    quad1 = []
    quad1_swipe = []

    # set up cursor
    # set quads
    # quad1
    for i in range(center_x - 1, 0, -1):
        b = (i * (center_y - 1) - (center_x - 1) * 1) / (center_y - 1 - 1)
        # if (i * (center_y - 1) - (center_x - 1) * 1) % (center_y - 1 - 1) >= 0.5:
        #     b = int(round(b + 1))
        a = (center_x - 1 - b) / (center_y - 1)
        # if (center_x - 1 - b) % (center_y - 1) >= 0.5:
        #     a = int(round(a + 1))

        # print("A(", 1, ",", i, ")")
        # print("B(", center_y - 1, ",", center_x - 1, ")")
        # print("b = ", b)
        # print("a = ", a)

        for k in range(1, center_y, 1):
            lin_y = int(round(a * k + b))
            if lin_y > center_x - 1:
                lin_y = center_x - 1
            quad1.append([lin_y, k])
        quad1_swipe.append(quad1.copy())
        quad1.clear()

    print("quad #1 lower: ")
    # print_screen_re(quad1_swipe)
    print("---------------------------")

    for j in range(1, center_y, 1):
        if center_y - 1 - j == 0:
            b = center_y - 1
            a = 0
        else:
            b = (1 * (center_y - 1) - (center_x - 1) * j) / (center_y - 1 - j)
            # if (1 * (center_y - 1) - (center_x - 1) * j) % (center_y - 1 - j) >= 0.5:
            #     b = int(round(b + 1))
            a = (center_x - 1 - b) / (center_y - 1)
            # if (center_x - 1 - b) % (center_y - 1) >= 0.5:
            #     a = int(round(a + 1))

        print("A(", j, ",", 1, ")")
        print("B(", center_y - 1, ",", center_x - 1, ")")
        print("b = ", b)
        print("a = ", a)

        valid_slope = False
        increased_slope = False

        while not valid_slope:
            for k in range(1, center_x, 1):
                lin_y = int(round(a * k + b))
                if lin_y <= 0:
                    a = a + 0.5
                    increased_slope = True
                    break
                if lin_y == 0:
                    lin_y = lin_y + 1
                if lin_y < 0:
                    lin_y = center_y - 1
                if lin_y >= center_y:
                    lin_y = center_y - 1
                quad1.append([k, lin_y])

            if increased_slope:
                increased_slope = False
                continue

            quad1_swipe.append(quad1.copy())
            quad1.clear()
            valid_slope = True

    print("quad #1 upper: ")
    # print_screen_re(quad1_swipe)
    print("---------------------------")

    quad_size = len(quad1_swipe)
    for i in range(quad_size - 1, -1, -1):
        for step in quad1_swipe[i]:
            quad1.append([step[0], Y_SIZE - 1 - step[1]])
        quad1_swipe.append(quad1.copy())
        quad1.clear()

    print("quad #2")
    # print_screen_re(quad1_swipe)
    print("---------------------------")

    for i in range(2 * quad_size - 1, quad_size - 1, -1):
        for step in quad1_swipe[i]:
            quad1.append([X_SIZE - 1 - step[0], step[1]])
        quad1_swipe.append(quad1.copy())
        quad1.clear()

    print("quad #3")
    # print_screen_re(quad1_swipe)
    print("---------------------------")

    for i in range(quad_size - 1, -1, -1):
        for step in quad1_swipe[i]:
            quad1.append([X_SIZE - 1 - step[0], step[1]])
        quad1_swipe.append(quad1.copy())
        quad1.clear()

    print("quad #4")
    # print_screen_re(quad1_swipe)
    print("---------------------------")

    while True:
        # animate cursor
        print_screen_re(quad1_swipe)
        # Slow down cursor speed/ avoid 100% cpu
        # sleep(0.05)


def split_arr(n_size, turn=0):
    segments_upper = []
    segments_lower = []

    if n_size == 1:
        segments_upper.append(1)
        segments_lower.append(0)
        return segments_lower, segments_upper

    segments_upper_size = 0
    while segments_upper_size == 0:
        segments_upper_no = 2 ** turn
        segments_upper_size = (n_size // 2) // segments_upper_no

        if segments_upper_size == 0:
            turn = turn - 1
            continue

        r = (n_size // 2) % segments_upper_size
        last_upper_segment_size = 0
        if r != 0:
            last_upper_segment_size = segments_upper_size + r

        for i in range(0, n_size // 2 - last_upper_segment_size, segments_upper_size):
            segments_upper.append(segments_upper_size)

        if r != 0:
            segments_upper.append(segments_upper_size + r)

    segments_lower_size = 0
    while segments_lower_size == 0:
        segments_lower_no = segments_upper_no // 2
        if segments_lower_no == 0:
            segments_lower_no = 1
        segments_lower_size = (n_size // 2) // segments_lower_no

        if segments_lower_size == 0:
            turn = turn - 1
            continue

        r = (n_size // 2) % segments_lower_size
        if 0 < n_size / 2 - n_size // 2 < 1:
            r = 1

        last_lower_segment_size = 0
        if r != 0:
            last_lower_segment_size = segments_lower_size + r

        for i in range(0, n_size // 2 - last_lower_segment_size, segments_lower_size):
            segments_upper.append(segments_lower_size)

        if r != 0:
            segments_upper.append(segments_lower_size + r)

    return segments_lower + segments_upper


def print_list(l):
    for item in l:
        print(item)


# def split_arr_test():
    # arr = [5, 6, 7, 8, 7]
    # segments_lower, segments_upper = split_arr(arr)
    # print_list(segments_upper)
    # print_list(segments_lower)
    # print('---------------------')
    # arr = [5]
    # segments_lower, segments_upper = split_arr(arr)
    # print_list(segments_upper)
    # print_list(segments_lower)
    # print('---------------------')
    # arr = [5, 6]
    # segments_lower, segments_upper = split_arr(arr)
    # print_list(segments_upper)
    # print_list(segments_lower)
    # print('---------------------')
    # arr = [5, 6, 7, 8]
    # segments_lower, segments_upper = split_arr(arr)
    # print_list(segments_upper)
    # print_list(segments_lower)
    # print('---------------------')
    # arr = [5, 6, 7, 8, 5, 6, 7, 8, 9]
    # segments_lower, segments_upper = split_arr(arr)
    # print_list(segments_upper)
    # print_list(segments_lower)
    # print('---------------------')
    # arr = [5, 6, 7, 8, 5, 6, 7, 8, 9, 1,
    #        5, 6, 7, 8, 5, 6, 7, 8, 9, 1,
    #        5, 6, 7, 8, 5, 6, 7, 8, 9, 1,
    #        5, 6, 7, 8, 5, 6, 7, 8, 9, 1,
    #        5, 6, 7, 8, 5, 6, 7, 8, 9, 1]
    # segments_lower, segments_upper = split_arr(arr, 1)
    # print_list(segments_upper)
    # print_list(segments_lower)
    # print('---------------------')
    # arr = [5, 6, 7, 8, 5, 6, 7, 8, 9, 1,
    #        5, 6, 7, 8, 5, 6, 7, 8, 9, 1,
    #        5, 6, 7, 8, 5, 6, 7, 8, 9, 1,
    #        5, 6, 7, 8, 5, 6, 7, 8, 9, 1,
    #        5, 6, 7, 8, 5, 6, 7, 8, 9, 1]
    # segments_lower, segments_upper = split_arr(arr, 2)
    # print_list(segments_upper)
    # print_list(segments_lower)
    # print('---------------------')
    # arr = [5, 6, 7, 8, 5, 6, 7, 8, 9, 1,
    #        5, 6, 7, 8, 5, 6, 7, 8, 9, 1,
    #        5, 6, 7, 8, 5, 6, 7, 8, 9, 1,
    #        5, 6, 7, 8, 5, 6, 7, 8, 9, 1,
    #        5, 6, 7, 8, 5, 6, 7, 8, 9, 1]
    # segments = split_arr(50, 3)
    # print_list(segments)
    # print('---------------------')

ascii_radar_re()
# split_arr_test()
gen_borders()
print_screen()







