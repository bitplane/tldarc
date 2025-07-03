#!/usr/bin/env python3
"""
Clean merge implementation with proper function separation and dependency injection.
"""

import sys
import os
import shutil

def parse_stream_line(line):
    """Parse domain\ttimestamp line."""
    parts = line.strip().split('\t')
    if len(parts) != 2:
        raise ValueError(f"Invalid format: {line}")
    return parts[0], parts[1]

def parse_file_line(line):
    """Parse domain\tfirst\tlast line."""
    parts = line.strip().split('\t')
    if len(parts) != 3:
        raise ValueError(f"Invalid format: {line}")
    return parts[0], parts[1], parts[2]

def flush_current_domain(output_f, current_domain, current_first, current_last):
    """Write accumulated domain to output and return updated last_written."""
    if current_domain:
        output_f.write(f"{current_domain}\t{current_first}\t{current_last}\n")
        return current_domain
    return None

def restart_merge(output_f, input_f, file_domain, file_line, temp_file, output_file, triggering_domain, compared_to):
    """Handle out-of-order restart: copy remaining file data, mv temp over original, reopen."""
    print(f"Warning: Out of order domain {triggering_domain} < {compared_to}, restarting merge", file=sys.stderr)
    
    # Copy any remaining file entries to temp output
    if file_domain:
        output_f.write(file_line)
        for line in input_f:
            output_f.write(line)
    
    # Close files
    output_f.close()
    if input_f:
        input_f.close()
        
    # Move temp over original
    shutil.move(temp_file, output_file)
    
    # Reopen everything
    input_f = open(output_file, 'r') if os.path.exists(output_file) else None
    output_f = open(temp_file, 'w')
    
    # Read first line from file
    if input_f:
        file_line = input_f.readline()
        if file_line:
            file_domain, file_first, file_last = parse_file_line(file_line)
        else:
            file_domain, file_first, file_last = None, None, None
    else:
        file_line = None
        file_domain, file_first, file_last = None, None, None
        
    return input_f, output_f, file_domain, file_first, file_last, file_line

def write_file_entries_before(output_f, input_f, file_domain, file_first, file_last, file_line, target_domain):
    """Write all file entries that come before target_domain. Returns updated file state and last_written."""
    last_written = None
    
    while file_domain and file_domain < target_domain:
        output_f.write(file_line)
        last_written = file_domain
        
        file_line = input_f.readline()
        if file_line:
            file_domain, file_first, file_last = parse_file_line(file_line)
        else:
            file_domain, file_first, file_last = None, None, None
            
    return file_domain, file_first, file_last, file_line, last_written

def try_merge_with_file(input_f, file_domain, file_first, file_last, file_line, stream_domain, stream_timestamp):
    """Try to merge stream domain with file entry. Returns (merged, current_domain, current_first, current_last, updated_file_state)."""
    if file_domain == stream_domain:
        # Merge with file entry
        current_domain = stream_domain
        current_first = min(file_first, stream_timestamp)
        current_last = max(file_last, stream_timestamp)
        
        # Consume file entry
        file_line = input_f.readline()
        if file_line:
            file_domain, file_first, file_last = parse_file_line(file_line)
        else:
            file_domain, file_first, file_last = None, None, None
            
        return True, current_domain, current_first, current_last, file_domain, file_first, file_last, file_line
    
    return False, stream_domain, stream_timestamp, stream_timestamp, file_domain, file_first, file_last, file_line

def merge_domains(output_file):
    """Main merge function with dependency injection."""
    temp_file = output_file + '.tmp'
    
    # Initialize state
    current_domain = None
    current_first = None
    current_last = None
    last_written = None
    
    # Open files
    if os.path.exists(output_file):
        input_f = open(output_file, 'r')
        file_line = input_f.readline()
        if file_line:
            file_domain, file_first, file_last = parse_file_line(file_line)
        else:
            file_domain, file_first, file_last = None, None, None
    else:
        input_f = None
        file_line = None
        file_domain, file_first, file_last = None, None, None
        
    output_f = open(temp_file, 'w')
    
    try:
        for stream_line in sys.stdin:
            try:
                stream_domain, stream_timestamp = parse_stream_line(stream_line)
            except ValueError:
                continue
                
            # Check if restart needed
            if ((last_written and stream_domain < last_written) or 
                (current_domain and stream_domain < current_domain)):
                
                # Determine what we're comparing against
                compared_to = last_written if (last_written and stream_domain < last_written) else current_domain
                
                # Flush current domain first
                flushed = flush_current_domain(output_f, current_domain, current_first, current_last)
                if flushed:
                    last_written = flushed
                current_domain = None
                
                # Restart merge
                input_f, output_f, file_domain, file_first, file_last, file_line = restart_merge(
                    output_f, input_f, file_domain, file_line, temp_file, output_file, stream_domain, compared_to)
                last_written = None
                current_domain = None
                current_first = None
                current_last = None
                
            # Accumulate or flush
            if current_domain == stream_domain:
                # Same domain - accumulate
                current_first = min(current_first, stream_timestamp)
                current_last = max(current_last, stream_timestamp)
            else:
                # Different domain - flush current and start new
                flushed = flush_current_domain(output_f, current_domain, current_first, current_last)
                if flushed:
                    last_written = flushed
                
                # Write file entries before this domain
                file_domain, file_first, file_last, file_line, written = write_file_entries_before(
                    output_f, input_f, file_domain, file_first, file_last, file_line, stream_domain)
                if written:
                    last_written = written
                    
                # Try to merge with file entry
                merged, current_domain, current_first, current_last, file_domain, file_first, file_last, file_line = try_merge_with_file(
                    input_f, file_domain, file_first, file_last, file_line, stream_domain, stream_timestamp)
                    
        # Flush final domain
        flush_current_domain(output_f, current_domain, current_first, current_last)
        
        # Copy remaining file entries
        if file_domain:
            output_f.write(file_line)
            for line in input_f:
                output_f.write(line)
                
    finally:
        output_f.close()
        if input_f:
            input_f.close()
            
    shutil.move(temp_file, output_file)
    print(f"Merge complete: {output_file}", file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: merge_domains.py <output_file>", file=sys.stderr)
        sys.exit(1)
        
    merge_domains(sys.argv[1])