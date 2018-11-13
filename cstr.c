#include <stdio.h>

int main()
{
    char greeting[6] = {'h', 'e', 'l', 'l', 'o', '\0'};
    char cstr[4] = "abcd";
    printf("greeting str: %s\n", greeting);
    printf("c str: %s\n", cstr);
    return 0;
}
