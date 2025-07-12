#!/usr/bin/env python3
"""
Nginx インストール・起動・自動起動設定スクリプト
対応OS: AlmaLinux 9
"""

import subprocess
import sys
import os

def run_command(command):
    """コマンドを実行して結果を返す"""
    try:
        # sudoを付けて実行
        if not command.startswith('sudo') and os.geteuid() != 0:
            command = f"sudo {command}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    print("=== AlmaLinux 9 Nginx セットアップ ===\n")
    
    # 1. Nginxをインストール
    print("1. Nginxをインストールしています...")
    success, stdout, stderr = run_command("dnf install -y nginx")
    if not success:
        print(f"エラー: インストールに失敗しました\n{stderr}")
        sys.exit(1)
    print("✓ インストール完了\n")
    
    # 2. Nginxを起動
    print("2. Nginxを起動しています...")
    success, stdout, stderr = run_command("systemctl start nginx")
    if not success:
        print(f"エラー: 起動に失敗しました\n{stderr}")
        sys.exit(1)
    print("✓ 起動完了\n")
    
    # 3. 自動起動を有効化
    print("3. 自動起動を設定しています...")
    success, stdout, stderr = run_command("systemctl enable nginx")
    if not success:
        print(f"エラー: 自動起動設定に失敗しました\n{stderr}")
        sys.exit(1)
    print("✓ 自動起動設定完了\n")
    
    # 4. ステータス確認
    print("4. 動作確認")
    success, stdout, _ = run_command("systemctl is-active nginx")
    if success and "active" in stdout:
        print("✓ Nginx: 稼働中")
    else:
        print("✗ Nginx: 停止中")
    
    success, stdout, _ = run_command("systemctl is-enabled nginx")
    if success and "enabled" in stdout:
        print("✓ 自動起動: 有効")
    else:
        print("✗ 自動起動: 無効")
    
    # IPアドレスを取得
    success, stdout, _ = run_command("hostname -I | awk '{print $1}'")
    ip = stdout.strip() if success and stdout.strip() else "サーバーIP"
    
    print("\n=== セットアップ完了 ===")
    print(f"ブラウザで以下にアクセスして確認してください:")
    print(f"  http://localhost")
    print(f"  http://{ip}")

if __name__ == "__main__":
    main()