class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        groups = dict()
        res = []

        for s in strs:
            s_sort = sorted(s)
            s_sort_s = ''.join(s_sort)

            if s_sort_s in groups:
                groups[s_sort_s].append(s)
            else:
                groups[s_sort_s] = []
                groups[s_sort_s].append(s)
        
        for v in groups.values():
            res.append(v)
        
        return res