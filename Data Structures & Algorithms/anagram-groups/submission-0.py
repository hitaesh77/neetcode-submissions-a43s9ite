class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        result = []
        distinct_dicts = []
        distinct_size = 0

        for i,curr_str in enumerate(strs):
            temp_dict = {}
            # load temporary dict to compare to existing dicts
            for char in curr_str:
                if char in temp_dict:
                    temp_dict[char] += 1
                else:
                    temp_dict[char] = 1

            temp_dict = dict(sorted(temp_dict.items()))
            if temp_dict not in distinct_dicts:
                distinct_dicts.append(temp_dict)
                result.append([])
                result[distinct_size].append(curr_str)
                distinct_size += 1
            else:
                idx = distinct_dicts.index(temp_dict)
                result[idx].append(curr_str)
        
        print(result)
        return result

