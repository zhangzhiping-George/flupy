#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main()
{
    char name[100] = "George";
    char *desc = NULL;

    //strcpy(name, "George");
    desc = calloc(30, sizeof(char));
    //desc = alloc(30*sizeof(char));
    if(desc == NULL)
    {
        fprintf(stderr, "Error - unable to allocate required memory\n");
    }
    else
    {
        strcpy(desc, "asjdflasdjfkasdfasd");
    }
    printf("Name: %s\n", name);
    printf("Desc: %s\n", desc);
}
