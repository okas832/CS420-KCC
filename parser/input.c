int v1=1, v2=1;
float i2f = 5;
int f2i = 5.678;
char ch = 'A';
char multi_cast = (4 - 1 * 2 / (123 % 4) & 0x12 | 0x34 ^ 0x56 + (1 << 2) + (345 >> 6) + (1 && 2) - (3 || 4)) + 2.3;
int arr[2], *ptr1, **ptr2, *ptr_arr[123];

int a(void) {
    ;

    ;
}
int b() {}
int c(void) { }
int d(int arg1, float *arg2)
{
    arg1++;
    *arg2 = 2.3;
}

int main(void)
{
    int a, b, c;
    float f;
    for (a = 0; a < b; a++, --b)
        if (a < b)
            0;
        else if (a > b)
            1;
        else
            d(5, &f);
    
    if (a /*this is some
    comment*/)
        if (b)
            b; // this is another comment // //
        else
            a;
    
    c = 1;
    c *= 2.3;
}