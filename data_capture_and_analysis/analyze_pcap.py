from elasticsearch import Elasticsearch
import pyshark
from datetime import datetime, timezone

def analyze_pcap(pcap_file):
    es = Elasticsearch(['http://localhost:9200'])
    capture = pyshark.FileCapture(pcap_file)

    for packet in capture:
        try:
            current_time = datetime.now(timezone.utc)
            packet_data = {
                'timestamp': current_time.isoformat(),
                'protocol': str(packet.highest_layer),
                'length': int(packet.length)
            }

            if hasattr(packet, 'ip'):
                packet_data.update({
                    'source_ip': str(packet.ip.src),
                    'dest_ip': str(packet.ip.dst)
                })

            if hasattr(packet, 'tcp'):
                packet_data.update({
                    'source_port': int(packet.tcp.srcport),
                    'dest_port': int(packet.tcp.dstport)
                })

            es.index(index='network-analysis', document=packet_data)
            print(f"Paquet indexé: {packet.highest_layer}")

        except Exception as e:
            print(f"Erreur: {e}")
            continue

    capture.close()

if __name__ == "__main__":
    analyze_pcap("capture.pcap")
