#include <stdio.h>

int max(int x, int y)
{
   return x > y ? x:y;
}

int main()
{
    int (* p)(int x, int y) = &max;
    int a, b, c, d;
    printf("input three num: \n");
    scanf("%d %d %d", &a, &b, &c);
    d = p(p(a, b), c);
    printf("max num is %d\n", d);
    return 0;
}
