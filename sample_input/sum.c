float sum(int length, int *value){
	int i;
	float total;
	total = 0;

	for(i = 0; i < length; i++){
		total = total + value[i];
	}

	return total;
}

int main(void){
	int count, i;
	int record[10];
	float total;

	count = 10;
	total = 0;
	
	printf("record :");

	for(i = 0; i < count; i++) {
		record[i] = i;
		printf(" %d", record[i]);
	}

	printf("\n\nCalculating...\n");

	for(i = 1; i <= count; i++) {
		total = sum(i, record);
		printf("%f\n", total);
	}

	printf("Done!\n");

}