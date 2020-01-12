/////////////////////////////////////////////////////
// Cross-Match Fits Catalog                        //
// Matheus J. Castro                               //
// Version 6.5                                     //
// Last Modification: 01/12/2020 (month/day/year)  //
/////////////////////////////////////////////////////

#include<stdio.h>
#include<math.h>
#include<time.h>

#define MAX 100000 // The maximum of objects that a catalog can contain.
#define range 3 // In arcseconds, the threshold that two objects can be considered the same.

void changedot(char name_in[100], char name_in_mod[100])
{
    // Function to change de csv file with the cross-matchs numbers.
    // It change the dots "." to commas ",".

    FILE *file; // Main file.
    FILE *new_file; // Modified file.

    char c;
    file = fopen(name_in, "r"); // Open the file in read mode.
    new_file = fopen(name_in_mod, "w"); // Create the new file in write mode.

    while ((c = getc(file)) != EOF) // When the file end, stop.
    {
        // Read character by character
        if (c == '.')
            c = ',';
        fprintf(new_file, "%c", c); // Write in the new file.
        //putchar(c); // Print a single character.
    }

    // Close both files.
    fclose(file);
    fclose(new_file);
}

void read_arq(char name_in_mod[100], double coord[4][MAX], int lens[2], int *len)
{
    // Read the csv file and set the variables in the right format.
    FILE *csv;
	csv = fopen(name_in_mod, "r"); // Open CSV.

	fscanf(csv, "(%d, %d)\n", &lens[0], &lens[1]); // Read the first line, the header of CSV that contain the number of objects in each catalog.
	printf("Catalogs len: %d and %d\n", lens[0], lens[1]);

	if (lens[0] >= lens[1]) // Verify witch catalog is bigger.
	    *len = lens[0];
	else
	    *len = lens[1];

    for (int i = 0; i < *len ; i++) // Read until the last line.
    {
        fscanf(csv, "(%lf, %lf, %lf, %lf)\n", &coord[0][i], &coord[1][i], &coord[2][i], &coord[3][i]); // Create the matrix of catalogs.
	    //printf("%.15lf %.15lf %.15lf %.15lf\n", coord[0][i], coord[1][i], coord[2][i], coord[3][i]);
	}
}

double return_module(double n, double m, double x, double y)
{
    // Return the module of distance of two points in a two dimensional space.
    double module = sqrt(pow((n-x), 2) + pow((m-y), 2));

    return module;
}

int check_equal(double n, double m, double x, double y, double threshold)
{
    // Check if two points have the module of distance inside a circle with a radius set in threshold variable.
    threshold = threshold / (60*60); // Transform arcsencods in degress.
    double module = sqrt(pow((n-x), 2) + pow((m-y), 2));

    if (module <= threshold)
        return 1; // Return 1 if it's inside.
    else
        return 0; // Return 0 if it's outside.
}

int cross_match(int index[2][MAX], double coord[4][MAX], int lens[2], int *len)
{
    // Do the cross-match of the catalogs.
    int count = 0;
    for (int i=0; i<lens[0]; i++)
    {
        int j_list[MAX];
        int n = 0;

        for (int j=0; j<lens[1]; j++) // Check every point in the catalog 1 that can fit inside the threshold circle for the given point in catalog 0.
        {
            int equal = check_equal(coord[0][i], coord[1][i], coord[2][j], coord[3][j], range);
            if (equal == 1)
            {
                j_list[n] = j; // Create a list of the index (of the table) of all points (j) of catalog 1 that fit in the given point (i) of catalog 0.
                n++;
            }
        }
        if (n != 0) // If the given point (i) of catalog 0 has equivalent points (j_list) in catalog 1, check witch one is the closest one.
        {
            double value, smaller;
            int ind_smaller = j_list[0]; // Set the first point as the closest one.
                                         // ind means index.
            smaller = return_module(coord[0][i], coord[1][i], coord[2][j_list[0]], coord[3][j_list[0]]); // Take the module of distance of the first point.
            for (int j=1; j<n; j++) // If the j_list has more than one point, check witch one is the smaller one.
            {
                value = return_module(coord[0][i], coord[1][i], coord[2][j_list[j]], coord[3][j_list[j]]);
                if (value < smaller)
                    smaller = value;
                    ind_smaller = j_list[j]; // Set the index for the closest point.
            }
            index[0][count] = i+1; // Save the index of catalog 0 of the object i.
            index[1][count] = ind_smaller+1; // Then save the index for the same object as the previous line but now referring the catalog 1 (ind_smaller).
            count++; // Count how much cross-matched objects were found.
        }
    //    float load = ((i+1.)/lens[0])*100; // The percent of the progress of the process.
    //    printf("Load: %f\n", load);
    }
    printf("Found %d objects\n", count);
    return count;
}

void save_arq(char name_out[100], int index[2][MAX], int founded)
{
    // Save the cross-matched objects in a csv file.
    FILE *csv_write;
    csv_write = fopen(name_out, "w"); // Create the file in write mode.

    for (int i=0; i<founded; i++) // Write until reaches the number of founded cross-matches.
        fprintf(csv_write, "%d, %d\n", index[0][i], index[1][i]);

    // Close the file.
    fclose(csv_write);
}

int py_script()
{
    // Call this function as you main function if you want to change the dots of the entrada.csv file.
    // If it's not what you want, call the normal main function.
    clock_t begin = clock();

    char name_in[100] = ".entrada.csv";
    char name_in_mod[100] = ".entrada_mod.csv";
    char name_out[100] = ".saida.csv";
    double coord[4][MAX];
    int lens[2], len, index[2][MAX];
    // The file entrada.csv contain four columns where the first two are the position of each object in the catalog 0,
    // and the others two columns are the position of each object in the catalog 1.
    // The file saida.csv will contain only the index in entrada.csv of catalog 0 and 1 that is a cross-match.
    // coord is the matrix that will contain all the positions of all objects in two catalogs using the same logic as the file entrada.csv.
    // index is the matrix that will contain the cross-match index whit the two catalogs in the table entrada.csv.

    changedot(name_in, name_in_mod);
    read_arq(name_in_mod, coord, lens, &len);
    int founded = cross_match(index, coord, lens, &len);
    save_arq(name_out, index, founded);

    clock_t end = clock();
    double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
    printf("Time C: %f\n", time_spent);

    return 0;
}

int main()
{
    // This is your main function only if you don't want to change the dots of entrada.csv file.
    // If you want to change it, use the py_script function as your main function.
    // Check the changedot function for more details.
    clock_t begin = clock();

    char name_in_mod[100] = ".entrada.csv";
    char name_out[100] = ".saida.csv";
    double coord[4][MAX];
    int lens[2], len, index[2][MAX];
    // The file entrada.csv contain four columns where the first two are the position of each object in the catalog 0,
    // and the others two columns are the position of each object in the catalog 1.
    // The file saida.csv will contain only the index in entrada.csv of catalog 0 and 1 that is a cross-match.
    // coord is the matrix that will contain all the positions of all objects in two catalogs using the same logic as the file entrada.csv.
    // index is the matrix that will contain the cross-match index whit the two catalogs in the table entrada.csv.

    read_arq(name_in_mod, coord, lens, &len);
    int founded = cross_match(index, coord, lens, &len);
    save_arq(name_out, index, founded);

    clock_t end = clock();
    double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
    printf("Time C: %f\n", time_spent);

    return 0;
}
