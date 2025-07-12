#!/usr/bin/env python3
"""
AlmaLinux システムアップデートスクリプト（シンプル版）
"""

import subprocess
import sys
import os

def check_root():
    """root権限チェック、必要なら自動的にsudoで再実行"""
    if os.geteuid() != 0:
        print("🔐 root権限が必要です。sudoで再実行します...")
        # 現在のPythonインタープリタとスクリプトのパスを取得
        python_exe = sys.executable
        script_path = os.path.abspath(sys.argv[0])
        
        # sudoで再実行
        try:
            os.execvp('sudo', ['sudo', python_exe, script_path] + sys.argv[1:])
        except Exception as e:
            print(f"❌ sudoでの再実行に失敗しました: {e}")
            print("手動で以下のコマンドを実行してください:")
            print(f"sudo {python_exe} {script_path}")
            sys.exit(1)

def run_command(cmd):
    """コマンド実行"""
    print(f"\n📌 実行中: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    return result.returncode == 0

def main():
    check_root()
    
    print("🔄 AlmaLinux システムアップデート開始")
    print("=" * 50)
    
    # 1. キャッシュ更新
    if not run_command(["dnf", "makecache"]):
        print("❌ キャッシュ更新に失敗しました")
        sys.exit(1)
    
    # 2. アップデート実行
    print("\n📦 パッケージをアップデートしています...")
    if not run_command(["dnf", "update", "-y"]):
        print("❌ アップデートに失敗しました")
        sys.exit(1)
    
    # 3. 不要パッケージ削除
    print("\n🧹 不要なパッケージを削除しています...")
    run_command(["dnf", "autoremove", "-y"])
    
    # 4. キャッシュクリーン
    print("\n🧹 キャッシュをクリーンアップしています...")
    run_command(["dnf", "clean", "all"])
    
    print("\n✅ アップデート完了！")
    print("=" * 50)

if __name__ == "__main__":
    main()
    