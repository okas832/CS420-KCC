void memcpy(char *dest, char *src, int len)
{
    int i;
    for (i = 0; i < len; i++)
    {
        dest[i] = src[i];
    }
    return;
}

int main(void)
{
    char *str = "Hello, Universe!\n";
    int len;
    char *a, *b;

    for (len = 0; str[len] != 0; len++) ;

    a = malloc(len + 1);
    memcpy(a, str, len);
    a[len] = 0;
    printf(a);

    b = malloc(len + 1);
    memcpy(b, a, len);
    b[len] = 0;

    free(a);

    printf(b);
    return 0;
}
