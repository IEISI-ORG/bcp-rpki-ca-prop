#!/bin/bash
# RPKI Error Checker Setup Script

echo "Setting up RPKI Error Checker..."

# Create virtual environment
python3 -m venv rpki_env
source rpki_env/bin/activate

# Install required packages
pip install requests

# Create directory structure
mkdir -p rpki_reports
mkdir -p logs

echo "Setup complete!"
echo ""
echo "USAGE INSTRUCTIONS:"
echo "=================="
echo ""
echo "1. Configure your settings:"
echo "   - Edit config.json with your SMTP settings and CA contacts"
echo "   - Update email addresses for notifications"
echo ""
echo "2. Test the script (dry run - no emails sent):"
echo "   python3 rpki_checker.py --dry-run"
echo ""
echo "3. Run the full check:"
echo "   python3 rpki_checker.py"
echo ""
echo "4. Schedule regular checks with cron:"
echo "   # Add to crontab (runs every 6 hours):"
echo "   0 */6 * * * /path/to/rpki_env/bin/python /path/to/rpki_checker.py"
echo ""
echo "5. Check generated reports:"
echo "   ls -la rpki_report_*.txt"
echo "   ls -la rpki_summary_*.txt"
echo ""
echo "FEATURES:"
echo "========="
echo "• Fetches latest RPKI errors from console.rpki-client.org"
echo "• Categorizes errors by type and severity (HIGH/MEDIUM/LOW)"
echo "• Groups errors by CA operator"
echo "• Generates detailed reports with recommendations"
echo "• Sends email notifications to CA operators"
echo "• Saves reports to files for record keeping"
echo "• Provides summary statistics"
echo ""
echo "ERROR TYPES DETECTED:"
echo "===================="
echo "• Expired certificates (HIGH priority)"
echo "• Expired CRLs (HIGH priority)"
echo "• Invalid manifests (MEDIUM priority)"
echo "• Sequence number gaps (MEDIUM priority)"
echo "• Resource violations (HIGH priority)"
echo "• Connection errors (LOW priority)"
echo "• DNS issues (LOW priority)"
echo "• TLS problems (MEDIUM priority)"
echo ""
echo "CONFIGURATION:"
echo "=============="
echo "Edit config.json to customize:"
echo "• Email server settings"
echo "• CA operator contact information"
echo "• Error severity mappings"
echo "• Notification preferences"
echo ""
echo "TROUBLESHOOTING:"
echo "==============="
echo "• Check logs for detailed error information"
echo "• Verify network connectivity to console.rpki-client.org"
echo "• Test SMTP settings with a simple email client"
echo "• Ensure CA contact emails are up to date"