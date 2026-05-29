#!/usr/bin/env python3
from scripts.generate_volume_plate import main

if __name__ == "__main__":
    import sys

    sys.argv = [sys.argv[0], "--volume", "VIII"]
    main()
