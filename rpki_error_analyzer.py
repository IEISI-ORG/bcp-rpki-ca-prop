#!/usr/bin/env python3
"""
RPKI-Client Error Log Analyzer
Analyzes error output from rpki-client console logs
"""

import re
import sys
import json
import argparse
from collections import defaultdict, Counter
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import requests
from urllib.parse import urlparse

class RPKIErrorAnalyzer:
    def __init__(self):
        self.error_patterns = {
            'connection_timeout': r'connect timeout',
            'connection_refused': r'connect refused',
            'no_route_to_host': r'No route to host',
            'dns_resolution_failed': r'no address associated with name',
            'crl_expired': r'CRL has expired',
            'cert_expired': r'certificate has expired',
            'cert_not_yet_valid': r'certificate is not yet valid',
            'manifest_unavailable': r'no valid manifest available',
            'seqnum_gap': r'seqnum gap detected',
            'tls_handshake_failed': r'TLS handshake.*certificate verification failed',
            'unexpected_manifest_number': r'unexpected manifest number',
            'rfc3779_resource_violation': r'RFC 3779 resource not subset',
            'notification_not_modified': r'notification file not modified',
            'fallback_to_rsync': r'fallback to rsync',
            'fallback_to_cache': r'fallback to cache',
            'cross_origin_redirect': r'cross origin redirect',
            'unexpected_end_of_file': r'unexpected end of file',
            'invalid_vcard': r'invalid vCard'
        }
        
        self.results = {
            'error_counts': defaultdict(int),
            'error_details': defaultdict(list),
            'affected_hosts': defaultdict(set),
            'timeline': [],
            'summary_stats': {},
            'recommendations': []
        }

    def parse_log_line(self, line: str) -> Optional[Dict]:
        """Parse a single log line and extract structured information"""
        # Extract timestamp
        timestamp_pattern = r'^(\w{3}\s+\d{2}\s+\d{2}:\d{2}:\d{2})'
        timestamp_match = re.search(timestamp_pattern, line)
        timestamp = timestamp_match.group(1) if timestamp_match else None
        
        # Extract host/URL information
        url_pattern = r'https?://([^/\s:]+)'
        rsync_pattern = r'rsync://([^/\s:]+)'
        path_pattern = r'([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
        
        host = None
        url_match = re.search(url_pattern, line)
        if url_match:
            host = url_match.group(1)
        else:
            rsync_match = re.search(rsync_pattern, line)
            if rsync_match:
                host = rsync_match.group(1)
            else:
                path_match = re.search(path_pattern, line)
                if path_match:
                    host = path_match.group(1)
        
        # Identify error types
        error_types = []
        for error_type, pattern in self.error_patterns.items():
            if re.search(pattern, line, re.IGNORECASE):
                error_types.append(error_type)
        
        if not error_types:
            return None
            
        return {
            'timestamp': timestamp,
            'host': host,
            'error_types': error_types,
            'raw_line': line.strip(),
            'severity': self.classify_severity(error_types)
        }

    def classify_severity(self, error_types: List[str]) -> str:
        """Classify error severity based on error types"""
        high_severity = ['cert_expired', 'cert_not_yet_valid', 'rfc3779_resource_violation']
        medium_severity = ['crl_expired', 'manifest_unavailable', 'seqnum_gap']
        
        if any(error in high_severity for error in error_types):
            return 'HIGH'
        elif any(error in medium_severity for error in error_types):
            return 'MEDIUM'
        else:
            return 'LOW'

    def analyze_log_content(self, content: str):
        """Analyze log content and extract error patterns"""
        lines = content.split('\n')
        
        for line in lines:
            if 'rpki-client:' not in line and 'openrsync:' not in line:
                continue
                
            parsed = self.parse_log_line(line)
            if not parsed:
                continue
                
            # Update counters
            for error_type in parsed['error_types']:
                self.results['error_counts'][error_type] += 1
                self.results['error_details'][error_type].append({
                    'timestamp': parsed['timestamp'],
                    'host': parsed['host'],
                    'message': parsed['raw_line'],
                    'severity': parsed['severity']
                })
                
                if parsed['host']:
                    self.results['affected_hosts'][error_type].add(parsed['host'])
            
            self.results['timeline'].append(parsed)

    def analyze_file(self, filepath: str):
        """Analyze errors from a log file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            self.analyze_log_content(content)
        except FileNotFoundError:
            print(f"Error: File '{filepath}' not found")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file: {e}")
            sys.exit(1)

    def fetch_console_data(self, url: str = "https://console.rpki-client.org/"):
        """Fetch current error data from RPKI console"""
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            self.analyze_log_content(response.text)
            print(f"Successfully fetched data from {url}")
        except requests.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
            sys.exit(1)

    def generate_summary(self) -> Dict:
        """Generate summary statistics"""
        total_errors = sum(self.results['error_counts'].values())
        unique_hosts = set()
        for hosts in self.results['affected_hosts'].values():
            unique_hosts.update(hosts)
        
        severity_counts = Counter()
        for entry in self.results['timeline']:
            severity_counts[entry['severity']] += 1
        
        self.results['summary_stats'] = {
            'total_errors': total_errors,
            'unique_error_types': len(self.results['error_counts']),
            'affected_hosts_count': len(unique_hosts),
            'severity_breakdown': dict(severity_counts),
            'most_common_errors': dict(Counter(self.results['error_counts']).most_common(10))
        }
        
        return self.results['summary_stats']

    def generate_recommendations(self):
        """Generate recommendations based on error analysis"""
        recommendations = []
        
        # Network connectivity issues
        network_errors = ['connection_timeout', 'connection_refused', 'no_route_to_host', 'dns_resolution_failed']
        if any(self.results['error_counts'][error] > 0 for error in network_errors):
            recommendations.append({
                'category': 'Network Connectivity',
                'priority': 'HIGH',
                'description': 'Multiple network connectivity issues detected',
                'action': 'Check network connectivity, firewall rules, and DNS resolution for affected hosts'
            })
        
        # Certificate issues
        if self.results['error_counts']['cert_expired'] > 0:
            recommendations.append({
                'category': 'Certificate Management',
                'priority': 'HIGH',
                'description': f"{self.results['error_counts']['cert_expired']} expired certificates found",
                'action': 'Contact CA operators to renew expired certificates'
            })
        
        # CRL issues
        if self.results['error_counts']['crl_expired'] > 0:
            recommendations.append({
                'category': 'CRL Management',
                'priority': 'MEDIUM',
                'description': f"{self.results['error_counts']['crl_expired']} expired CRLs found",
                'action': 'CA operators should update Certificate Revocation Lists'
            })
        
        # Manifest issues
        if self.results['error_counts']['manifest_unavailable'] > 0:
            recommendations.append({
                'category': 'Manifest Management',
                'priority': 'MEDIUM',
                'description': f"{self.results['error_counts']['manifest_unavailable']} invalid manifests found",
                'action': 'CA operators should regenerate and publish valid manifests'
            })
        
        # Sequence number gaps
        if self.results['error_counts']['seqnum_gap'] > 0:
            recommendations.append({
                'category': 'Repository Synchronization',
                'priority': 'LOW',
                'description': f"{self.results['error_counts']['seqnum_gap']} sequence number gaps detected",
                'action': 'Monitor repository synchronization and consider cache refresh'
            })
        
        self.results['recommendations'] = recommendations

    def print_summary(self):
        """Print a human-readable summary of the analysis"""
        stats = self.generate_summary()
        self.generate_recommendations()
        
        print("\n" + "="*80)
        print("RPKI-CLIENT ERROR ANALYSIS SUMMARY")
        print("="*80)
        
        print(f"\nOVERALL STATISTICS:")
        print(f"  Total Errors: {stats['total_errors']}")
        print(f"  Unique Error Types: {stats['unique_error_types']}")
        print(f"  Affected Hosts: {stats['affected_hosts_count']}")
        
        print(f"\nERROR SEVERITY BREAKDOWN:")
        for severity, count in stats['severity_breakdown'].items():
            print(f"  {severity}: {count}")
        
        print(f"\nTOP 10 MOST COMMON ERRORS:")
        for error_type, count in stats['most_common_errors'].items():
            print(f"  {error_type.replace('_', ' ').title()}: {count}")
        
        print(f"\nAFFECTED HOSTS BY ERROR TYPE:")
        for error_type, hosts in self.results['affected_hosts'].items():
            if hosts:
                print(f"  {error_type.replace('_', ' ').title()}: {len(hosts)} hosts")
                for host in sorted(hosts)[:5]:  # Show first 5 hosts
                    print(f"    - {host}")
                if len(hosts) > 5:
                    print(f"    ... and {len(hosts) - 5} more")
        
        print(f"\nRECOMMENDATIONS:")
        for i, rec in enumerate(self.results['recommendations'], 1):
            print(f"  {i}. [{rec['priority']}] {rec['category']}")
            print(f"     {rec['description']}")
            print(f"     Action: {rec['action']}\n")

    def export_json(self, filename: str):
        """Export results to JSON file"""
        # Convert sets to lists for JSON serialization
        export_data = dict(self.results)
        export_data['affected_hosts'] = {k: list(v) for k, v in self.results['affected_hosts'].items()}
        
        try:
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
            print(f"Results exported to {filename}")
        except Exception as e:
            print(f"Error exporting to JSON: {e}")

    def export_csv(self, filename: str):
        """Export error details to CSV file"""
        import csv
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Timestamp', 'Host', 'Error_Type', 'Severity', 'Message'])
                
                for error_type, details in self.results['error_details'].items():
                    for detail in details:
                        writer.writerow([
                            detail['timestamp'],
                            detail['host'],
                            error_type,
                            detail['severity'],
                            detail['message']
                        ])
            print(f"Error details exported to {filename}")
        except Exception as e:
            print(f"Error exporting to CSV: {e}")

def main():
    parser = argparse.ArgumentParser(description='Analyze RPKI-client error logs')
    parser.add_argument('-f', '--file', help='Path to log file to analyze')
    parser.add_argument('-u', '--url', help='URL to fetch live data from', 
                       default='https://console.rpki-client.org/')
    parser.add_argument('-j', '--json', help='Export results to JSON file')
    parser.add_argument('-c', '--csv', help='Export error details to CSV file')
    parser.add_argument('--no-fetch', action='store_true', 
                       help='Skip fetching live data (only use with --file)')
    
    args = parser.parse_args()
    
    if not args.file and args.no_fetch:
        print("Error: --no-fetch requires --file to be specified")
        sys.exit(1)
    
    analyzer = RPKIErrorAnalyzer()
    
    # Analyze file if provided
    if args.file:
        print(f"Analyzing log file: {args.file}")
        analyzer.analyze_file(args.file)
    
    # Fetch live data unless explicitly disabled
    if not args.no_fetch:
        print(f"Fetching live data from: {args.url}")
        analyzer.fetch_console_data(args.url)
    
    # Generate and display summary
    analyzer.print_summary()
    
    # Export results if requested
    if args.json:
        analyzer.export_json(args.json)
    
    if args.csv:
        analyzer.export_csv(args.csv)

if __name__ == '__main__':
    main()
