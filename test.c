#include<stdio.h>
#include<math.h>
#include<time.h>

#define MAX 100000
#define range 3

void read_arq(char name_in[100], double coord[4][MAX], int lens[2], int *len)
{
    FILE *csv;
	csv = fopen(name_in, "r");

	fscanf(csv, "(%d, %d)\n", &lens[0], &lens[1]);
	printf("Catalogs len: %d and %d\n", lens[0], lens[1]);

	if (lens[0] >= lens[1])
	    *len = lens[0];
	else
	    *len = lens[1];

    for (int i = 0; i < *len; i++)
    {
        fscanf(csv, "(%lf, %lf, %lf, %lf)\n", &coord[0][i], &coord[1][i], &coord[2][i], &coord[3][i]);
	    //printf("%.15lf %.15lf %.15lf %.15lf\n", coord[0][i], coord[1][i], coord[2][i], coord[3][i]);
	}
}

double return_module(double n, double m, double x, double y, double threshold)
{
    threshold = threshold / (60*60);
    double module = sqrt(pow((n-x), 2) + pow((m-y), 2));

    return module;
}

int check_equal(double n, double m, double x, double y, double threshold)
{
    threshold = threshold / (60*60);
    double module = sqrt(pow((n-x), 2) + pow((m-y), 2));

    if (module <= threshold)
        return 1;
    else
        return 0;
}

int cross_match(int index[2][MAX], double coord[4][MAX], int lens[2], int *len)
{
    int count = 0;
    for (int i=0; i<lens[0]; i++)
    {
        int j_list[MAX];
        int n = 0;

        for (int j=0; j<lens[1]; j++)
        {
            int equal = check_equal(coord[0][i], coord[1][i], coord[2][j], coord[3][j], range);
            if (equal == 1)
            {
                j_list[n] = j;
                n++;
            }
        }
        if (n != 0)
        {
            double value, smaller;
            int ind_smaller = j_list[0];
            smaller = return_module(coord[0][i], coord[1][i], coord[2][j_list[0]], coord[3][j_list[0]], range);
            for (int j=1; j<n; j++)
            {
                value = return_module(coord[0][i], coord[1][i], coord[2][j_list[j]], coord[3][j_list[j]], range);
                if (value < smaller)
                    smaller = value;
                    ind_smaller = j_list[j];
            }
            index[0][count] = i+1;
            index[1][count] = ind_smaller+1;
            count++;
        }
        float load = ((i+1.)/lens[0])*100;
    //    printf("Load: %f\n", load);
    }
    printf("Found %d objects\n", count);
    return count;
}

void save_arq(char name_out[100], int index[2][MAX], int founded)
{
    FILE *csv_write;
    csv_write = fopen(name_out, "w");

    for (int i=0; i<founded; i++)
        fprintf(csv_write, "%d, %d\n", index[0][i], index[1][i]);
}

int main()
{
    clock_t begin = clock();

    char name_in[100] = "entrada.csv";
    char name_out[100] = "saida.csv";
    double coord[4][MAX];
    int lens[2], len, index[2][MAX];

    read_arq(name_in, coord, lens, &len);
    int founded = cross_match(index, coord, lens, &len);
    save_arq(name_out, index, founded);

    clock_t end = clock();
    double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
    printf("Time C: %f\n", time_spent);

    return 0;
}
