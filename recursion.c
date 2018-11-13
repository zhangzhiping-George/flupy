#include <stdio.h>

/*int factorial(int n)
{
    if(n<=1)
        return 1;
    else
        return n*factorial(n-1);
}

int main()
{
    int n = 10;
    int fac = factorial(n);
    printf("%d factorial value is %d\n", n, fac);
    return 0;
}*/

int fib(int n)
{
    if (n==0)
    {
        return 0;
    }
    else if (n==1)
    {
        return 1;
    }
    else
    {
        return fib(n-1)+fib(n-2);
    }
}

int main()
{
    for (int i=0; i<=15; i++)
    {
        printf("fib(%d) is: %d\n", i, fib(i));
    }
}
