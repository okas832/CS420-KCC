int some(char *s)
{
    if (s[0] == 0)
        return 0;
    else
    {
        some(&s[1]);
        printf(s);
        printf("\n");
    }
}

int main(void)
{
    char *s = "Very Long Sentence";

    some(s);
    return 0;
}
