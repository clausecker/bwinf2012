#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>

#define STAT_DAYS    10 /* days in statistical window */
#define INTRO_DAYS   10 /* Amount of days the assistant refills the can */
#define WORKER_COUNT 15 /* number of worker in the company */
#define WORKER_BITS   4 /* number of bits used by WORKER_COUNT */
#define WORKER_MASK ((1<<WORKER_BITS)-1)
#define CAN_CAPACITY 10 /* Cups per can */
#define SERVINGS      3 /* Coffee servings per worker per day */

/* data for one worker */
typedef struct {
	int cups;
	int cans;
} worker_t[STAT_DAYS];

/* data for the whole company at a given point */
typedef struct {
	double threshold;
	int day_number;
	int total_cups; /* total number of cups drunk by the workers */
	int can_state;
	worker_t workers[WORKER_COUNT];
} company_t;

/* xorshift random number generator for random number generation with good
 * statistical properties. See http://en.wikipedia.org/wiki/Xorshift */
static uint32_t xor_state[4], xor_now;
static int xor_entropy = 0;

static uint32_t xor128(int bits) {
	uint32_t t;

	/* use remaining entropy if possible */
	if (xor_entropy < bits) {
		xor_entropy = 32;
		t = xor_state[0] ^ (xor_state[1] << 11);
		xor_state[0] = xor_state[1];
		xor_state[1] = xor_state[2];
		xor_state[2] = xor_state[3];
		xor_state[3] ^= (xor_state[3] >> 19) ^ (t ^ ( t >> 8));
		xor_now = xor_state[3];
	}

	xor_entropy -= bits;
	t = xor_now & ((1<<bits)-1);
	xor_now >>= bits;
	return t;
}

/* initialize the random number generator. Return 0 on success. */
static uint32_t init_xor128(void) {
	FILE *entropy = fopen("/dev/urandom","rb");
	size_t items_read;

	if (entropy == NULL) {
		perror("Can't open /dev/random");
		return 1;
	}

	items_read = fread(xor_state,sizeof xor_state[0],4,entropy);

	fclose(entropy);

	if (items_read != sizeof(xor_state[0]*4)) {
		fprintf(stderr,"Can't initialize rng.\n");
		return 1;
	}

	return 0;
}

/* number of bits used by i. __builtin_clz is an intrisic available on gcc
 * and clang. */
static int bits(uint32_t i) {
	return 32 - __builtin_clz(i);
}

/* Generate a permuted array of pointers to members of an array of workers.
 * Algorithm taken from http://en.wikipedia.org/wiki/Fisher–Yates_shuffle */
static void shuffle_array(int out[WORKER_COUNT]) {
	int i,j;

	out[0] = 0;

	for (i = 1; i < WORKER_COUNT; i++) {
		/* get random numbers till you get one in range */
		while (j = xor128(bits(i)), j > i);
		out[i] = out[j];
		out[j] = i;
	}
}

/* Is a worker happy? */
static bool happy(worker_t *worker,double threshold) {
	int i;
	int cup_count = 0, can_count = 0;

	/* get amount of cups drunk, cans brewed */
	for (i = 0; i < STAT_DAYS; i++) cup_count += (*worker)[i].cups;
	for (i = 0; i < STAT_DAYS; i++) can_count += (*worker)[i].cans;

	/* I interprete n >= 10 as "n >= sliding window" */
	return cup_count >= STAT_DAYS && 1.0L*can_count/cup_count < threshold;
}

/* simulate one round of coffee for all workers */
static void coffee_round(company_t *company) {
	int order[WORKER_COUNT];
	int i, day_mod = company->day_number % STAT_DAYS;

	shuffle_array(order);

	for (i = 0; i < WORKER_COUNT; i++) {
		int j = order[i];
		if (!company->can_state && company->day_number >= INTRO_DAYS) {
			if (!happy(&company->workers[j],company->threshold)) continue;

			company->can_state = CAN_CAPACITY - 1;
			company->workers[j][day_mod].cans++;
		}

		company->can_state--;
		company->workers[j][day_mod].cups++;
		company->total_cups++;
	}
}

/* simulate one day of coffee */
static void day(company_t *company) {
	/* day_mod: index into the statistical tables */
	int i, day_mod = company->day_number % STAT_DAYS;

	/* zero out statistics entry for today */
	for (i = 0;i < WORKER_COUNT; i++) {
		company->workers[i][day_mod].cups = 0;
		company->workers[i][day_mod].cans = 0;
	}

	company->can_state = 0; /* empty can */

	for (i = 0;i < SERVINGS; i++) coffee_round(company);

	company->day_number++; /* A day has passed */
}

/* Main function */
int main(int argc,char **argv) {
	company_t *company;
	int day_count;

	if (argc != 3) {
		fprintf(stderr,"Usage: %s days threshold\n",argv[0]);
		return EXIT_FAILURE;
	}

	/* allocate and set to zero */
	company = calloc(sizeof *company,1);

	if (!sscanf(argv[1],"%d",&day_count) || day_count <= 0) {
		fprintf(stderr,"%s is not a valid number of days.\n",argv[1]);
		return EXIT_FAILURE;
	}

	if (!sscanf(argv[2],"%lf",&company->threshold)) {
		fprintf(stderr,"%s is not a valid threshold.\n",argv[2]);
		return EXIT_FAILURE;
	}

	if (init_xor128()) return EXIT_FAILURE;

	while (company->day_number < day_count) day(company);

	/* print output */
	printf("%.6lf\t%.6lf\n",
	  company->threshold,
	  ((double)company->total_cups/day_count)/WORKER_COUNT);

	free(company);

	return EXIT_SUCCESS;
}
