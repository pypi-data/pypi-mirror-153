"""
Script for simulating the MQTT messages coming from pyaware slave. Using imac2 as a base.
Responds to the commands being sent to it on local mqtt broker.
Has CLI interface for setting options
"""
import pyaware

if __name__ == "__main__":
    pyaware.main()
