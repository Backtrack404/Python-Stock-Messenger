#ifndef __SERVER_H__ 
#define __SERVER_H__

#include "header.h"

#define HOME "./"

#define CERTF "server.crt"
#define KEYF "server.key"
 
#define CHK_NULL(x) if((x) == NULL) exit(EXIT_FAILURE);
#define CHK_ERR(err, s) if((err) == -1) { perror(s); exit(EXIT_FAILURE); }
#define CHK_SSL(err) if((err) == -1) { ERR_print_errors_fp(stderr); exit(EXIT_FAILURE); }

#define TRUE 1
#define FALSE 0

#define BACKLOG 10
#define BUFFSIZE 4096
#define MY_PORT 8007 
#define RECV_SERVER_PORT 3000

void* send_thread(void* arg);

#endif