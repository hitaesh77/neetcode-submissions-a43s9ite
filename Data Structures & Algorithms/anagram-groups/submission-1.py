class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        result = defaultdict(list)
        for string in strs:
            sorted_str = "".join(sorted(string))
            result[sorted_str].append(string)
        return list(result.values())

