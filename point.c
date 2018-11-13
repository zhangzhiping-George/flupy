#include <stdio.h>

int main()
{
    int var = 20;
    int *ip;
    ip = &var;
    int *np = NULL;
    printf("add of var: %p\n",  &var);
    printf("add stored in ip of var: %p\n",  ip);
    printf("var of *ip of var: %d\n",  *ip);
    printf("addr of null point: %p\n",  np);
    if(np)
    {
        printf("null point is true");
    }
    else
    {
        printf("null point is false\n");
    }
    return 0;
}
