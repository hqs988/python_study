#序列都可以进行的操作包括索引，切片，加，乘，检查成员。


# ------------------------------------------------------------------------------------------------------
# 创建一个列表，只要把逗号分隔的不同的数据项使用方括号括起来即可
# ------------------------------------------------------------------------------------------------------

# 字符串型
list1 = ['one', 'two']
print(list1)


# 整型
list2 = [1, 2, 3]
print(list2)
print(list2[0])

# ------------------------------------------------------------------------------------------------------
# 访问列表中的值
# ------------------------------------------------------------------------------------------------------
list3 = [1, 2, 3, 4, 5, 6, 7]
print(list3[1])
print(list3[1:5])

# ------------------------------------------------------------------------------------------------------
# 更新列表中的值
# ------------------------------------------------------------------------------------------------------
list4 = []
list4.append("china")
list4.append(1)          # 列出中的元素的值的类型可以不同
print(list4)
list4[0] = "love"
print(list4)             # 修改指定元素


# ------------------------------------------------------------------------------------------------------
# 更新列表中的值
# ------------------------------------------------------------------------------------------------------
print("\n# debug list 5")
list5 = [1, 2, 3, "china", 4, 5, "love"]
print(list5)
del list5[1]
print(list5)
del list5[2]
print(list5)


# ------------------------------------------------------------------------------------------------------
# Python列表脚本操作符   +/组合  */重复 len()/求长度   in/遍历查找  for/迭代
# ------------------------------------------------------------------------------------------------------
print("\n# debug list 6/7")
list6 = [1, 2, 3, 4, 5, "china"]
len(list6)
print(len(list6))  # len()/求长度

list7 = [8, 9, 10]

print(list6+list7)  # +/组合

print(list7 * 2)    # */重复


print(3 in list6)
print(3 in list7)

# ------------------------------------------------------------------------------------------------------
# Python列表截取
# ------------------------------------------------------------------------------------------------------
print("\n# debug list 8")

list8 = ["google", "yahoo", "facebook", "tomcat", "hw", "tom", "hello"]
print(list8[2])      # 从左开始数, 打印列表第3个元素, 从左时，以0开始
print(list8[-2])     # 从右开始数, 打印列表第2个元素，从右向左时，以1开始
print(list8[2:-2])   # 左边开始， 第三个，包含第三个， 至右边开始第2个，不含第2个
print(list8[1:-1])



