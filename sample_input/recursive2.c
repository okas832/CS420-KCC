int is_even(int n) {
    if (n == 0)
        return 1;
    else
        return is_odd(n - 1);
}

int is_odd(int n) {
    if (n == 0)
        return 0;
    else
        return is_even(n - 1);
}

int main(void)
{
    printf("%d is ", 76);
    if (is_even(76))
    {
        printf("even.\n");
    }
    else if (is_odd(76))
    {
        printf("odd.\n");
    }
    else
    {
        printf("Holy Shiiiiit.\n");
    }
    return 0;
}
