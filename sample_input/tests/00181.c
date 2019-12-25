int A[4], B[4], C[4];

/* Print the current configuration of A, B, and C to the screen */
void PrintAll(void)
{
    int i;

    printf("A: ");
    for(i=0;i<4;i++)printf(" %d ",A[i]);
    printf("\n");

    printf("B: ");
    for(i=0;i<4;i++)printf(" %d ",B[i]);
    printf("\n");

    printf("C: ");
    for(i=0;i<4;i++)printf(" %d ",C[i]);
    printf("\n");
    printf("------------------------------------------\n");
    return;
}

/* Move the leftmost nonzero element of source to dest, leave behind 0. */
/* Returns the value moved (not used.) */
int Move(int *source, int *dest)
{
    int i = 0, j = 0;

    while (i<4 && (source[i])==0) i++;
    while (j<4 && (dest[j])==0) j++;

    dest[j-1] = source[i];
    source[i] = 0;
    PrintAll();       /* Print configuration after each move. */
    return dest[j-1];
}


/* Moves first n nonzero numbers from source to dest using the rules of Hanoi.
   Calls itself recursively.
   */
void Hanoi(int n,int *source, int *dest, int *spare)
{
    int i;
    if(n==1){
        Move(source,dest);
        return;
    }

    Hanoi(n-1,source,spare,dest);
    Move(source,dest);
    Hanoi(n-1,spare,dest,source);
    return;
}

int main()
{
    int i;

    /* initialize the towers */
    for(i=0;i<4;i++)A[i]=i+1;
    for(i=0;i<4;i++)B[i]=0;
    for(i=0;i<4;i++)C[i]=0;

    printf("Solution of Tower of Hanoi Problem with %d Disks\n\n",4);

    /* Print the starting state */
    printf("Starting state:\n");
    PrintAll();
    printf("\n\nSubsequent states:\n\n");

    /* Do it! Use A = Source, B = Destination, C = Spare */
    Hanoi(4,A,B,C);

    return 0;
}
