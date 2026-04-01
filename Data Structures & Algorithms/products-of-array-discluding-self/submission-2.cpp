class Solution {
public:
    vector<int> productExceptSelf(vector<int>& nums) {
        int prod = 1;
        int z_cnt = 0;

        for(int i = 0; i < nums.size(); i++){
            if (nums[i] == 0){
                z_cnt += 1;
            } else {
                prod *= nums[i];
            }
        }

        vector<int> res(nums.size(), 0);
        if(z_cnt > 1){
            return res;
        }

        for(int j = 0; j < nums.size(); j++){
            if (z_cnt == 1){
                if (nums[j] == 0){
                    res[j] = prod;
                }
            } else {
                res[j] = prod / nums[j];
            }
        }
        return res;
    }
};
