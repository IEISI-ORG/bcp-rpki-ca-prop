#!/usr/bin/env python3
"""
RPKI Error Checker and Notifier

This script fetches RPKI validation errors from console.rpki-client.org,
categorizes them by CA operator, and sends notifications about the issues.
"""

import re
import json
import smtplib
import requests
from collections import defaultdict
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dataclasses import dataclass
from typing import List, Dict, Set
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class RPKIError:
    """Represents an RPKI validation error"""
    timestamp: str
    error_type: str
    repository: str
    file_path: str
    error_message: str
    severity: str

class RPKIErrorChecker:
    """Main class for checking RPKI errors and notifying CA operators"""
    
    def __init__(self, config_file='config.json'):
        """Initialize with configuration"""
        self.config = self.load_config(config_file)
        self.errors = []
        self.ca_contacts = self.config.get('ca_contacts', {})
        
    def load_config(self, config_file):
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Config file {config_file} not found. Using default configuration.")
            return self.get_default_config()
    
    def get_default_config(self):
        """Return default configuration"""
        return {
            "rpki_console_url": "https://console.rpki-client.org/",
            "email": {
                "smtp_server": "localhost",
                "smtp_port": 587,
                "username": "",
                "password": "",
                "from_address": "rpki-monitor@example.com"
            },
            "ca_contacts": {
                "rpki.ripe.net": ["noc@ripe.net"],
                "rpki.apnic.net": ["helpdesk@apnic.net"],
                "rpki.arin.net": ["hostmaster@arin.net"],
                "rpki.lacnic.net": ["registro@lacnic.net"],
                "rpki.afrinic.net": ["hostmaster@afrinic.net"],
                "rsync.paas.rpki.ripe.net": ["noc@ripe.net"],
                "rpki.sub.apnic.net": ["helpdesk@apnic.net"],
                "rpki-rps.arin.net": ["hostmaster@arin.net"],
                "rpki.cnnic.cn": ["service@cnnic.cn"],
                "rpki-repo.registro.br": ["hostmaster@registro.br"]
            },
            "severity_mapping": {
                "certificate has expired": "HIGH",
                "CRL has expired": "HIGH",
                "no valid manifest available": "MEDIUM",
                "seqnum gap detected": "MEDIUM",
                "certificate is not yet valid": "MEDIUM",
                "RFC 3779 resource not subset": "HIGH",
                "connect timeout": "LOW",
                "connect refused": "LOW",
                "no address associated": "LOW",
                "TLS handshake": "MEDIUM",
                "unexpected end of file": "LOW"
            }
        }
    
    def fetch_rpki_console_data(self):
        """Fetch the raw RPKI console output"""
        try:
            response = requests.get(self.config["rpki_console_url"], timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Failed to fetch RPKI console data: {e}")
            return None
    
    def parse_rpki_errors(self, console_data):
        """Parse RPKI errors from console output"""
        if not console_data:
            return []
        
        # Split into lines and find error lines
        lines = console_data.split('\n')
        errors = []
        
        # Pattern to match rpki-client error lines
        error_pattern = r'^(\w+\s+\d+\s+\d+:\d+:\d+)\s+rpki-client:\s+(.+?):\s+(.+)$'
        
        for line in lines:
            match = re.match(error_pattern, line.strip())
            if match:
                timestamp, location, message = match.groups()
                
                # Extract repository from location
                repo_match = re.search(r'([\w.-]+\.[\w.-]+)', location)
                repository = repo_match.group(1) if repo_match else "unknown"
                
                # Determine error type and severity
                error_type = self.categorize_error(message)
                severity = self.determine_severity(message)
                
                error = RPKIError(
                    timestamp=timestamp,
                    error_type=error_type,
                    repository=repository,
                    file_path=location,
                    error_message=message,
                    severity=severity
                )
                errors.append(error)
        
        return errors
    
    def categorize_error(self, message):
        """Categorize the error based on the message"""
        message_lower = message.lower()
        
        if "certificate has expired" in message_lower:
            return "EXPIRED_CERTIFICATE"
        elif "crl has expired" in message_lower:
            return "EXPIRED_CRL"
        elif "no valid manifest available" in message_lower:
            return "INVALID_MANIFEST"
        elif "seqnum gap detected" in message_lower:
            return "SEQUENCE_GAP"
        elif "certificate is not yet valid" in message_lower:
            return "PREMATURE_CERTIFICATE"
        elif "rfc 3779 resource not subset" in message_lower:
            return "RESOURCE_VIOLATION"
        elif "connect timeout" in message_lower or "connect refused" in message_lower:
            return "CONNECTION_ERROR"
        elif "no address associated" in message_lower:
            return "DNS_ERROR"
        elif "tls handshake" in message_lower:
            return "TLS_ERROR"
        elif "unexpected end of file" in message_lower:
            return "FILE_ERROR"
        else:
            return "OTHER"
    
    def determine_severity(self, message):
        """Determine severity based on error message"""
        message_lower = message.lower()
        
        for pattern, severity in self.config["severity_mapping"].items():
            if pattern.lower() in message_lower:
                return severity
        
        return "LOW"
    
    def group_errors_by_ca(self, errors):
        """Group errors by CA operator"""
        ca_errors = defaultdict(list)
        
        for error in errors:
            # Map repository to CA contact
            ca_contact = self.get_ca_contact(error.repository)
            if ca_contact:
                ca_errors[ca_contact].append(error)
            else:
                # Use repository as key if no specific contact found
                ca_errors[error.repository].append(error)
        
        return ca_errors
    
    def get_ca_contact(self, repository):
        """Get CA contact email(s) for a repository"""
        # Direct match
        if repository in self.ca_contacts:
            return repository
        
        # Pattern matching for subdomains
        for pattern, contacts in self.ca_contacts.items():
            if pattern in repository or repository.endswith(pattern):
                return pattern
        
        return None
    
    def generate_report(self, ca_errors):
        """Generate detailed error reports for each CA"""
        reports = {}
        
        for ca, errors in ca_errors.items():
            # Group by error type and severity
            error_summary = defaultdict(lambda: defaultdict(list))
            
            for error in errors:
                error_summary[error.severity][error.error_type].append(error)
            
            # Generate report text
            report = self.format_report(ca, error_summary, errors)
            reports[ca] = report
        
        return reports
    
    def format_report(self, ca, error_summary, all_errors):
        """Format a detailed error report for a CA"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
        
        report = f"""
RPKI Validation Errors Report
=============================
CA/Repository: {ca}
Generated: {timestamp}
Total Errors: {len(all_errors)}

EXECUTIVE SUMMARY
================
"""
        
        # Summary by severity
        for severity in ["HIGH", "MEDIUM", "LOW"]:
            if severity in error_summary:
                count = sum(len(errors) for errors in error_summary[severity].values())
                report += f"{severity} Priority: {count} errors\n"
        
        report += "\nDETAILED BREAKDOWN\n"
        report += "==================\n"
        
        # Detailed breakdown by severity and type
        for severity in ["HIGH", "MEDIUM", "LOW"]:
            if severity in error_summary:
                report += f"\n{severity} PRIORITY ISSUES:\n"
                report += "-" * (len(severity) + 18) + "\n"
                
                for error_type, errors in error_summary[severity].items():
                    report += f"\n{error_type} ({len(errors)} occurrences):\n"
                    
                    # Group similar errors
                    grouped = defaultdict(list)
                    for error in errors:
                        key = error.error_message
                        grouped[key].append(error)
                    
                    for message, error_list in grouped.items():
                        report += f"  • {message}\n"
                        if len(error_list) > 1:
                            report += f"    Affected files: {len(error_list)}\n"
                        else:
                            report += f"    File: {error_list[0].file_path}\n"
        
        report += "\nRECOMMENDED ACTIONS\n"
        report += "===================\n"
        report += self.get_recommendations(error_summary)
        
        report += "\n\nCONTACT INFORMATION\n"
        report += "===================\n"
        report += "This report was generated by an automated RPKI monitoring system.\n"
        report += "For questions or assistance, please contact: rpki-monitor@example.com\n"
        
        return report
    
    def get_recommendations(self, error_summary):
        """Generate recommendations based on error types"""
        recommendations = []
        
        if "HIGH" in error_summary:
            if "EXPIRED_CERTIFICATE" in error_summary["HIGH"]:
                recommendations.append("• URGENT: Renew expired certificates immediately to restore RPKI validation")
            if "EXPIRED_CRL" in error_summary["HIGH"]:
                recommendations.append("• URGENT: Update Certificate Revocation Lists (CRLs)")
            if "RESOURCE_VIOLATION" in error_summary["HIGH"]:
                recommendations.append("• URGENT: Fix resource certification - certificates contain resources not authorized by parent")
        
        if "MEDIUM" in error_summary:
            if "INVALID_MANIFEST" in error_summary["MEDIUM"]:
                recommendations.append("• Update or republish manifest files")
            if "SEQUENCE_GAP" in error_summary["MEDIUM"]:
                recommendations.append("• Check manifest sequence numbers for gaps")
            if "TLS_ERROR" in error_summary["MEDIUM"]:
                recommendations.append("• Review TLS configuration and certificates")
        
        if "LOW" in error_summary:
            if "CONNECTION_ERROR" in error_summary["LOW"]:
                recommendations.append("• Check network connectivity and firewall configurations")
            if "DNS_ERROR" in error_summary["LOW"]:
                recommendations.append("• Verify DNS configuration for repository hostnames")
        
        if not recommendations:
            recommendations.append("• Review specific error messages for appropriate corrective actions")
        
        return "\n".join(recommendations)
    
    def send_email_report(self, ca, report, contacts):
        """Send email report to CA contacts"""
        if not self.config["email"]["from_address"]:
            logger.warning("Email not configured. Skipping email notification.")
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config["email"]["from_address"]
            msg['To'] = ", ".join(contacts)
            msg['Subject'] = f"RPKI Validation Errors - {ca} - {datetime.now().strftime('%Y-%m-%d')}"
            
            msg.attach(MIMEText(report, 'plain'))
            
            # Send email
            smtp_server = smtplib.SMTP(
                self.config["email"]["smtp_server"], 
                self.config["email"]["smtp_port"]
            )
            
            if self.config["email"]["username"]:
                smtp_server.starttls()
                smtp_server.login(
                    self.config["email"]["username"], 
                    self.config["email"]["password"]
                )
            
            smtp_server.send_message(msg)
            smtp_server.quit()
            
            logger.info(f"Email report sent to {contacts} for {ca}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {contacts} for {ca}: {e}")
            return False
    
    def save_report_to_file(self, ca, report):
        """Save report to file"""
        filename = f"rpki_report_{ca.replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        try:
            with open(filename, 'w') as f:
                f.write(report)
            logger.info(f"Report saved to {filename}")
            return filename
        except Exception as e:
            logger.error(f"Failed to save report to {filename}: {e}")
            return None
    
    def run_check(self):
        """Main method to run the complete check and notification process"""
        logger.info("Starting RPKI error check...")
        
        # Fetch console data
        console_data = self.fetch_rpki_console_data()
        if not console_data:
            logger.error("No console data available")
            return False
        
        # Parse errors
        self.errors = self.parse_rpki_errors(console_data)
        logger.info(f"Found {len(self.errors)} RPKI errors")
        
        if not self.errors:
            logger.info("No errors found")
            return True
        
        # Group by CA
        ca_errors = self.group_errors_by_ca(self.errors)
        logger.info(f"Errors grouped into {len(ca_errors)} CA operators")
        
        # Generate and send reports
        reports = self.generate_report(ca_errors)
        
        for ca, report in reports.items():
            logger.info(f"Processing report for {ca}")
            
            # Save to file
            self.save_report_to_file(ca, report)
            
            # Get contacts and send email
            if ca in self.ca_contacts:
                contacts = self.ca_contacts[ca]
                self.send_email_report(ca, report, contacts)
            else:
                logger.warning(f"No contact information found for {ca}")
        
        # Generate summary
        self.generate_summary_report(ca_errors)
        
        logger.info("RPKI error check completed")
        return True
    
    def generate_summary_report(self, ca_errors):
        """Generate a summary report of all errors"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
        total_errors = sum(len(errors) for errors in ca_errors.values())
        
        summary = f"""
RPKI Validation Errors - Summary Report
=======================================
Generated: {timestamp}
Total CAs with errors: {len(ca_errors)}
Total errors: {total_errors}

BREAKDOWN BY CA:
"""
        
        # Sort CAs by error count
        sorted_cas = sorted(ca_errors.items(), key=lambda x: len(x[1]), reverse=True)
        
        for ca, errors in sorted_cas:
            severity_counts = defaultdict(int)
            for error in errors:
                severity_counts[error.severity] += 1
            
            summary += f"\n{ca}: {len(errors)} errors\n"
            for severity in ["HIGH", "MEDIUM", "LOW"]:
                if severity_counts[severity] > 0:
                    summary += f"  {severity}: {severity_counts[severity]}\n"
        
        # Save summary
        filename = f"rpki_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        try:
            with open(filename, 'w') as f:
                f.write(summary)
            logger.info(f"Summary report saved to {filename}")
        except Exception as e:
            logger.error(f"Failed to save summary report: {e}")
        
        print(summary)

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='RPKI Error Checker and Notifier')
    parser.add_argument('--config', '-c', default='config.json', 
                       help='Configuration file path (default: config.json)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Run without sending emails')
    
    args = parser.parse_args()
    
    # Create checker instance
    checker = RPKIErrorChecker(args.config)
    
    if args.dry_run:
        # Disable email sending for dry run
        checker.config["email"]["from_address"] = ""
        logger.info("Running in dry-run mode - no emails will be sent")
    
    # Run the check
    success = checker.run_check()
    
    if success:
        print("RPKI error check completed successfully")
    else:
        print("RPKI error check failed")
        exit(1)

if __name__ == "__main__":
    main()
