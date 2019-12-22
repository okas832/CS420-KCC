int gcd(int a, int b){
	int big, small, rem;
	
	big = a;
	small = b;

	if(b > a){
		big = b;
		small = a;
	}

	for(rem = big % small; rem>0; rem = big % small){
		big = small;
		small = rem;
	}
	
	return small;
}

int main(void){
	int a, b, c, d;
	int result;

	a = 15;
	b = 7;
	c = 10;
	d = 3;

	printf("gcd of 15 and 7 : ");
	result = gcd(a, b);
	printf("%d\n", result);

	printf("gcd of 15 and 10 : ");
	result = gcd(a, c);
	printf("%d\n", result);

	printf("gcd of 15 and 3 : ");
	result = gcd(a, d);
	printf("%d\n", result);
}