#include <iostream>
using namespace std;

int factorial(int n)
{
    if (n < 0)
        return -1;
    if (n > 1)
        return n * factorial(n - 1);
    else
        return 1;
}

int main()
{
    int num = -1;

    cout << factorial(num) << endl;
    return 0;
}