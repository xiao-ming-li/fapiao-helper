import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import sys

def select_folder():
    folder = filedialog.askdirectory(title="请选择存放发票的文件夹")
    if folder:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, folder)

def start_process():
    folder = entry_path.get()
    if not folder:
        messagebox.showwarning("提示", "请先选择发票文件夹！")
        return

    # 获取 invoice_agent.exe 所在的真实路径
    if getattr(sys, 'frozen', False):
        # 打包后运行
        app_dir = os.path.dirname(sys.executable)
    else:
        # 开发环境
        app_dir = os.path.dirname(os.path.abspath(__file__))

    agent_exe = os.path.join(app_dir, "invoice_agent.exe")
    if not os.path.exists(agent_exe):
        messagebox.showerror("错误", f"找不到引擎文件：{agent_exe}\n请确保 invoice_agent.exe 和本程序在同一个文件夹里！")
        return

    btn_start.config(state=tk.DISABLED, text="正在处理...")
    lbl_status.config(text="正在读取发票，请稍候...")
    root.update()

    # 调用引擎执行发票处理
    cmd = [
        agent_exe,
        folder,
        "-o", folder,
        "--mark-reimbursed",
        "--save-json"
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        if result.returncode == 0:
            lbl_status.config(text="处理完成！")
            messagebox.showinfo("成功", "发票处理完成！Excel 文件已生成在发票文件夹中。")
        else:
            lbl_status.config(text="处理失败")
            messagebox.showerror("失败", f"处理失败：\n{result.stderr[:500]}")
    except Exception as e:
        lbl_status.config(text="发生错误")
        messagebox.showerror("错误", f"运行时发生错误：\n{e}")
    finally:
        btn_start.config(state=tk.NORMAL, text="开始处理")

# 创建窗口界面
root = tk.Tk()
root.title("发票报销助手")
root.geometry("500x250")
root.resizable(False, False)

# 提示文字
tk.Label(root, text="发票文件夹路径：", font=("微软雅黑", 11)).pack(pady=10)

# 路径输入框和选择按钮
frame = tk.Frame(root)
frame.pack(pady=5)
entry_path = tk.Entry(frame, width=40, font=("微软雅黑", 10))
entry_path.pack(side=tk.LEFT, padx=5)
btn_select = tk.Button(frame, text="选择目录", command=select_folder, font=("微软雅黑", 10))
btn_select.pack(side=tk.LEFT)

# 状态显示
lbl_status = tk.Label(root, text="请选择文件夹后点击开始", font=("微软雅黑", 10), fg="gray")
lbl_status.pack(pady=15)

# 开始按钮
btn_start = tk.Button(root, text="开始处理", command=start_process, font=("微软雅黑", 12, "bold"), bg="#2c3e50", fg="white", width=15, height=2)
btn_start.pack(pady=5)

root.mainloop()