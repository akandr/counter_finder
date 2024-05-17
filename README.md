## Overview
This tool is designed to efficiently locate and analyze 16-bit counters embedded within the headers of raw image frames. It uniquely addresses the challenge posed by potential padding bytes that might separate parts of the counter, ensuring accurate detection even when counters are not continuously aligned.

## Features
- **Counter Detection**: Identifies 16-bit counters within specified byte ranges of raw image frame headers.
- **Padding Byte Consideration**: Capable of detecting counters that are separated by a padding byte, accommodating non-standard counter configurations.
- **Concurrency**: Utilizes multithreading to enhance performance, enabling faster processing of multiple image frames.
- **Endianness Support**: Supports both little-endian and big-endian byte orders to cater to different image formats.
- **Incremental Analysis**: Compares counters across consecutive frames to find incrementing sequences, useful in determining frame order or integrity.

