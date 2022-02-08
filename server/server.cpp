#include "server.h"

using namespace std;

mutex mtx;

queue<char*> disconnQUEUE;
queue<char*> connQUEUE;

char recvMSG[BUFFSIZE];
char sendMSG[BUFFSIZE];

int main()
{
    int sockfd, new_fd;
    struct sockaddr_in my_addr;
    struct sockaddr_in their_addr;
    unsigned int sin_size;
    int rcv_byte;
    int val = 1;
    int count = 1;

    pthread_t t_thread;

    pthread_create(&t_thread, NULL, send_thread, (void*)1);
    //sleep(1);

    while(1)
    {
        sockfd = socket(AF_INET, SOCK_STREAM, 0);
        if(sockfd == -1)
        {
            perror("Server-socket() error!");
            exit(EXIT_FAILURE);
        }
        else printf("Server-socket() sockfd is OK...\n");
        
        my_addr.sin_family = AF_INET;
        
        my_addr.sin_port = htons(RECV_SERVER_PORT);
        
        my_addr.sin_addr.s_addr = INADDR_ANY;
        
        memset(&(my_addr.sin_zero), 0, 8);
        
        if(setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, (char*)&val, sizeof val) < 0)
        {
            perror("setsockopt");
            close(sockfd);
            return -1;
        }

        if(bind(sockfd, (struct sockaddr *)&my_addr, sizeof (struct sockaddr)) == -1)
        {
            perror("Server-bind() error!");
            exit(EXIT_FAILURE);
        }
        else printf("Server-bind() is OK...\n");

        if(listen(sockfd, BACKLOG) == -1)
        {
            perror("listen() error!");
            exit(EXIT_FAILURE);
        }
        else printf("listen() is OK...\n\n");
        
        sin_size = sizeof(struct sockaddr_in);
        new_fd = accept(sockfd, (struct sockaddr *)&their_addr, &sin_size);
        printf("accept() is OK...\n");
        printf("\n");

        mtx.lock();
        recv(new_fd, recvMSG, sizeof(recvMSG), 0);
        //printf("count: %d\n %s\n", count, recvMSG);
        // recvMSG[0] = '\0';
        count++;
        close(sockfd);
        close(new_fd);
        mtx.unlock();
    }
}


void* send_thread(void *arg)
{
    int err;
    int server_fd;
    int client_fd;
    struct sockaddr_in my_addr;
    struct sockaddr_in client_addr;
    socklen_t client_len;
    
    /* SSL Context 및 관련 구조체를 선언 */
    SSL_CTX             *ctx;
    SSL                 *ssl;
    X509                *client_cert;
    char                *str;
    char                buf[BUFFSIZE];
    const SSL_METHOD    *method;

    /* SSL 관련 초기화 작업을 수행 */
    SSL_load_error_strings();
    SSLeay_add_ssl_algorithms();
    method = SSLv23_server_method();          // 서버 메소드.
    ctx = SSL_CTX_new(method);                // 지정된 초기 값을 이용하여 SSL Context를 생성
   
    if(!ctx) {
        ERR_print_errors_fp(stderr);
        exit(2);
    }

    if(!ctx) {
        ERR_print_errors_fp(stderr);
        exit(2);
    }
   
    /* 사용하게 되는 인증서 파일을 설정 */
    if(SSL_CTX_use_certificate_file(ctx, CERTF, SSL_FILETYPE_PEM) <= 0) {      // 인증서를 파일로 부터 로딩할때 사용함
        ERR_print_errors_fp(stderr);
        exit(3);
    }
   
    /* 암호화 통신을 위해서 이용하는 개인 키를 설정 */
    if(SSL_CTX_use_PrivateKey_file(ctx, KEYF, SSL_FILETYPE_PEM) <= 0) {
        ERR_print_errors_fp(stderr);
        exit(4);
    }
   
    /* 개인 키가 사용 가능한 것인지 확인 */
    if(!SSL_CTX_check_private_key(ctx)) {
        fprintf(stderr, "ERROR! Private key does not match the certificate public keyn");
        exit(5);
    }
    
    /* Prepare TCP socket for receiving connections */
    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    CHK_ERR(server_fd, "socket");
   
    memset(&my_addr, ' ', sizeof(my_addr));
    my_addr.sin_family = AF_INET;
    my_addr.sin_addr.s_addr = INADDR_ANY;
    my_addr.sin_port = htons(MY_PORT); /* Server Port number */
    
    err = bind(server_fd, (struct sockaddr*)&my_addr, sizeof(my_addr));
    CHK_ERR(err, "bind");
   
    /* Receive a TCP connection. */
    
     err = listen(server_fd, BACKLOG);
     CHK_ERR(err, "listen");
    
     client_len = sizeof(client_addr);
     client_fd = accept(server_fd, (struct sockaddr*)&client_addr, &client_len);
     CHK_ERR(client_fd, "accept");
     //close(server_fd);
    
     printf("Connection from %d, port %d\n", client_addr.sin_addr.s_addr, client_addr.sin_port);
    
     /* TCP connection is ready. Do server side SSL. */
    ssl = SSL_new(ctx); // 설정된 Context를 이용하여 SSL 세션의 초기화 작업을 수행한다.
    CHK_NULL(ssl);
    SSL_set_fd(ssl, client_fd);
    err = SSL_accept(ssl);    // SSL 세션을 통해 클라이언트의 접속을 대기한다.
    CHK_SSL(err);
   
    /* Get the cipher – opt */
    printf("SSL connection using %s\n", SSL_get_cipher(ssl));
   
    /* 클라이언트의 인증서를 받음 – opt */
    client_cert = SSL_get_peer_certificate(ssl);
    if(client_cert != NULL) {
        printf("Client certificate:\n");
       
        str = X509_NAME_oneline(X509_get_subject_name(client_cert), 0, 0);
        CHK_NULL(str);
        //printf("t subject: %s\n", str);
        OPENSSL_free(str);
       
        str = X509_NAME_oneline(X509_get_issuer_name(client_cert), 0, 0);
        CHK_NULL(str);
        //printf("t issuer: %s\n", str);
        OPENSSL_free(str);
       
        /* We could do all sorts of certificate verification stuff here before deallocating the certificate. */
        X509_free(client_cert);
    } 
    // else {
    //     printf("Client does not have certificate.\n");
    // }
   

    // FILE *f = fopen("encrypted_data.bin", "rb");
    // fseek(f, 0, SEEK_END);
    // long fsize = ftell(f);
    // fseek(f, 0, SEEK_SET); 

    // fread(recvMSG, fsize, 1, f);
    // fclose(f);
    // printf("%s\n", recvMSG);   
    //SSL_write(ssl, recvMSG, sizeof(recvMSG));

    while(1)
    {
        if(strcmp(recvMSG, "\0") != 0)
        {
            char *ptr = strtok(recvMSG, "{");
            ptr = strtok(NULL, "}");      // 다음 문자열을 잘라서 포인터를 반환
            sprintf(sendMSG, "%s%s%s", "{",ptr,"}");
            printf("\nsend: %s\nlen: %ld\nsize: %ld\n", sendMSG, strlen(sendMSG), sizeof(sendMSG));
            //printf("%s\n", sendMSG);
            SSL_write(ssl, sendMSG, strlen(sendMSG));  
            recvMSG[0] = '\0';
        }
    }   
    /* 설정한 자원을 반환하고 종료한다. */
    close(client_fd);
    SSL_free(ssl);
    SSL_CTX_free(ctx);

    return(0);
}
