def quadtree(data,num_point, list, axis, final_list, min_x, max_x, min_y, max_y)
    if len(data) <= num_point:
        list[0] = list[0] + 1
        for index in range(len(data)):
            data[index]["properties"]["cluster_id"] = list[0]
            final_list.append(data[index])
            print(len(final_list))
        return final_list