# dict_union_with.py
# todo Consider that the functionality is shadowed by the new Python dict
#  union operator: |=


def union_with(destination: dict, to_merge: dict) -> dict:
    """ Merges to_merge into destination, keeping the contents of the latest
    key found when two keys have colliding names. Similar to unionWith in
    Haskell. """
    if 0 == len(destination):
        return to_merge.copy()
    else:
        result: dict = destination.copy()
        # print("current starting dict %s" % result)
        # print("to merge with %s" % to_merge)
        for key in to_merge.keys():
            if key in result:
                if type(result[key]) == dict:
                    # print("%s is a dictionary" % result[key])
                    # print("union with \n%s\n and \n%s" % (result[key],
                    #                                       to_merge[key]))
                    result[key] = union_with(result[key], to_merge[key])
                else:
                    result[key] = to_merge[key]
            else:
                result[key] = to_merge[key]
        return result


def union_all_with(merge_result: dict,
                   list_of_dicts_to_merge: [dict]) -> dict:
    """ Merges all the dictionaries from list_of_dicts_to_merge into
    merge_result, using union_with. """
    for dict_to_merge in list_of_dicts_to_merge:
        merge_result = union_with(merge_result, dict_to_merge)
    return merge_result


def union_with_all(list_of_destinations: [dict],
                   dict_to_merge: dict) -> [dict]:
    """ Merges dict_to_merge into all of the dictionaries from
    list_of_destinations. """
    list_of_merge_results = []
    for destination in list_of_destinations:
        list_of_merge_results.append(
            union_with(destination,
                       dict_to_merge)
        )
    return list_of_merge_results
