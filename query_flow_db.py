#!/usr/bin/python3

import sqlite3

SLOW_RTT_THRESHOULD_IN_NANOSECONDS = 20000000

def query_flows_with_drop(input=""):
    # Connect to the SQLite database
    conn = sqlite3.connect('flows.db')  # Replace 'example.db' with the path to your SQLite database file
    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()
    cursor.execute(
        "SELECT PktDropLatestDropCause, DstAddr, DstPort, Interface, Proto, SrcAddr, SrcPort FROM flow WHERE PktDropLatestDropCause != 0"
    )

    # Fetch the results
    rows = cursor.fetchall()
    # Close the cursor and connection
    cursor.close()
    conn.close()
    return rows


def query_flows_without_drop(input=""):
    # Connect to the SQLite database
    conn = sqlite3.connect('flows.db')  # Replace 'example.db' with the path to your SQLite database file
    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()
    # Execute a SELECT query
    cursor.execute("SELECT DstAddr, DstPort, Interface, Proto, SrcAddr, SrcPort FROM flow")

    # Fetch the results
    rows = cursor.fetchall()
    # Close the cursor and connection
    cursor.close()
    conn.close()
    return rows

def query_flows_with_slow_rtt(input=""):
    # Connect to the SQLite database
    conn = sqlite3.connect('flows.db')  # Replace 'example.db' with the path to your SQLite database file
    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()
    cursor.execute(
        "SELECT TimeFlowRTTNs, DstAddr, DstPort, Interface, Proto, SrcAddr, SrcPort FROM flow WHERE  TimeFlowRTTNs > " + str(SLOW_RTT_THRESHOULD_IN_NANOSECONDS)
    )

    # Fetch the results
    rows = cursor.fetchall()
    # Close the cursor and connection
    cursor.close()
    conn.close()
    return rows

def print_flows(rows):
    for row in rows:
        print(row)


if __name__ == '__main__':
    print("Netobserv flows with drops")
    print_flows(query_flows_with_drop())
    print("Netobserv flows without drops")
    print_flows(query_flows_without_drop())
    print("Netobserv flows with slow RTT")
    print_flows(query_flows_with_slow_rtt())
