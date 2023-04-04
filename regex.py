import re, os
import pandas as pd
from glob import glob

pattern = r'(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d+)\s\|\sBlocked\s.*Method\s=\s(\w+)\s.*requestor_domain\s=\s([\w.-]+)\s.*requestor_ip\s=\s([\d.]+)\s.*Referer\s=\s(https?://\S+)\s.*is_allowed_ip\s=\s(\w+)\s.*is_allowed_domain\s=\s(\w+)\s.*is_allowed\s=\s(\w+)'

date_time = []
method = []
requestor_domain = []
requestor_ip = []
referer = []
is_allowed_ip = []
is_allowed_domain = []
is_allowed = []

directory = os.getcwd()
txt_files = glob(directory + "/logs/*.txt")

for file_path in txt_files:
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            result = re.search(pattern, line)
            if result:
                date_time.append(result.group(1))
                method.append(result.group(2))
                requestor_domain.append(result.group(3))
                requestor_ip.append(result.group(4))
                referer.append(result.group(5))
                is_allowed_ip.append(result.group(6))
                is_allowed_domain.append(result.group(7))
                is_allowed.append(result.group(8))

result = {
    "date_time": date_time,
    "method": method,
    "requestor_domain": requestor_domain,
    "requestor_ip": requestor_ip,
    "referer": referer,
    "is_allowed_ip": is_allowed_ip,
    "is_allowed_domain": is_allowed_domain,
    "is_allowed": is_allowed
}

df = pd.DataFrame(result)
df.to_excel("Log de Bloqueios nas APIs.xlsx", index=False)
df.drop_duplicates(subset="requestor_domain", inplace=True)
df.to_excel("Log de Bloqueios nas APIs Sem Duplicados.xlsx", index=False)
print(df)
