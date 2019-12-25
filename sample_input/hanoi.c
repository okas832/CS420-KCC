int dp[64];

/* Function to initialize the dp table */
void initialize(void)
{
    int i, j, k;
    /* Initialize with maximum value */
    for (i = 0; i <= 3; i += 1) {
        for (j = 1; j <= 3; j++) {
            for (k = 1; k <= 3; k += 1) {
                dp[i * 16 + j * 4 + k] = 2147483647;
            }
        }
    }
}

/* Function to return the minimum cost */
int mincost(int idx, int src, int dest, int *costs)
{
    int rem, ans, case1, case2;

    /* Base case */
    if (idx > 3)
        return 0;

    /* If problem is already solved,
       return the pre-calculated answer */
    if (dp[idx * 16 + src * 4 + dest] != 2147483647)
        return dp[idx * 16 + src * 4 + dest];

    /* Number of the auxilary disk */
    rem = 6 - (src + dest);

    /* Initialize the minimum cost as Infinity */
    ans = 2147483647;

    /* Calculationg the cost for first case */
    case1 = costs[(src - 1) * 4 + dest - 1]
        + mincost(idx + 1, src, rem, costs)
        + mincost(idx + 1, rem, dest, costs);

    /* Calculating the cost for second case */
    case2 = costs[(src - 1) * 4 + rem - 1]
        + mincost(idx + 1, src, dest, costs)
        + mincost(idx + 1, dest, src, costs)
        + costs[(rem - 1) * 4 + dest - 1]
        + mincost(idx + 1, src, dest, costs);

    /* Minimum of both the above cases */
    if (case1 < case2)
        ans = case1;
    else
        ans = case2;

    /* Store it in the dp table */
    dp[idx * 16 + src * 4 + dest] = ans;

    /* Return the minimum cost */
    return ans;
}

/* Driver code */
int main(void)
{
    int costs[16];
    costs[0 * 4 + 0] = 0, costs[0 * 4 + 1] = 1, costs[0 * 4 + 2] = 2, costs[0 * 4 + 3] = 0;
    costs[1 * 4 + 0] = 2, costs[1 * 4 + 1] = 0, costs[1 * 4 + 2] = 1, costs[1 * 4 + 3] = 0;
    costs[2 * 4 + 0] = 3, costs[2 * 4 + 1] = 2, costs[2 * 4 + 2] = 0; costs[2 * 4 + 3] = 0;
    costs[3 * 4 + 0] = 0, costs[3 * 4 + 1] = 0, costs[3 * 4 + 2] = 0; costs[3 * 4 + 3] = 0;

    printf("The standard Tower of Hanoi problem is explained here. In the standard problem, all the disc transactions are considered identical. Given a 4×4 matrix costs[16] containing the costs of transfer of disc between the rods where costs[i * 4 + j] stores the cost of transferring a disc from rod i to rod j. Cost of transfer between the same rod is 0. Hence the diagonal elements of the cost matrix are all 0s. The task is to print the minimum cost in which all the N discs are transferred from rod 1 to rod 3.\n");

    initialize();
    printf("Minimum Cost: %d\n", mincost(1, 1, 3, costs));

    return 0;
}
