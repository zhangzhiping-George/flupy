#include <stdio.h>

double balance[5] = {1000.0, 2.0, 3.4, 7.0, 50.0};
const int MAX = 4;
 
int main ()
{
   //初始化指针数组
   const char *names[] = {
                   "Zara Ali",
                   "Hina Ali",
                   "Nuha Ali",
                   "Sara Ali",
   };
   int i = 0;
 
   printf("Value of names = %s\n", *names);
   for ( i = 0; i < MAX; i++)
   {
      printf("Value of names[%d] = %s\n", i, names[i] );
   }
    for ( int i = 0; i < 6; i++)
    {
        printf("array[%d] elements: %f\n", i, balance[i]);
    }
   return 0;
}
