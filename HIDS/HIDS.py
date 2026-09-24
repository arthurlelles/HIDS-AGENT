#!/usr/bin/env python3
import builtins
import os
import time
import subprocess
import typer
import threading

app = typer.Typer()

# -------------------------
# CONFIG
# -------------------------
MAPA_LOGS = {
    "nginx": "/var/log/nginx/error.log",
    "ssh": "journald",
}

monitorados = set()

# -------------------------
# COLETORES
# -------------------------
def tail_f(path: str):
    with builtins.open(path, "r", encoding="utf-8", errors="replace") as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if line:
                yield line
            else:
                time.sleep(0.2)

def journal():
    cmd = ["journalctl", "-f", "-o", "cat"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)
    assert proc.stdout is not None
    for line in proc.stdout:
        yield line

# -------------------------
# REGRA
# -------------------------
def rule_alert(line: str) -> bool:
    low = line.lower()
    keywords = ["failed", "warning", "error", "crash", "segfault"]
    return any(k in low for k in keywords)

# -------------------------
# PROCESSAMENTO
# -------------------------
def process_line(source: str, line: str):
    if rule_alert(line):
        typer.echo(f"[{source}] ALERTA: {line.rstrip()}")

# -------------------------
# THREADS
# -------------------------
def run_journal():
    for line in journal():
        process_line("journal", line)

def run_file(path: str):
    for line in tail_f(path):
        process_line(path, line)

# -------------------------
# DETECTOR DE PROCESSOS
# -------------------------
def scan_processes():
    while True:
        result = subprocess.run(
            ["ps", "-e", "-o", "comm="],
            stdout=subprocess.PIPE,
            text=True
        )

        processos = result.stdout.splitlines()

        for proc in processos:
            if proc in monitorados:
                continue

            source = MAPA_LOGS.get(proc)

            # ignora desconhecidos e journald (já temos global)
            if source and source != "journald" and os.path.exists(source):
                typer.echo(f"[+] Monitorando {proc} → {source}")

                t = threading.Thread(target=run_file, args=(source,), daemon=True)
                t.start()

                monitorados.add(proc)

        time.sleep(2)

# -------------------------
# MAIN
# -------------------------
def run():
    typer.echo("[+] SOC iniciado")

    # journald sempre rodando
    threading.Thread(target=run_journal, daemon=True).start()

    # detector de processos
    scan_processes()

@app.callback(invoke_without_command=True)
def main():
    run()

if __name__ == "__main__":
    app()
