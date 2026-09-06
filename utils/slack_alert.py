import requests

def send_slack_alert(webhook_url: str, quality_score: float, total_rows: int, missing_vals: int):
    if not webhook_url:
        return
    
    status_emoji = "🟢" if quality_score > 90 else "🟡" if quality_score > 75 else "🔴"
    
    payload = {
        "text": f"{status_emoji} *Data Quality Alert* \n"
                f"• *Quality Score:* `{quality_score:.2f}%`\n"
                f"• *Total Rows:* `{total_rows}`\n"
                f"• *Missing Values:* `{missing_vals}`\n"
                f"Pipeline executed and logged to metadata store."
    }
    
    try:
        response = requests.post(webhook_url, json=payload)
        return response.status_code == 200
    except Exception as e:
        print(f"Slack webhook failed: {e}")
        return False