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
    int sockServerC, sockClientPy, sockClientC;
    char bufferCommunication[MAXCAR + 1];

    struct sockaddr_in addrClientC, addrServerC;

    //--------------------------------------------------------------------------------------------------
    //---------------------------------------Connecting Socket------------------------------------------
    //--------------------------------------------------------------------------------------------------

    printf("Connecting to the socket...\n");

    sockClientC = socket(AF_INET, SOCK_STREAM, 0);
   
    addrClientC.sin_family = AF_INET;
    addrClientC.sin_port = htons(700);
    addrClientC.sin_addr.s_addr = INADDR_ANY;

    CHECK_ERROR(bind(sockClientC, (struct sockaddr*) &addrClientC, sizeof(addrClientC)), -1, "Erreur de liaison 1\n");

    printf("Socket connected\n");

    //--------------------------------------------------------------------------------------------------
    //-------------------------------------Connecting to Server-----------------------------------------
    //--------------------------------------------------------------------------------------------------

    printf("Connecting to Server...\n");

    sockServerC = socket(AF_INET, SOCK_STREAM, 0);

    addrServerC.sin_family = AF_INET;
    addrServerC.sin_port = htons(600);
    addrServerC.sin_addr.s_addr = inet_addr("192.168.0.124");

    connect(sockServerC, (const struct sockaddr *) &addrServerC, sizeof(addrServerC));

    printf("Server connected\n");

    //--------------------------------------------------------------------------------------------------
    //-----------------------------------Connecting to Client Py----------------------------------------
    //--------------------------------------------------------------------------------------------------

    printf("Waiting for Client Py...\n");

    listen(sockClientC, 1);

    sockClientPy = accept(sockClientC, NULL, NULL);

    printf("Client Py Connected...\n");

    //--------------------------------------------------------------------------------------------------
    //----------------------------------------Communication---------------------------------------------
    //--------------------------------------------------------------------------------------------------

    while (1) {
        read(sockClientPy, bufferCommunication, MAXCAR + 1);
        write(sockServerC, bufferCommunication, strlen(bufferCommunication));
        bzero(bufferCommunication, strlen(bufferCommunication));

        read(sockServerC, bufferCommunication, MAXCAR + 1);

        int i;
        for (i = 0; bufferCommunication[i] != '\0'; i++) {
            if (bufferCommunication[i] == '@')
                bufferCommunication[i + 1] = '\0';
        }

        write(sockClientPy, bufferCommunication, strlen(bufferCommunication));
        bzero(bufferCommunication, strlen(bufferCommunication));
    }

}