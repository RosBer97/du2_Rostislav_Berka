# sort features acording to x - longitude (0) or y - latitude (1)
def sort_coordinates(features, axis):
    features.sort(key = lambda p: p["geometry"]["coordinates"][axis])
    return features

# acquire bounding points of rectangles (It also may be useful in the future for turtle drawing):
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
# This rectangle is "established" by given points. Its necessary to split these points to two halves (geometrically, not
# split the list to two halves), boundary is midd point of square/rectangle. This function gives index of last point (closest point
# to the midd border) of the left part of mass of point. Principle is quite similar to binary search.
def two_halves(sorted_list, mid_rectangle, left, right, axis):
    index_mid_list = (left + right) // 2
    # just for check:
    print("len of list",len(sorted_list))
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
    # If all of the points lie only in one half of rectangular/square (mid_rectangle is bigger than all of the points)
    if (right - left == 1) and float(sorted_list[index_mid_list]["geometry"]["coordinates"][axis]) < mid_rectangle:
        print("situation no 4, end of searching of mid")
        return right
    # If all of the points lie only in one half of rectangular/square (mid_rectangle is smaller than all of the points)
    if (left == 0 and right == 0) and float(sorted_list[index_mid_list]["geometry"]["coordinates"][axis]) > mid_rectangle:
        print("situation no 5, end of searching of mid")
        return left


    # if one of these conditions above is not satisfied, recurse:

    if float(sorted_list[index_mid_list]["geometry"]["coordinates"][axis]) < mid_rectangle:
        left = index_mid_list
        return two_halves(sorted_list, mid_rectangle, left, right, axis)
    if float(sorted_list[index_mid_list]["geometry"]["coordinates"][axis]) > mid_rectangle:
        right = index_mid_list
        return two_halves(sorted_list, mid_rectangle, left, right, axis)

# Input is list of dictionaries of features, axis and "special" counter. This recurse function splits given data
# to 4 rectangles/squares using two_halves function defined above.
def quadtree(data, list, axis, final_list, min_x, max_x, min_y, max_y):
    if len(data) <= 50:
        list[0] = list[0] + 1
        for index in range(len(data)):
            data[index]["properties"]["cluster_id"] = list[0]
            final_list.append(data[index])
            print(len(final_list))
        return final_list

    left = 0
    right = len(data) - 1
    if axis == 0:
        mid_rectangle = (min_x + max_x) / 2
    if axis == 1:
        mid_rectangle = (min_y + max_y) / 2

    sort_coordinates(data, axis)
    index_geometrical_mid = two_halves(data, mid_rectangle, left, right,axis)

    left_half = data[:index_geometrical_mid]
    right_half = data[index_geometrical_mid + 1:]

    if axis == 0:
        quadtree(left_half, list, 1, final_list, min_x, mid_rectangle, min_y, max_y)
        quadtree(right_half, list, 1, final_list, mid_rectangle, max_x, min_y, max_y)

    if axis == 1:
        quadtree(left_half, list, 0, final_list, min_x, max_x, min_y, mid_rectangle)
        quadtree(right_half, list, 0, final_list, min_x, max_x, mid_rectangle, max_y)

