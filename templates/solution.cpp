/*
 * Problem   : 0001. Two Sum
 * Topic     : Arrays
 * Difficulty: Easy        // Easy | Medium | Hard
 * Link      : https://leetcode.com/problems/two-sum/
 * Time      : O(n)
 * Space     : O(n)
 *
 * Approach:
 *   Store each number's complement in a hash map while scanning.
 *   When the complement is found, return both indices.
 */

#include <bits/stdc++.h>
using namespace std;

class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        unordered_map<int, int> seen;

        for (int i = 0; i < static_cast<int>(nums.size()); ++i) {
            int complement = target - nums[i];

            if (seen.count(complement)) {
                return {seen[complement], i};
            }

            seen[nums[i]] = i;
        }

        return {};
    }
};
