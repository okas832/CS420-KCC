void charfunc(char a)
{
    printf("char: %d\n", a);
}

void intfunc(int a)
{
    printf("int: %d\n", a);
}

void floatfunc(float a)
{
    printf("float: %f\n", a);
}

int main(void)
{
    char b, c;
    int d, e;
    float f, g;

    charfunc('a');
    charfunc(98);
    charfunc(99.0);

    intfunc('a');
    intfunc(98);
    intfunc(99.0);

    floatfunc('a');
    floatfunc(98);
    floatfunc(99.0);

    /* printf("%c %d %f\n", 'a', 'b', 'c'); */
    /* printf("%c %d %f\n", 97, 98, 99); */
    /* printf("%c %d %f\n", 97.0, 98.0, 99.0); */

    b = 97;
    c = 97.0;

    printf("%d %d\n", b, c);

    d = 'a';
    e = 97.0;

    printf("%d %d\n", d, e);

    f = 'a';
    g = 97;

    printf("%f %f\n", f, g);

    return 0;
}
