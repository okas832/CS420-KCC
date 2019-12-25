int main(void)
{
    int i, len, j, k;
    char *t[3], l;
    char *tmp;
    char buf[2];

    t[0] = "kanglib";
    t[1] = "ironore15";
    t[2] = "cxion";

    for (i = 0; i < 3; i++)
    {
        tmp = t[i];
        len = 0;
        while (tmp[len] != 0)
        {
            len++;
        }
        for (j = 0; j < len; j++)
        {
            for (k = j + 1; k < len; k++)
            {
                if (tmp[j] == tmp[k])
                {
                    printf("Conflicting characters at ");
                    buf[0] = tmp[j];
                    buf[1] = 0;
                    printf(buf);
                    printf(" (%d) and ", j);
                    buf[0] = tmp[k];
                    buf[1] = 0;
                    printf(buf);
                    printf(" (%d) in ", k);
                    printf(tmp);
                    printf("\n");
                }
            }
        }
    }
}
