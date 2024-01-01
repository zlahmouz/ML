// N nombre de pixels de l'image
int N = get_image_size(filename);
 // variables MPI
  int my_rank, size;

// allocation de la mémoire pour contenir l'image
// variable pixels : tableau de 3*N octets (3 octets par pixels, RVB)
char *pixels = allocate_image(N);

// Initialisation de MPI
  MPI_Init(NULL, NULL);

  // Récupération des informations MPI
  MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);
  MPI_Comm_size(MPI_COMM_WORLD, &size);

// lecture de l'image
 read_image(pixels, N, filename);
MPI_Scatter(pixels,N,MPI_INT,pixels_loc,N/size,MPI_INT,0,MPI_COMM_WORLD);



        // tableau lumi contenant la luminance de chaque pixel
    // (valeur entre 0 et 255 => tableau d'entiers de taille N)
    int *lumi_loc = allocate_lumi(N/size);

    // calcul de la luminance -> complexité : 1 calcul par pixel
    compute_luminance(lumi_loc, pixels_loc, N/size);

    // tableau histo de taille 256 qui compte le nombre de pixels
    // ayant la luminance correspondante
    int *histo_loc = allocate_histo(256);

    // calcul de l'histogramme -> complexité : 1 calcul par pixel
    compute_histo(histo_loc, lumi_loc, N/size);

    // Équilibrage de l'image d'origine en utilisant l'histogramme :
    // on crée une nouvelle image -> complexité : 1 calcul par pixel
    // la saturation (nombre de pixels ayant la valeur 0 ou la valeur 255)
    // est aussi calculée
    char *new_pixels_loc = allocate_image(N/size);
    int saturation;

    equalize(new_pixels_loc, &saturation, pixels_loc, histo_loc, N/size);

    MPI_Allgather(new_pixels_loc,N/size,MPI_INT,new_pixels_global,N/size,MPI_INT,MPI_COMM_WORLD)




// sauvegarde de l'image égalisée
save_image(new_pixels, N, filename2);

// affichage de la saturation
printf("la saturation est de %d\n", saturation)

MPI_Finalize();