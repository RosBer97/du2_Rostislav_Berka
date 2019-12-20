# sort list of features acording to x - longitude (0) or y - latitude (1)
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

    # build rectangle/square (define area of interest) from first and last coordinates in sorted list---points of rectangle:
        #top_left = (min_x, max_y)
        #top_right = (max_x, max_y)
        #bottom_left = (min_x, min_y)
        #bottom_right = (max_x, min_y)

# This recurse function get sorted list of dictionaries with coordinates, geometrical middle point of rectangle/square,
# axis (0 -> x, 1 -> y) and also left and right – boundary of the list (indexes).
# This rectangle is "established" by given points. Its necessary to split these points to two halves (geometrically, not
# split the list to two halves), boundary is midd point of square/rectangle. This function gives index of first point (closest point
# to the midd border) of the right part of points. Principle is quite similar to binary search.
def two_halves(sorted_list, mid_rectangle, left, right, axis):
    if len(sorted_list) == 0: # for case, that sorted list is empty
        return 0
    else: # for all other cases
        index_mid_list = (left + right) // 2
        # just for check:
        print("len of list",len(sorted_list))
        print("print left and right:", left, right)
        print("print index mid list:", index_mid_list, "value of this mid:", sorted_list[index_mid_list]["geometry"]["coordinates"][axis])
        print("print wanted mid_rectangle:", mid_rectangle)
        # There are special conditions for list with only 1 feature:
        if len(sorted_list) == 1:
            if (sorted_list[index_mid_list]["geometry"]["coordinates"][axis]) < float(mid_rectangle):
                return index_mid_list + 1 # <- In this situation, first point of right part is little bit abstract.
            if (sorted_list[index_mid_list]["geometry"]["coordinates"][axis]) > float(mid_rectangle):
                return index_mid_list

        # highly unlikely, just for sure:
        if float(sorted_list[index_mid_list]["geometry"]["coordinates"][axis]) == float(mid_rectangle):
            print("situation no 1, end of searching of mid")
            return index_mid_list
        # wanted situation:
        if float(sorted_list[index_mid_list]["geometry"]["coordinates"][axis]) < float(mid_rectangle) < float(sorted_list[index_mid_list + 1]["geometry"]["coordinates"][axis]):
            print("situation no 2, end of searching of mid")
            return index_mid_list + 1
        # another wanted situation:
        if float(sorted_list[index_mid_list - 1]["geometry"]["coordinates"][axis]) < mid_rectangle < float(sorted_list[index_mid_list]["geometry"]["coordinates"][axis]):
            print("situation no 3, end of searching of mid")
            return index_mid_list
        # If all of the points lie only in one half of rectangular/square (mid_rectangle is bigger than all of the points)
        if (right - left == 1) and float(sorted_list[index_mid_list]["geometry"]["coordinates"][axis]) < mid_rectangle:
            print("situation no 4, end of searching of mid")
            return right + 1 # <- In this situation, first point of right part is little bit abstract.
        # If all of the points lie only in one half of rectangular/square (mid_rectangle is smaller than all of the points)
        if (left == 0 and right == 0) and float(sorted_list[index_mid_list]["geometry"]["coordinates"][axis]) > mid_rectangle:
            print("situation no 5, end of searching of mid")
            return left


        # if one of those conditions above is not satisfied, recurse:

        if float(sorted_list[index_mid_list]["geometry"]["coordinates"][axis]) < mid_rectangle:
            left = index_mid_list
            return two_halves(sorted_list, mid_rectangle, left, right, axis)
        if float(sorted_list[index_mid_list]["geometry"]["coordinates"][axis]) > mid_rectangle:
            right = index_mid_list
            return two_halves(sorted_list, mid_rectangle, left, right, axis)

# Input is list of dictionaries of features, "special" counter (list) and bounding points of rectangle/square. This recurse function splits given data
# to 4 rectangles/squares using two_halves function defined above.
def quadtree(data, cluster_counter, min_x, max_x, min_y, max_y):
    # for case, if all of the points lies in one half of rectangle and another (this) half is empty:
    if len(data) == 0:
        print("empty list")
    # for most of the cases – if list is not empty:
    else:
        # end condition for recurse function:
        if (len(data) < 50):
            # cluster counter – its a list with one element – its index is 0 and value of this element is also 0 (at the beginning
            # of the script). If end condition of recursion is satisfied ---> add + 1 to the value in the list cluster counter.
            # So, the value is bigger and bigger and at the end of the script it says, how many cluster are made.
            cluster_counter[0] = cluster_counter[0] + 1
            for index in range(len(data)):
                data[index]["properties"]["cluster_id"] = cluster_counter[0] # add cluster id, which is original for every cluster,
                # thanks to the procces of adding + 1, 3 lines above
                print(cluster_counter[0])
            return data

        left = 0
        right = len(data) - 1

        mid_rectangle_x = (min_x + max_x) / 2
        mid_rectangle_y = (min_y + max_y) / 2
        # start of splitting list to 2 halves according to x axis
        sort_coordinates(data, 0)
        index_geometrical_mid_x = two_halves(data, mid_rectangle_x, left, right, 0)
        print(index_geometrical_mid_x)
        # Point with index_geometrical_mid is first (closest to the geometrical midd of rectangle/square)
        # in the right half of the rectangle/square. So, this point belongs to right_half.
        left_half_x = data[: index_geometrical_mid_x ]
        right_half_x = data[index_geometrical_mid_x :]
        # now there are 2 halves sorted according to x, its necessary to sort them according to y.
        sort_coordinates(left_half_x, 1)
        sort_coordinates(right_half_x, 1)
        # right indexes of these two halves:
        right_left_halve = len(left_half_x) - 1
        right_right_halve = len(right_half_x) - 1
        # Finding index of point closest to the geometrical mid of rectangles/squares.
        index_geometrical_mid_y_left = two_halves(left_half_x, mid_rectangle_y, left, right_left_halve, 1)
        index_geometrical_mid_y_right = two_halves(right_half_x, mid_rectangle_y, left, right_right_halve, 1)

        # building 4 rectangles/squares:

        left_upper = left_half_x[index_geometrical_mid_y_left :]
        left_bottom = left_half_x[: index_geometrical_mid_y_left]

        right_upper = right_half_x[index_geometrical_mid_y_right :]
        right_bottom = right_half_x[: index_geometrical_mid_y_right]

        # recurse on these 4 rectangles/squares:
        quadtree(left_upper, cluster_counter, min_x, mid_rectangle_x, mid_rectangle_y, max_y)
        quadtree(left_bottom, cluster_counter, min_x, mid_rectangle_x, min_y, mid_rectangle_y)

        quadtree(right_upper, cluster_counter, mid_rectangle_x, max_x, mid_rectangle_y, max_y)
        quadtree(right_bottom, cluster_counter, mid_rectangle_x, max_x, min_y, mid_rectangle_y)

