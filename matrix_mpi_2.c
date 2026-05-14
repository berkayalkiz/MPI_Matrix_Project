#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
#include <cblas.h> 

int main(int argc, char** argv) {
    int rank, size, N;
    double *A = NULL, *B = NULL, *C = NULL;
    double *local_A, *local_C;
    double start_total, end_total, start_comp, end_comp;
    double t_total, t_comp;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);


    if (rank == 0) {
        int ch;
        FILE *fa = fopen("A.csv", "r");
        fscanf(fa, "%d", &N); 
        while((ch = fgetc(fa)) != '\n' && ch != EOF); 
        
        A = (double*)malloc(N * N * sizeof(double));
        for(int i = 0; i < N * N; i++) {
            fscanf(fa, "%lf", &A[i]); 
            while((ch = fgetc(fa)) == ',' || ch == ' ' || ch == '\n' || ch == '\r'); 
            if (ch != EOF) ungetc(ch, fa);
        }
        fclose(fa);

        FILE *fb = fopen("B.csv", "r");
        while ((ch = fgetc(fb)) != '\n' && ch != EOF); 
        
        B = (double*)malloc(N * N * sizeof(double));
        for(int i = 0; i < N * N; i++) {
            fscanf(fb, "%lf", &B[i]); 
            while((ch = fgetc(fb)) == ',' || ch == ' ' || ch == '\n' || ch == '\r');
            if (ch != EOF) ungetc(ch, fb);
        }
        fclose(fb);

        start_total = MPI_Wtime(); 
    }

    
    MPI_Bcast(&N, 1, MPI_INT, 0, MPI_COMM_WORLD); 
    
    if (rank != 0) {
        B = (double*)malloc(N * N * sizeof(double)); 
    }

    MPI_Bcast(B, N * N, MPI_DOUBLE, 0, MPI_COMM_WORLD); 
    int *sendcounts = (int*)malloc(size * sizeof(int));
    int *displs = (int*)malloc(size * sizeof(int));

    int kalan = N % size;
    int toplam_kaydirma = 0;
    for (int i = 0; i < size; i++) {
        int i_satir_sayisi = (N / size) + (i < kalan ? 1 : 0);
        sendcounts[i] = i_satir_sayisi * N;
        displs[i] = toplam_kaydirma;
        toplam_kaydirma += sendcounts[i];
    }

    int satir_sayisi = N / size + (rank < kalan ? 1 : 0);
    int eleman_sayisi = satir_sayisi * N;

    local_A = (double*)malloc(eleman_sayisi * sizeof(double));
    local_C = (double*)malloc(eleman_sayisi * sizeof(double));

    MPI_Scatterv(A, sendcounts, displs, MPI_DOUBLE, local_A, eleman_sayisi, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    // savunmada yapılan değişiklik burası
    if(rank == 0) {
        for(int i = 0; i < size; i++) {
            printf("rank = %d | toplam satir %d | baslangic satir %d | bitis satir %d\n",i, sendcounts[i]/N, displs[i]/N, (displs[i]+sendcounts[i])/N);
        }
    }
    

    start_comp = MPI_Wtime();
    
    // cblas_dgemm: C = alpha * A * B + beta * C
    cblas_dgemm(CblasRowMajor, CblasNoTrans, CblasNoTrans, 
                satir_sayisi, N, N, 
                1.0, local_A, N, B, N, 
                0.0, local_C, N);
                
    end_comp = MPI_Wtime();
    t_comp = end_comp - start_comp;


    if (rank == 0) {
        C = (double*)malloc(N * N * sizeof(double));
    }

    MPI_Gatherv(local_C, eleman_sayisi, MPI_DOUBLE, C, sendcounts, displs, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    
    if (rank == 0) { // bundan sonrası json kaydetme muhabbeti
        end_total = MPI_Wtime();
        t_total = end_total - start_total;

        printf("Dil: C | N=%d | P=%d test edildi. Toplam Sure: %f sn | Saf Hesaplama: %f sn\n", N, size, t_total, t_comp);

        char cmd[256];
        snprintf(cmd, sizeof(cmd), "python3 update_json.py i5-10400 C %d %d %f %f", N, size, t_total, t_comp);
        system(cmd);

        free(A); free(C);
    }

    free(B); free(local_A); free(local_C);
    free(sendcounts); free(displs);
    MPI_Finalize();
    return 0;
}