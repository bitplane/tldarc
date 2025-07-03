#!/usr/bin/env python3
"""
Simple stream accumulator: accumulates consecutive identical domains.
Only triggers restart for true out-of-order cases.
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

def merge_domains(output_file):
    """Merge domain observations from stdin into output file."""
    temp_file = output_file + '.tmp'
    
    # Stream accumulator
    current_domain = None
    current_first = None
    current_last = None
    
    # File reading state
    if os.path.exists(output_file):
        input_f = open(output_file, 'r')
        file_line = input_f.readline()
        if file_line:
            file_domain, file_first, file_last = parse_file_line(file_line)
        else:
            file_domain = None
    else:
        input_f = None
        file_domain = None
        
    output_f = open(temp_file, 'w')
    last_written = None
    
    def flush_current():
        """Write out accumulated domain."""
        nonlocal current_domain, current_first, current_last, last_written
        if current_domain:
            print(f"DEBUG: Flushing {current_domain} {current_first}-{current_last}", file=sys.stderr)
            output_f.write(f"{current_domain}\t{current_first}\t{current_last}\n")
            last_written = current_domain
            current_domain = None
    
    def restart_merge():
        """Restart due to out-of-order input."""
        nonlocal input_f, output_f, file_domain, file_line, last_written
        
        print(f"Warning: Out of order domain {stream_domain} < {last_written}, restarting merge", file=sys.stderr)
        
        # Flush any pending domain first
        flush_current()
        
        # Close files
        output_f.close()
        if input_f:
            input_f.close()
            
        # Move temp over original and restart
        shutil.move(temp_file, output_file)
        
        # Reopen everything
        input_f = open(output_file, 'r')
        output_f = open(temp_file, 'w')
        last_written = None
        
        # Read first line from file
        file_line = input_f.readline()
        if file_line:
            file_domain, file_first, file_last = parse_file_line(file_line)
        else:
            file_domain = None
    
    try:
        for stream_line in sys.stdin:
            try:
                stream_domain, stream_timestamp = parse_stream_line(stream_line)
            except ValueError:
                continue  # Skip malformed lines
                
            # Check if we need to restart due to out-of-order
            if (last_written and stream_domain < last_written) or (current_domain and stream_domain < current_domain):
                restart_merge()
                
            print(f"DEBUG: Processing {stream_domain} {stream_timestamp}, current={current_domain}", file=sys.stderr)
            
            # Accumulate this observation
            if current_domain == stream_domain:
                # Same domain - update timestamps
                print(f"DEBUG: Accumulating {stream_domain}", file=sys.stderr)
                current_first = min(current_first, stream_timestamp)
                current_last = max(current_last, stream_timestamp)
            else:
                # Different domain - flush previous and start new
                flush_current()
                
                # Write any file entries that come before this domain
                while file_domain and file_domain < stream_domain:
                    output_f.write(file_line)
                    last_written = file_domain
                    
                    file_line = input_f.readline()
                    if file_line:
                        file_domain, file_first, file_last = parse_file_line(file_line)
                    else:
                        file_domain = None
                        
                # Check if we can merge with file entry
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
                        file_domain = None
                else:
                    # New domain
                    current_domain = stream_domain
                    current_first = stream_timestamp
                    current_last = stream_timestamp
                    
        # Flush final accumulated domain
        flush_current()
        
        # Write remaining file entries
        if file_domain:
            output_f.write(file_line)
            for line in input_f:
                output_f.write(line)
                
    finally:
        output_f.close()
        if input_f:
            input_f.close()
            
    # Atomic replace
    shutil.move(temp_file, output_file)
    print(f"Merge complete: {output_file}", file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: merge_domains.py <output_file>", file=sys.stderr)
        print("Reads domain\\ttimestamp from stdin", file=sys.stderr)
        print("Merges into output_file as domain\\tfirst\\tlast", file=sys.stderr)
        sys.exit(1)
        
    merge_domains(sys.argv[1])