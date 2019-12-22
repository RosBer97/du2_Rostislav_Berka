from turtle import forward, left, right, exitonclick, penup, pendown, \
speed, setup, setworldcoordinates, goto, dot, window_height, window_width, \
tracer

# to work with smaller and "nicer" numbers recalculate every coordinate relatively to minimum coordinate
# and multiply it with 1000000. ---> turtle cant draw point or distance with more than 2 decimal numbers.
# (turtle draws it, but with low precision – it draws only 2 decimal numbers (checked during testing), third and more decimal ignores...)
# Unfortunatelly coordinates  typical  have a lot of decimal numbers and numbers are very close to one another.
# So, because of this, every coordinate will be recalculate relatively to minimum coordinate.
# So in the turtle drawing minimum coordinate will be 0 and maximum will be (max - min).
# It has also advantage, that left bottom corner of bounding box will be in left bottom corner of
# turtle drawing window after setworldcoordinates function.
def modify_coor(coor_given, coor_global_min):
    return (coor_given - coor_global_min) * 10000000

# get x and y coordinate from list and use modify function defined above
def extract_x(one_feature, min_axis_value):
    return modify_coor(one_feature["geometry"]["coordinates"][0], min_axis_value)
def extract_y(one_feature, min_axis_value):
    return modify_coor(one_feature["geometry"]["coordinates"][1], min_axis_value)

# special function, which recalculate coordinates in order to fit best to the window of turtle drawing
def ratio_multiplier(size_window_x, size_window_y, size_data_x, size_data_y, wanted_coor, data_orientation):
    if data_orientation == "landscape":
        return wanted_coor * size_window_x / size_data_x
    if data_orientation == "portrait":
        return wanted_coor * size_window_y / size_data_y

# draw one point
def draw_1_point(x_coor, y_coor):
    speed("fastest")
    penup()
    goto(x_coor, y_coor)
    pendown()
    dot()
# draw boundary box of data. Its used in recurse function quadtree.
def draw_b_box(b_box_min_x, b_box_max_x, b_box_min_y, b_box_max_y, configuration_tuple):
    tracer(300, 1)
    speed("fastest")
    x_max_modified = modify_coor(b_box_max_x, configuration_tuple[5])
    x_min_modified = modify_coor(b_box_min_x, configuration_tuple[5])
    y_max_modified = modify_coor(b_box_max_y, configuration_tuple[6])
    y_min_modified = modify_coor(b_box_min_y, configuration_tuple[6])

    x_max_ratio = ratio_multiplier(configuration_tuple[0], configuration_tuple[1], configuration_tuple[2], configuration_tuple[3], x_max_modified, configuration_tuple[4])
    x_min_ratio = ratio_multiplier(configuration_tuple[0], configuration_tuple[1], configuration_tuple[2], configuration_tuple[3], x_min_modified, configuration_tuple[4])
    y_max_ratio = ratio_multiplier(configuration_tuple[0], configuration_tuple[1], configuration_tuple[2], configuration_tuple[3], y_max_modified, configuration_tuple[4])
    y_min_ratio = ratio_multiplier(configuration_tuple[0], configuration_tuple[1], configuration_tuple[2], configuration_tuple[3], y_min_modified, configuration_tuple[4])

    penup() # go to starting position
    goto(x_min_ratio, y_max_ratio) # upper left corner – starting position
    pendown()
    forward(abs(x_max_ratio - x_min_ratio)) # upper right corner
    right(90)
    forward(abs(y_max_ratio - y_min_ratio)) # bottom right corner
    right(90)
    forward(abs(x_max_ratio - x_min_ratio)) # bottom left corner
    right(90)
    forward(abs(y_max_ratio - y_min_ratio)) # go to starting position, draw line between starting and ending position
    right(90) # turn to starting position, turtle have to head to the east

# very important function, it draws all the given point and set turtle drawing environment
def draw_points(data, global_min_x, global_max_x, global_min_y, global_max_y):
    # size of window of turtle drawing = 85 % of user´s monitor width and height
    setup(width=0.85, height=0.85, startx=None, starty=None)
    print("screen size:", window_width(), window_height())
    # speed is set to fastest, but its not still enough
    speed("fastest")
    tracer(10000, 1)
    # height and width of window on user´s computer
    screen_max_x = window_width()
    screen_max_y = window_height()

    # set coordinate system for turtle drawing. Left bottom corner is 0,0 and right upper corner is maximum of window height and width.
    # -0,02 and 1,02 coeficients are useful to have a small white "frame" around data. In some situations bordering coordinates
    # (max/min x and y) and bigges bounding box couldnt be seen, bacause they were hide under border of turtle drawing window.
    # ---> windows of turtle drawing has a little bit bigger max/min x and y than given data. Thanks to this, drown data perfectly
    # fits to turtle drawing window.
    setworldcoordinates(-0.02 * screen_max_x, -0.02 * screen_max_y, 1.02 * screen_max_x, 1.02 * screen_max_y)

    # ratio of turtle drawing window (typically 16 : 9 = 1,777, but it can differ, depend on type of user´s monitor):
    ratio_window = screen_max_x / screen_max_y
    # ratio of given data (it can be anything)
    ratio_given_data = (global_max_x - global_min_x) / (global_max_y - global_min_y)
    print("ratio screen:", ratio_window, "ratio data:", ratio_given_data)

    # finding suitable multiply mode for data drown by turtle:
    if ratio_window < ratio_given_data:
        multiplier = "landscape"
    if ratio_window > ratio_given_data:
        multiplier = "portrait"
    # configuration tuple – it would be so annoying to write a lot of information during callig function draw_b_box or ratio_multiplier,
    # so I save this informations to tuple and transmit this tuple to the funtion draw_b_box and ratio_multiplier
    configuration_tuple = (screen_max_x, screen_max_y, modify_coor(global_max_x, global_min_x), modify_coor(global_max_y, global_min_y), multiplier, global_min_x, global_min_y)
    print("config tuple:", configuration_tuple)
    # drawing of points:
    for dic in data:
        point_x = extract_x(dic, global_min_x)
        point_y = extract_y(dic, global_min_y)

        x_with_ratio = ratio_multiplier(configuration_tuple[0], configuration_tuple[1], configuration_tuple[2], configuration_tuple[3], point_x, configuration_tuple[4])
        y_with_ratio = ratio_multiplier(configuration_tuple[0], configuration_tuple[1], configuration_tuple[2], configuration_tuple[3], point_y, configuration_tuple[4])
        # draw 1 point:
        draw_1_point(x_with_ratio, y_with_ratio)
    return configuration_tuple