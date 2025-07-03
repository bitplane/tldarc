#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

#define BUFFER_SIZE 1048576

// Check if character is valid in a domain name
#define IS_DOMAIN_CHAR(c) ((c) == '.' || (c) == '-' || (c) == '_' || (c) == '%' || (c) > 127 || \
                           ((c) >= '0' && (c) <= '9') || \
                           ((c) >= 'A' && (c) <= 'Z') || \
                           ((c) >= 'a' && (c) <= 'z'))

// Line buffering state
static char line_buffer[BUFFER_SIZE];
static char *line_start = line_buffer;
static char *buffer_end = line_buffer;

// Get next complete line, returns NULL on EOF
static inline char *next_line() {
    while (1) {
        // Find end of current line
        char *line_end = memchr(line_start, '\n', buffer_end - line_start);
        
        if (line_end) {
            // Found complete line
            *line_end = '\0';
            char *result = line_start;
            line_start = line_end + 1;
            return result;
        }
        
        // No complete line, need more data
        size_t partial_len = buffer_end - line_start;
        
        // Move partial line to start if needed
        if (partial_len > 0 && line_start != line_buffer) {
            memmove(line_buffer, line_start, partial_len);
        }
        line_start = line_buffer;
        buffer_end = line_buffer + partial_len;
        
        // Check for line too long
        size_t space_left = BUFFER_SIZE - partial_len;
        if (space_left <= 1) {
            fprintf(stderr, "Warning: Line too long, skipping\n");
            line_start = line_buffer;
            buffer_end = line_buffer;
            space_left = BUFFER_SIZE;
        }
        
        // Read more data
        size_t bytes_read = fread(buffer_end, 1, space_left - 1, stdin);
        if (bytes_read == 0) {
            // EOF
            if (partial_len > 0) {
                // Process last line without newline
                buffer_end[0] = '\0';
                char *result = line_start;
                line_start = buffer_end;
                return result;
            }
            return NULL;
        }
        buffer_end += bytes_read;
    }
}

int main() {
    char domain[2048];
    char *line;
    
    while ((line = next_line()) != NULL) {
        char *p = line;
        
        // Step 1: Skip to timestamp (after first space)
        while (*p && *p != ' ') p++;
        if (!*p) continue;
        p++; // skip space
        
        // Step 2: Extract timestamp (YYYYMMDD)
        if (p + 8 > line + strlen(line)) continue;
        char timestamp[9];
        memcpy(timestamp, p, 8);
        timestamp[8] = '\0';
        
        // Validate timestamp
        int ts = atoi(timestamp);
        if (ts < 19700000) continue;
        
        // Step 3: Find URL
        char *url_pos = strstr(p, "\"url\"");
        if (!url_pos) continue;
        
        char *proto_end = strstr(url_pos, "://");
        if (!proto_end) continue;
        proto_end += 3;
        
        // Skip user:pass@ if present
        char *at_sign = strchr(proto_end, '@');
        char *first_slash = strchr(proto_end, '/');
        if (at_sign && (!first_slash || at_sign < first_slash)) {
            proto_end = at_sign + 1;
        }
        
        // Step 4: Extract and process domain in single pass
        char *domain_ptr = domain;
        char *seg_start = domain;
        char *a = domain;
        char *b = domain;
        char *c = domain;
        int has_numeric_segment = 0;
        
        // Skip IPv6 addresses
        if (*proto_end == '[') {
            continue;
        }
        
        // Copy domain while tracking segments
        char *src = proto_end;
        while (*src && IS_DOMAIN_CHAR(*src) && (domain_ptr - domain) < 2047) {
            
            if (*src == '.') {
                // Check if next character is valid domain char, if not stop here
                if (!IS_DOMAIN_CHAR(*(src + 1))) {
                    break;
                }
                
                // Check if current segment is all numeric
                int all_digit = 1;
                for (char *check = seg_start; check < domain_ptr; check++) {
                    if (!isdigit(*check)) {
                        all_digit = 0;
                        break;
                    }
                }
                if (all_digit && seg_start < domain_ptr) {
                    has_numeric_segment = 1;
                }
                
                // Update segment pointers
                a = b;
                b = c;
                c = domain_ptr + 1;
                seg_start = domain_ptr + 1;
            }
            
            *domain_ptr++ = tolower(*src++);
        }
        *domain_ptr = '\0';
        
        // Strip trailing dot if present
        if (domain_ptr > domain && *(domain_ptr - 1) == '.') {
            *(--domain_ptr) = '\0';
        }
        
        // Skip if numeric segment found
        if (has_numeric_segment) continue;
        
        // Check final segment for numeric
        if (seg_start < domain_ptr) {
            int all_digit = 1;
            for (char *check = seg_start; check < domain_ptr; check++) {
                if (!isdigit(*check)) {
                    all_digit = 0;
                    break;
                }
            }
            if (all_digit) continue;
        }
        
        // Determine output based on segment positions and lengths
        char *output_start;
        
        if (c == domain) {
            // No dots found, single segment
            output_start = domain;
        } else if (b == domain) {
            // Only one dot found (two segments)
            output_start = domain;
        } else {
            // At least two dots (three or more segments)
            // Calculate length of segment b
            char *b_end = c - 1; // c points after the dot
            int b_len = b_end - b;
            
            if (b_len <= 3) {
                // b is short, include a.b.c
                output_start = a;
            } else {
                // b is long, just b.c
                output_start = b;
            }
        }
        
        if (*output_start) {
            printf("%s\t%s\n", timestamp, output_start);
        }
    }
    
    return 0;
}