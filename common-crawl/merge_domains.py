#!/usr/bin/env python3
"""
Simple merge tool: merges domain\ttimestamp streams into domain\tfirst\tlast format.
Handles out-of-order input by restarting with IO penalty.
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
    
    # Open files
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
    
    try:
        for stream_line in sys.stdin:
            try:
                stream_domain, stream_timestamp = parse_stream_line(stream_line)
            except ValueError:
                continue  # Skip malformed lines
                
            print(f"DEBUG: Processing {stream_domain} {stream_timestamp}", file=sys.stderr)
            
            # Check if we need to restart due to out-of-order OR duplicate domain
            if last_written and (stream_domain < last_written or stream_domain == last_written):
                print(f"DEBUG: Restart needed: {stream_domain} vs {last_written}", file=sys.stderr)
                
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
                    
            # Write all file entries that come before stream domain
            while file_domain and file_domain < stream_domain:
                print(f"DEBUG: Writing file entry {file_domain}", file=sys.stderr)
                output_f.write(file_line)
                last_written = file_domain
                
                file_line = input_f.readline()
                if file_line:
                    file_domain, file_first, file_last = parse_file_line(file_line)
                else:
                    file_domain = None
                    
            # Check if we can merge with current file entry
            if file_domain == stream_domain:
                # Merge timestamps
                merged_first = min(file_first, stream_timestamp)
                merged_last = max(file_last, stream_timestamp)
                
                print(f"DEBUG: Merging {stream_domain}: file({file_first}-{file_last}) + stream({stream_timestamp}) = ({merged_first}-{merged_last})", file=sys.stderr)
                
                output_f.write(f"{stream_domain}\t{merged_first}\t{merged_last}\n")
                last_written = stream_domain
                
                # Consume the file line
                file_line = input_f.readline()
                if file_line:
                    file_domain, file_first, file_last = parse_file_line(file_line)
                else:
                    file_domain = None
                    
            else:
                # Insert new domain
                print(f"DEBUG: Inserting new {stream_domain} {stream_timestamp}", file=sys.stderr)
                output_f.write(f"{stream_domain}\t{stream_timestamp}\t{stream_timestamp}\n")
                last_written = stream_domain
                
        # Write remaining file entries
        if file_domain:
            print(f"DEBUG: Writing remaining file entries starting with {file_domain}", file=sys.stderr)
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