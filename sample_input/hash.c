int c_hash(char *str, int p)
{
    int hash = 0, i, len = 0;

    while (str[len] != 0)
    {
        len++;
    }

    for (i = len - 1; i >= 0; i--)
    {
        hash *= p;
        hash += str[i];
    }
    return hash;
}

int main(void)
{
    int i, len, j, k;
    char *t[3];
    char *tmp;

    t[0] = "kanglib";
    t[1] = "ironore15";
    t[2] = "cxion";

    for (i = 0; i < 3; i++)
    {
        printf("Hash of ");
        printf(t[i]);
        printf(": ");
        printf("%d\n", c_hash(t[i], 13));
    }

    return 0;
}
