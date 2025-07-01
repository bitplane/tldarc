#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

#define BUFFER_SIZE 65536
#define DEBUG(fmt, ...) fprintf(stderr, "DEBUG: " fmt "\n", ##__VA_ARGS__)

int is_all_digits(const char *start, const char *end) {
    if (start >= end) return 0;
    for (const char *p = start; p < end; p++) {
        if (!isdigit(*p)) return 0;
    }
    return 1;
}

int main() {
    char buffer[BUFFER_SIZE];
    char raw_domain[256];
    
    while (fgets(buffer, BUFFER_SIZE, stdin)) {
        char *p = buffer;
        
        // Skip first field (up to first space)
        while (*p && *p != ' ') p++;
        if (!*p) continue;
        p++; // skip space
        
        // Extract timestamp (first 6 chars for YYYYMM)
        char *timestamp = p;
        p[6] = '\0'; // Null terminate at 6th position
        int timestamp_val = atoi(timestamp);
        if (timestamp_val < 197000) continue; // Skip invalid timestamps
        p += 7; // Move past timestamp and null terminator
        
        // Find "url" then look for "//" after it
        char *url_pos = strstr(p, "\"url\"");
        if (!url_pos) continue;
        
        // Find "//" after the "url" 
        char *proto_end = strstr(url_pos, "://");
        if (!proto_end) continue;
        proto_end += 3;
        
        // Skip user:pass@ if present
        char *at_sign = strchr(proto_end, '@');
        char *first_slash = strchr(proto_end, '/');
        if (at_sign && (!first_slash || at_sign < first_slash)) {
            proto_end = at_sign + 1;
        }
        
        // Extract raw domain (up to port, path, query, or end quote)
        char *domain_ptr = raw_domain;
        char *p2 = proto_end;
        while (*p2 && *p2 != '/' && *p2 != ':' && *p2 != '?' && *p2 != '#' && *p2 != '"' && (domain_ptr - raw_domain) < 255) {
            *domain_ptr++ = tolower(*p2++);
        }
        *domain_ptr = '\0';
        
        if (!raw_domain[0]) continue;
        
        // Check for numeric segments and apply smart domain algorithm
        char *start = raw_domain;
        char *pos1 = raw_domain;
        char *pos2 = raw_domain;
        int has_numeric_segment = 0;
        
        // Check each segment for being all digits
        char *seg_start = raw_domain;
        for (char *c = raw_domain; *c; c++) {
            if (*c == '.' || *(c+1) == '\0') {
                char *seg_end = (*c == '.') ? c : c + 1;
                if (is_all_digits(seg_start, seg_end)) {
                    has_numeric_segment = 1;
                    break;
                }
                seg_start = c + 1;
            }
        }
        
        if (has_numeric_segment) continue; // Skip domains with numeric segments
        
        // Apply position tracking algorithm to find significant domain part
        seg_start = raw_domain;
        for (char *c = raw_domain; *c; c++) {
            if (*c == '.') {
                if (c - seg_start > 4) { // Current segment is >4 chars
                    start = seg_start;
                }
                seg_start = c + 1; // Start of next segment
            }
        }
        
        // Null terminate domain in place at the calculated position
        if (start[0]) {
            printf("%s\t%s\n", timestamp, start);
        }
    }
    
    return 0;
}