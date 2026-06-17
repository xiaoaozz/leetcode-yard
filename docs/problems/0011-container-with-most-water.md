---
id: 11
title: Container With Most Water
difficulty: Medium

tags:
  - array
  - two-pointers

top150: true

leetcode: https://leetcode.com/problems/container-with-most-water/
---

# Container With Most Water

## 题目描述

给定一个长度为 `n` 的整数数组 `height`。有 `n` 条垂线，第 `i` 条线的两个端点是 `(i, 0)` 和 `(i, height[i])`。

找出其中的两条线，使得它们与 `x` 轴共同构成的容器可以容纳最多的水。

返回容器可以储存的最大水量。

**示例 1：**

```
输入：[1,8,6,2,5,4,8,3,7]
输出：49
```

## 思路分析

### 方法一：双指针

从两端向中间收缩，每次移动较短的那条线。

- 时间复杂度：$O(n)$
- 空间复杂度：$O(1)$

## Java

代码见：

[solutions/java/0011_ContainerWithMostWater.java](../../solutions/java/0011_ContainerWithMostWater.java)

## Go

代码见：

[solutions/golang/0011_container_with_most_water.go](../../solutions/golang/0011_container_with_most_water.go)

## Python

代码见：

[solutions/python/0011_container_with_most_water.py](../../solutions/python/0011_container_with_most_water.py)

## C++

代码见：

[solutions/cpp/0011_container_with_most_water.cpp](../../solutions/cpp/0011_container_with_most_water.cpp)
