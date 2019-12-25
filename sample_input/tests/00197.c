int fred = 1234;
int joe;

void henry(void)
{
    int fred = 4567;

    printf("%d\n", fred);
    fred++;
}

int main(void)
{
    printf("%d\n", fred);
    henry();
    henry();
    henry();
    henry();
    printf("%d\n", fred);
    fred = 8901;
    joe = 2345;
    printf("%d\n", fred);
    printf("%d\n", joe);

    return 0;
}
