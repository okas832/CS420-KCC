int v1=1, v2=7/3;
float i2f = 5;
int f2i = 5.678;
char ch = 'A';
char multi_cast = ('A' - 1 * 2 / (123 % 4) & 0x12 | 0x34 ^ 0x56 + (1 << 2) + (345 >> 6) + (1 && 2) - (3 || 4)) + 2.3;
int arr[2], *ptr1, **ptr2, *ptr_arr[123], arr2[10];

int a(void) {
    int expr_many_cast = (2, 3.4);
    return (2, 3.4);
}
int b() {}
int c(void) { }
int d(int arg1, float *arg2)
{
    arg1++;
    *arg2 = 2.3;

    return 0;
}
int e(int *arg1, int arg2[10]) { }
void ret_void() { }
int *ret_iptr() { }

int main(void)
{
    int *arr_ptr = arr;  // cast int[2] to *int
    int a=1, b, c=a;
    float f;
    void *vptr, **vdptr;
    a = f = c = 1;
    for (a = 0; a < b; a++, --b)
        if (a < b)
            break;
        else if (a > b)
            continue;
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

    e(&a, ptr1);
    e(&a, arr);
    e(&v2, arr2);

    printf("abcde\n");
    printf("%d\n", a);
    printf("%f\n", f);
    printf("%d\n", f);  // no type conversion @ AST_TYPE, intended behaviour

    ret_void();

    a = (f > b) + c;

    a = *arr;
    vptr = *vdptr;
    vptr = *vdptr++;
    a = ret_iptr()[0];
    ptr1 = &a + (&b - &c);
    ptr1 = arr + a + (&b - arr);

    arr[ch];
    arr_ptr[ch];
}