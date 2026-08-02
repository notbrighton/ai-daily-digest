import os
import datetime

def export_markdown(content: str, output_dir: str = "digests") -> str:
    os.makedirs(output_dir, exist_ok=True)
    today_str = datetime.date.today().strftime("%Y%m%d")
    filepath = os.path.join(output_dir, f"digest_{today_str}.md")
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
        
    return filepath
