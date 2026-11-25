#include <errno.h>
#include <limits.h>
#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum { POINTS = 4096, RANKS = 4, LOCAL_POINTS = POINTS / RANKS };
static const double diffusion = 0.25;

static int write_csv(const char *path, const double temperatures[POINTS])
{
    FILE *file = fopen(path, "w");
    if (!file) {
        perror(path);
        return EXIT_FAILURE;
    }

    fprintf(file, "position,temperature\n");
    for (int i = 0; i < POINTS; ++i) {
        fprintf(file, "%d,%.17g\n", i, temperatures[i]);
    }
    const int write_failed = ferror(file);
    if (fclose(file) == EOF || write_failed) {
        fprintf(stderr, "Could not write %s\n", path);
        return EXIT_FAILURE;
    }
    return EXIT_SUCCESS;
}

int main(int argc, char **argv)
{
    MPI_Init(&argc, &argv);
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    char *end = NULL;
    errno = 0;
    const long steps = argc >= 3 ? strtol(argv[1], &end, 10) : 0;
    const int boundary_check = argc == 4 && strcmp(argv[3], "--boundary-check") == 0;
    if ((argc != 3 && !boundary_check) || errno || !end || *end ||
        steps < 1 || steps > INT_MAX || size != RANKS) {
        if (rank == 0) {
            fprintf(stderr, "Usage: mpirun -n 4 ./heat STEPS OUTPUT.csv [--boundary-check]\n");
        }
        MPI_Finalize();
        return EXIT_FAILURE;
    }

    double first[LOCAL_POINTS + 2] = {0};
    double second[LOCAL_POINTS + 2] = {0};
    double *current = first;
    double *next = second;
    if (rank == 0) {
        current[1] = 100.0;
        if (boundary_check) current[LOCAL_POINTS] = 100.0;
    }
    const int left = rank == 0 ? MPI_PROC_NULL : rank - 1;
    const int right = rank == size - 1 ? MPI_PROC_NULL : rank + 1;

    for (int step = 0; step < steps; ++step) {
        MPI_Sendrecv(&current[1], 1, MPI_DOUBLE, left, 0,
                     &current[LOCAL_POINTS + 1], 1, MPI_DOUBLE, right, 0,
                     MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        MPI_Sendrecv(&current[LOCAL_POINTS], 1, MPI_DOUBLE, right, 1,
                     &current[0], 1, MPI_DOUBLE, left, 1,
                     MPI_COMM_WORLD, MPI_STATUS_IGNORE);

        const int start = rank == 0 ? 2 : 1;
        const int stop = rank == size - 1 ? LOCAL_POINTS - 1 : LOCAL_POINTS;
        for (int i = start; i <= stop; ++i) {
            next[i] = current[i] + diffusion * (current[i - 1] - 2.0 * current[i] + current[i + 1]);
        }
        if (rank == 0) next[1] = 100.0;

        double *previous = current;
        current = next;
        next = previous;
    }

    double temperatures[POINTS];
    MPI_Gather(&current[1], LOCAL_POINTS, MPI_DOUBLE,
               temperatures, LOCAL_POINTS, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    int result = EXIT_SUCCESS;
    if (rank == 0) {
        result = write_csv(argv[2], temperatures);
        if (result == EXIT_SUCCESS) {
            printf("Rank 0 gathered %d points from %d ranks after %ld steps -> %s\n",
                   POINTS, size, steps, argv[2]);
        }
    }
    MPI_Bcast(&result, 1, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Finalize();
    return result;
}
