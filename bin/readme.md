## 文件结构

* src
  * sort.py
* bin
  * requirement.txt
  * readme.md
* report.pdf
* hw5.pdf

### 各个文件的作用

sort.py 实现了各种排序算法

使用方式为 python sort.py <number of data>  <choose of algorithm>

例如 python sort.py 10000  0 将会使用插入排序对随机生成的10000个数据进行排序，输出所用的时间

0到5 分别代表insertsort, shellsort, quicksort, mergesort, radixsort, timsort

hw5.pdf 是证明题

report.pdf 是实验报告

requirement.txt 是依赖的库，为空（没有使用除了内置库的其他第三方库）