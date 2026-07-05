#!/usr/bin/env python3
"""
TCP Port Scanner
Usage: python port_scanner.py <host> [options]
"""

import argparse
import logging
import socket
import sys
import threading
from datetime import datetime
from ipaddress import ip_address, IPv4Address, IPv6Address

# ------------------------- Configuration -------------------------
DEFAULT_TIMEOUT = 1.0          # seconds
DEFAULT_THREADS = 100
DEFAULT_PORT_RANGE = (1, 1024) # commonly used ports

# ------------------------- Logging Setup -------------------------
LOG_FILE = "port_scan_results.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# ------------------------- Core Functions -------------------------

def scan_port(host, port, timeout=DEFAULT_TIMEOUT):
    """
    Attempt a TCP connection to a single port.
    Returns a tuple: (port, state, error_message)
    state: 'open', 'closed', 'timeout', 'error'
    """
    try:
        # Resolve hostname to IP (socket will do this, but we catch exceptions)
        # We create a socket with IPv4 or IPv6 depending on the host.
        # Using socket.AF_UNSPEC lets the system choose.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            if result == 0:
                return (port, "open", None)
            else:
                # result is an error number; map to human-readable if possible
                # Common: 111 = connection refused (closed), 110 = timeout, etc.
                if result == 110 or result == 60:  # timeout on some systems
                    return (port, "timeout", "Connection timed out")
                else:
                    return (port, "closed", f"Connection refused (errno {result})")
    except socket.gaierror as e:
        return (port, "error", f"Name resolution error: {e}")
    except socket.timeout:
        return (port, "timeout", "Connection timed out")
    except Exception as e:
        return (port, "error", str(e))


def scan_host(host, ports, timeout=DEFAULT_TIMEOUT, max_threads=DEFAULT_THREADS):
    """
    Scan a list of ports on a given host using multiple threads.
    Returns a list of (port, state, message) for each port.
    """
    results = []
    lock = threading.Lock()
    threads = []

    def worker(port):
        port, state, msg = scan_port(host, port, timeout)
        with lock:
            results.append((port, state, msg))
            # Log each result as we go (optional)
            logger.info(f"Port {port}: {state.upper()} - {msg if msg else ''}")

    # Create and start threads
    for port in ports:
        t = threading.Thread(target=worker, args=(port,))
        threads.append(t)
        t.start()
        # Limit concurrent threads to avoid overwhelming the system
        if len(threads) >= max_threads:
            # Wait for one to finish before starting another
            # (simple throttle: join the first thread in the list)
            threads[0].join()
            threads.pop(0)

    # Wait for all remaining threads
    for t in threads:
        t.join()

    # Sort results by port number for consistent output
    results.sort(key=lambda x: x[0])
    return results


def print_summary(results, host):
    """Print a nicely formatted summary."""
    open_ports = [p for p, state, _ in results if state == "open"]
    closed_ports = [p for p, state, _ in results if state == "closed"]
    timeout_ports = [p for p, state, _ in results if state == "timeout"]
    error_ports = [p for p, state, _ in results if state == "error"]

    print("\n" + "=" * 60)
    print(f"Scan Results for {host}")
    print("=" * 60)
    print(f"Total ports scanned : {len(results)}")
    print(f"Open ports          : {len(open_ports)}")
    print(f"Closed ports        : {len(closed_ports)}")
    print(f"Timeouts            : {len(timeout_ports)}")
    print(f"Errors              : {len(error_ports)}")
    if open_ports:
        print(f"Open ports list     : {', '.join(map(str, open_ports))}")
    print("=" * 60)

    # Also log summary
    logger.info(f"Scan completed for {host}. Open ports: {open_ports}")

# ------------------------- Command Line Interface -------------------------

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="TCP Port Scanner",
        epilog="Example: python port_scanner.py example.com -p 1-1000 -t 2 -T 200"
    )
    parser.add_argument(
        "host",
        help="Target host (IP address or domain name)"
    )
    parser.add_argument(
        "-p", "--ports",
        help="Port range to scan (e.g., 1-1024, or 80,443,8080). Default: 1-1024",
        default="1-1024"
    )
    parser.add_argument(
        "-t", "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help=f"Connection timeout in seconds (default: {DEFAULT_TIMEOUT})"
    )
    parser.add_argument(
        "-T", "--threads",
        type=int,
        default=DEFAULT_THREADS,
        help=f"Maximum number of concurrent threads (default: {DEFAULT_THREADS})"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Increase output verbosity (log every port scan attempt)"
    )
    return parser.parse_args()


def parse_port_range(port_spec):
    """
    Parse a port specification like '1-1024' or '80,443,8080'
    Returns a list of integers.
    """
    ports = []
    # Remove spaces
    port_spec = port_spec.replace(" ", "")
    if "," in port_spec:
        parts = port_spec.split(",")
        for part in parts:
            if "-" in part:
                start, end = part.split("-")
                ports.extend(range(int(start), int(end) + 1))
            else:
                ports.append(int(part))
    elif "-" in port_spec:
        start, end = port_spec.split("-")
        ports = list(range(int(start), int(end) + 1))
    else:
        ports = [int(port_spec)]
    return ports


def main():
    args = parse_arguments()

    # Adjust logging level
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    # Validate host (basic)
    try:
        # Test resolution
        socket.gethostbyname(args.host)
    except socket.gaierror:
        logger.error(f"Could not resolve host: {args.host}")
        sys.exit(1)

    # Parse ports
    try:
        ports = parse_port_range(args.ports)
        if not ports:
            logger.error("No valid ports specified.")
            sys.exit(1)
        # Ensure ports are within 1-65535 (optional)
        invalid = [p for p in ports if p < 1 or p > 65535]
        if invalid:
            logger.warning(f"Ignoring invalid ports (outside 1-65535): {invalid}")
            ports = [p for p in ports if 1 <= p <= 65535]
            if not ports:
                logger.error("No valid ports remaining.")
                sys.exit(1)
    except ValueError as e:
        logger.error(f"Invalid port specification: {e}")
        sys.exit(1)

    logger.info(f"Starting scan of {args.host} on {len(ports)} ports")
    logger.info(f"Timeout: {args.timeout}s, Threads: {args.threads}")

    start_time = datetime.now()

    # Perform the scan
    results = scan_host(args.host, ports, args.timeout, args.threads)

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    # Print summary
    print_summary(results, args.host)
    logger.info(f"Scan completed in {duration:.2f} seconds")
    logger.info(f"Results logged to {LOG_FILE}")

# ------------------------- Entry Point -------------------------
if __name__ == "__main__":
    main()
