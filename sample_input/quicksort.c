/* This function takes last element as pivot, places
   the pivot element at its correct position in sorted
    array, and places all smaller (smaller than pivot)
   to left of pivot and all greater elements to right
   of pivot */
int partition(int *arr, int low, int high)
{
    /* pivot (Element to be placed at right position) */
    int pivot = arr[high];
    int i = low - 1, j, tmp;

    for (j = low; j <= high - 1; j++)
    {
        /* If current element is smaller than the pivot */
        if (arr[j] < pivot)
        {
            i++;    /* increment index of smaller element */
            tmp = arr[i];
            arr[i] = arr[j];
            arr[j] = tmp;
        }
    }
    tmp = arr[i + 1];
    arr[i + 1] = arr[high];
    arr[high] = tmp;
    return i + 1;
}

/* low  --> Starting index,  high  --> Ending index */
void quickSort(int *arr, int low, int high)
{
    if (low < high)
    {
        /* pi is partitioning index, arr[pi] is now
           at right place */
        int pi = partition(arr, low, high);

        quickSort(arr, low, pi - 1);  /* Before pi */
        quickSort(arr, pi + 1, high); /* After pi */
    }
}

void printArray(int *arr, int length)
{
    int i;

    printf("[");
    if (length >= 1) printf("%d", arr[0]);

    for (i = 1; i < length; i++)
    {
        printf(", %d", arr[i]);
    }
    printf("]\n");
}

int main(void)
{
    int arr[7];
    arr[0] = 10, arr[1] = 80, arr[2] = 30, arr[3] = 90, arr[4] = 40, arr[5] = 50, arr[6] = 70;

    printArray(arr, 7);
    quickSort(arr, 0, 6);
    printArray(arr, 7);
    return 0;
}
