# sort features acording to x - longitude (0) or y - latitude (1)
def sort_coordinates(features, axis):
    features.sort(key = lambda p: p["geometry"]["coordinates"][axis])
    return features

# acquire bounding points of rectangles (It may be useful in the future durink turtle drawing):
def acquire_bounding_points(list_of_feat):
    sort_x = sort_coordinates(list_of_feat,0)
    min_x = sort_x[0]["geometry"]["coordinates"][0]
    max_x = sort_x[-1]["geometry"]["coordinates"][0]

    sort_y = sort_coordinates(list_of_feat,1)
    min_y = sort_y[0]["geometry"]["coordinates"][1]
    max_y = sort_y[-1]["geometry"]["coordinates"][1]

    return (min_x, max_x, min_y, max_y)

    # build rectangle (define area of interest) from first and last coordinates in sorted list---points of rectangle:
        #top_left = (min_x, max_y)
        #top_right = (max_x, max_y)
        #bottom_left = (min_x, min_y)
        #bottom_right = (max_x, min_y)
        #print(top_left,top_right,bottom_left,bottom_right)

# This recurse function get sorted list of dictionaries with coordinates and also geometrical middle point of rectangle/square.
# This rectangle is "established" by mass of given point. Its necessary to split these points to two halves (geometrically, not
# split the list to two halves), boundary is midd point of square/rectangle. This function gives index of last point (closest point
# to the midd border) of the left part of mass of point. Principle is quite similar to binary search.
def two_halves(sorted_list, mid_rectangle, axis):
    left = 0
    right = len(sorted_list) - 1
    index_mid_list = (left + right) // 2
    # just for check:
    print("print left and right:", left, right)
    print("print index mid list:", index_mid_list, "value of this mid:", sorted_list[index_mid_list]["geometry"]["coordinates"][axis])
    print("print wanted mid_rectangle:", mid_rectangle)
    # highly unlikely, just for sure:
    if float(sorted_list[index_mid_list]["geometry"]["coordinates"][axis]) == float(mid_rectangle):
        print("situation no 1, end of searching of mid")
        return index_mid_list
    # wanted situation:
    if float(sorted_list[index_mid_list]["geometry"]["coordinates"][axis]) < float(mid_rectangle) < float(sorted_list[index_mid_list + 1]["geometry"]["coordinates"][axis]):
        print("situation no 2, end of searching of mid")
        return index_mid_list
    # another wanted situation:
    if float(sorted_list[index_mid_list - 1]["geometry"]["coordinates"][axis]) < mid_rectangle < float(sorted_list[index_mid_list]["geometry"]["coordinates"][axis]):
        print("situation no 3, end of searching of mid")
        return (index_mid_list - 1)

    # if one of these 3 conditions above is not satisfied, recurse:

    if float(sorted_list[index_mid_list]["geometry"]["coordinates"][axis]) < mid_rectangle:
        left = index_mid_list
        return two_halves(sorted_list, mid_rectangle, axis)
    if float(sorted_list[index_mid_list]["geometry"]["coordinates"][axis]) > mid_rectangle:
        right = index_mid_list
        return two_halves(sorted_list, mid_rectangle, axis)
# Input is list of dictionaries of features, axis and "special" counter. This recurse function splitting given data
# to 4 rectangles/squares using two_halves function defined above.
def quadtree(data, counter, axis):
    if len(data) <= 50:
        A = A + 1
        for index in range(len(data)):
            data[index]["properties"]["class_id"] = A
            print("returning points")
        return data

    if axis == 0:
        sort_coordinates(data,0)
        mid_rectangle = (data[-1]["geometry"]["coordinates"][0] + data[0]["geometry"]["coordinates"][0]) / 2
        # min = data[left]
        # max = data[right]
        index_mid_list = two_halves(data, mid_rectangle,0)
    if axis == 1:
        sort_coordinates(data,1)
        mid_rectangle = (data[-1]["geometry"]["coordinates"][1] + data[0]["geometry"]["coordinates"][1]) / 2
        # min = data[left]
        # max = data[right]
        index_mid_list = two_halves(data, mid_rectangle,1)
    left_half = data[:index_mid_list]
    right_half = data[index_mid_list + 1:]

    if axis == 0:
        quadtree(left_half, counter, 1)
        quadtree(right_half, counter, 1)

    if axis == 1:
        quadtree(left_half, counter, 0)
        quadtree(right_half, counter, 0)

print()
