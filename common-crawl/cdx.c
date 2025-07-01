#include <stdio.h>
#include <ctype.h>
#include <string.h>

#define BUFFER_SIZE 65536

int main() {
    char buffer[BUFFER_SIZE];
    char timestamp[9] = {0};
    char domain[256];
    
    while (fgets(buffer, BUFFER_SIZE, stdin)) {
        char *p = buffer;
        
        // Skip first field (up to first space)
        while (*p && *p != ' ') p++;
        if (!*p) continue;
        p++; // skip space
        
        // Extract 8-digit timestamp
        if (!isdigit(*p)) continue;
        memcpy(timestamp, p, 8);
        timestamp[8] = '\0';
        
        // Find "url":"
        char *url_start = strstr(p, "\"url\":\"");
        if (!url_start) continue;
        url_start += 7; // skip "url":"
        
        // Skip protocol
        char *proto_end = strstr(url_start, "://");
        if (!proto_end) continue;
        proto_end += 3;
        
        // Extract domain (up to / ; or ")
        char *domain_ptr = domain;
        char *p2 = proto_end;
        while (*p2 && *p2 != '/' && *p2 != ';' && *p2 != '"' && *p2 != '?' && (domain_ptr - domain) < 255) {
            *domain_ptr++ = tolower(*p2++);
        }
        *domain_ptr = '\0';
        
        if (domain[0]) {
            printf("%s\t%s\n", timestamp, domain);
        }
    }
    
    return 0;
}