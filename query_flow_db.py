#!/usr/bin/python3

import sqlite3
from tabulate import tabulate

SLOW_RTT_THRESHOULD_IN_NANOSECONDS = 80000000
SLOW_DNS_THRESHOULD_IN_MSECONDS = 2

def query_flows_with_drop(input=""):
    # Connect to the SQLite database
    conn = sqlite3.connect('flows.db')  # Replace 'example.db' with the path to your SQLite database file
    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()
    cursor.execute(
        "SELECT PktDropLatestDropCause, DstAddr, DstPort, Interface, Proto, SrcAddr, SrcPort, Bytes, Packets, PktDropBytes, PktDropPackets FROM flow WHERE PktDropLatestDropCause >  0 LIMIT 10"
    )

    # Fetch the results
    rows = cursor.fetchall()
    # Get column names from the cursor description
    headers = [description[0] for description in cursor.description]
    # Format the result as a table
    table = tabulate(rows, headers=headers, tablefmt="grid")
    # Close the cursor and connection
    cursor.close()
    conn.close()
    print(table)
    return table

def query_flows_without_drop(input=""):
    # Connect to the SQLite database
    conn = sqlite3.connect('flows.db')  # Replace 'example.db' with the path to your SQLite database file
    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()
    # Execute a SELECT query
    cursor.execute("SELECT DstAddr, DstPort, Interface, Proto, SrcAddr, SrcPort, Bytes, Packets FROM flow LIMIT 10")

    # Fetch the results
    rows = cursor.fetchall()
    # Get column names from the cursor description
    headers = [description[0] for description in cursor.description]
    # Format the result as a table
    table = tabulate(rows, headers=headers, tablefmt="grid")
    # Close the cursor and connection
    cursor.close()
    conn.close()
    print(table)
    return table

def query_flows_with_slow_rtt(input=""):
    # Connect to the SQLite database
    conn = sqlite3.connect('flows.db')  # Replace 'example.db' with the path to your SQLite database file
    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()
    cursor.execute(
        "SELECT TimeFlowRTTNs, DstAddr, DstPort, Interface, Proto, SrcAddr, SrcPort, Bytes, Packets FROM flow WHERE  TimeFlowRTTNs > " + str(SLOW_RTT_THRESHOULD_IN_NANOSECONDS) + " LIMIT 10"
    )

    # Fetch the results
    rows = cursor.fetchall()
    # Get column names from the cursor description
    headers = [description[0] for description in cursor.description]
    # Format the result as a table
    table = tabulate(rows, headers=headers, tablefmt="grid")
    # Close the cursor and connection
    cursor.close()
    conn.close()
    print(table)
    return table

def query_flows_with_slow_dns(input=""):
    # Connect to the SQLite database
    conn = sqlite3.connect('flows.db')  # Replace 'example.db' with the path to your SQLite database file
    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()
    cursor.execute(
        "SELECT DnsLatencyMs, DnsFlagsResponseCode, DnsId, DstAddr, DstPort, Interface, Proto, SrcAddr, SrcPort, Bytes, Packets FROM flow WHERE  DnsLatencyMs > " + str(SLOW_DNS_THRESHOULD_IN_MSECONDS) + " LIMIT 10"
    )

    # Fetch the results
    rows = cursor.fetchall()
    # Get column names from the cursor description
    headers = [description[0] for description in cursor.description]
    # Format the result as a table
    table = tabulate(rows, headers=headers, tablefmt="grid")
    # Close the cursor and connection
    cursor.close()
    conn.close()
    print(table)
    return table


if __name__ == '__main__':
    print("Netobserv flows with drops")
    print(query_flows_with_drop())
    print("Netobserv flows without drops")
    print(query_flows_without_drop())
    print("Netobserv flows with slow RTT")
    print(query_flows_with_slow_rtt())
    print("Netobserv flows with slow DNS")
    print(query_flows_with_slow_dns())
