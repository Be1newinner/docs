Algorithm       |  Time Complexity                                         |  Space Complexity             |  Stable?  |  Use Case                                        
----------------+----------------------------------------------------------+-------------------------------+-----------+--------------------------------------------------
Bubble Sort     |  O(n2)O(n^2)O(n2)                                        |  O(1)O(1)O(1)                 |  Yes      |  Simple, small inputs                            
Selection Sort  |  O(n2)O(n^2)O(n2)                                        |  O(1)O(1)O(1)                 |  No       |  Small inputs, fewer writes                      
Insertion Sort  |  O(n2)O(n^2)O(n2)avg/worst,O(n)O(n)O(n)best              |  O(1)O(1)O(1)                 |  Yes      |  Nearly sorted data                              
Merge Sort      |  O(nlog⁡n)O(n \log n)O(nlogn)                            |  O(n)O(n)O(n)                 |  Yes      |  Large data, stable needed                       
Quicksort       |  AvgO(nlog⁡n)O(n \log n)O(nlogn), WorstO(n2)O(n^2)O(n2)  |  O(log⁡n)O(\log n)O(logn)avg  |  No       |  General purpose, fast in practice               
Heapsort        |  O(nlog⁡n)O(n \log n)O(nlogn)                            |  O(1)O(1)O(1)                 |  No       |  In-place, guaranteedO(nlog⁡n)O(n \log n)O(nlogn)
Counting Sort   |  O(n+k)O(n + k)O(n+k)                                    |  O(k)O(k)O(k)                 |  Yes      |  Small integer ranges                            
Bucket Sort     |  AvgO(n+k)O(n + k)O(n+k)                                 |  Varies                       |  Yes      |  Uniform distribution                            
Radix Sort      |  O(nk)O(nk)O(nk)                                         |  O(n+k)O(n + k)O(n+k)         |  Yes      |  Large numbers or strings                        
Quickselect     |  AvgO(n)O(n)O(n), WorstO(n2)O(n^2)O(n2)                  |  O(1)O(1)O(1)                 |  No       |  Select k-th element without full sorting        