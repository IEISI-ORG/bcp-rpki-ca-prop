# USAGE INSTRUCTIONS:

1. Configure your settings:
   - Edit config.json with your SMTP settings and CA contacts
   - Update email addresses for notifications

2. Test the script (dry run - no emails sent):
   python3 rpki_checker.py --dry-run

3. Run the full check:
   python3 rpki_checker.py

4. Schedule regular checks with cron:
   # Add to crontab (runs every 6 hours):
   0 */6 * * * /path/to/rpki_env/bin/python /path/to/rpki_checker.py

5. Check generated reports:
   ls -la rpki_report_*.txt
   ls -la rpki_summary_*.txt

# FEATURES:

• Fetches latest RPKI errors from console.rpki-client.org
• Categorizes errors by type and severity (HIGH/MEDIUM/LOW)
• Groups errors by CA operator
• Generates detailed reports with recommendations
• Sends email notifications to CA operators
• Saves reports to files for record keeping
• Provides summary statistics

# ERROR TYPES DETECTED:

• Expired certificates (HIGH priority)
• Expired CRLs (HIGH priority)
• Invalid manifests (MEDIUM priority)
• Sequence number gaps (MEDIUM priority)
• Resource violations (HIGH priority)
• Connection errors (LOW priority)
• DNS issues (LOW priority)
• TLS problems (MEDIUM priority)

# CONFIGURATION:

Edit config.json to customize:
• Email server settings
• CA operator contact information
• Error severity mappings
• Notification preferences

# TROUBLESHOOTING:

• Check logs for detailed error information
• Verify network connectivity to console.rpki-client.org
• Test SMTP settings with a simple email client
• Ensure CA contact emails are up to date

