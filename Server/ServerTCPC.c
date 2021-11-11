#include <stdlib.h>
#include <stdio.h>

#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <string.h>

#define CHECK_ERROR(val1, val2, msg) if(val1 == val2) {perror(msg); exit(1);}
#define MAXCAR 20

int main() {
    int sockServerPy, sockServerC;
    int sockClientC;
    char bufferCommunication[MAXCAR + 1];

    struct sockaddr_in addrServerC, addrClientC, addrServerPy;
    int lengthAddr = sizeof(addrClientC);

    //--------------------------------------------------------------------------------------------------
    //---------------------------------------Connecting Socket------------------------------------------
    //--------------------------------------------------------------------------------------------------

    printf("Connecting to the socket...\n");

    sockServerC = socket(AF_INET, SOCK_STREAM, 0);
   
    addrServerC.sin_family = AF_INET;
    addrServerC.sin_port = htons(600);
    addrServerC.sin_addr.s_addr = INADDR_ANY;

    CHECK_ERROR(bind(sockServerC, (struct sockaddr*) &addrServerC, sizeof(addrServerC)), -1, "Erreur de liaison 1\n");

    printf("Socket connected\n");

    //--------------------------------------------------------------------------------------------------
    //-------------------------------------Waiting for clients------------------------------------------
    //--------------------------------------------------------------------------------------------------

    printf("Waiting for clients...\n");

    while (1) {

        listen(sockServerC, 5);
        sockClientC = accept(sockServerC, (struct sockaddr *) &addrClientC, &lengthAddr);

        printf("Client Connected\n");

        int pc = fork();

        if (pc == 0) {
            close(sockServerC);

            read(sockClientC, bufferCommunication, MAXCAR + 1);

            //--------------------------------------------------------------------------------------------------
            //------------------------------------Connecting to Server Py---------------------------------------
            //--------------------------------------------------------------------------------------------------

            printf("Connecting Client to Server Py\n");

            sockServerPy = socket(AF_INET, SOCK_STREAM, 0);

            addrServerPy.sin_family = AF_INET;
            addrServerPy.sin_port = htons(500);
            addrServerPy.sin_addr.s_addr = inet_addr("127.0.0.1");

            connect(sockServerPy, (const struct sockaddr *) &addrServerPy, sizeof(addrServerPy));

            printf("Server connected\n");

            strcpy(bufferCommunication, inet_ntoa(addrClientC.sin_addr));
            write(sockServerPy, bufferCommunication, strlen(bufferCommunication));
            bzero(bufferCommunication, strlen(bufferCommunication));

            while(1) {

                read(sockServerPy, bufferCommunication, MAXCAR + 1);
                write(sockClientC, bufferCommunication, strlen(bufferCommunication));
                bzero(bufferCommunication, strlen(bufferCommunication));

                read(sockClientC, bufferCommunication, MAXCAR + 1);
                write(sockServerPy, bufferCommunication, strlen(bufferCommunication));
                bzero(bufferCommunication, strlen(bufferCommunication));

            }
        }
        else {
            close(sockClientC);
        }

    }

}