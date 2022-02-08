#ifndef __DEFINE_H__
#define __DEFINE_H__

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <pthread.h>

#define LOGIN "OK"

#define SERV_IP "127.0.0.1"
#define SERV_PORT 3000

#define BUFFSIZE 10000
#define BUFFID 20
#define BUFFPW 20

#endif