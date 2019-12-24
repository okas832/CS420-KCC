int main(void)
{
    int a[6], *pi, *pj;
    a[0] = 1, a[1] = 4, a[2] = 2, a[3] = 8, a[4] = 5, a[5] = 7;

    for (pi = a; pi < &a[6]; pi++)
    {
        for (pj = pi + 1; &a[6] - pj > 0; pj++)
        {
            if (*pi > *pj)
            {
                int tmp = *pi;
                *pi = *pj;
                *pj = tmp;
            }
        }
    }

    for (pi = a + 6; pi > &a[0]; 0)
    {
        printf("%d\n", *--pi);
    }

    return 0;
}