#ifndef __HEADER_H__
#define __HEADER_H__

#include <cstdio>
#include <unistd.h>
#include <stdlib.h>
#include <memory.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <pthread.h>

 /* SSLeay stuff */
#include <openssl/rsa.h>       
#include <openssl/crypto.h>
#include <openssl/x509.h>
#include <openssl/pem.h>
#include <openssl/ssl.h>
#include <openssl/err.h>

#include <queue>
#include <mutex>
#include <chrono>
#include <vector>
#include <functional>
#include <condition_variable>
#include <shared_mutex>	

#endif