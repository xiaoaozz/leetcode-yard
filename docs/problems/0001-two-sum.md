---
id: 1
title: Two Sum
difficulty: Easy

tags:
  - array
  - hash-table

top150: true

leetcode: https://leetcode.com/problems/two-sum/
---

# Two Sum

## 题目描述

给定一个整数数组 `nums` 和一个整数目标值 `target`，请你在该数组中找出 **和为目标值** `target`  的那 **两个** 整数，并返回它们的数组下标。

你可以假设每种输入只会对应一个答案，并且你不能使用两次相同的元素。

你可以按任意顺序返回答案。

**示例 1：**

```
输入：nums = [2,7,11,15], target = 9
输出：[0,1]
解释：因为 nums[0] + nums[1] == 9 ，返回 [0, 1] 。
```

**示例 2：**

```
输入：nums = [3,2,4], target = 6
输出：[1,2]
```

**示例 3：**

```
输入：nums = [3,3], target = 6
输出：[0,1]
```

**约束条件：**

- `2 <= nums.length <= 10^4`
- `-10^9 <= nums[i] <= 10^9`
- `-10^9 <= target <= 10^9`
- 只存在一个有效答案

## 思路分析

### 方法一：暴力枚举

遍历所有可能的两数组合，检查它们的和是否等于 `target`。

- 时间复杂度：$O(n^2)$
- 空间复杂度：$O(1)$

### 方法二：哈希表（推荐）

遍历数组，对于每个元素 `nums[i]`，检查 `target - nums[i]` 是否已经出现在哈希表中。

- 时间复杂度：$O(n)$
- 空间复杂度：$O(n)$

## Java

代码见：

[solutions/java/0001_TwoSum.java](../../solutions/java/0001_TwoSum.java)

## Go

代码见：

[solutions/golang/0001_two_sum.go](../../solutions/golang/0001_two_sum.go)

## Python

代码见：

[solutions/python/0001_two_sum.py](../../solutions/python/0001_two_sum.py)

## C++

代码见：

[solutions/cpp/0001_two_sum.cpp](../../solutions/cpp/0001_two_sum.cpp)

## Rust

代码见：

[solutions/rust/0001_TwoSum.rs](../../solutions/rust/0001_TwoSum.rs)

## TypeScript

代码见：

[solutions/typescript/0001_two_sum.ts](../../solutions/typescript/0001_two_sum.ts)
