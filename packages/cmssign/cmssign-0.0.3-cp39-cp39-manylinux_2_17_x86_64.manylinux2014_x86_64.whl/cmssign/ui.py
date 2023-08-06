#!/usr/bin/env python3
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===========================================================================

import os
import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog as filedialog
try:
    from cmssign.cmssign import sign_cms, sign_tsa, append_tsa_to_cms, get_time
except ImportError:
    from cmssign import sign_cms, sign_tsa, append_tsa_to_cms


class App(object):
    PATH_WIDTH = 50
    NAME_WIDTH = 15

    def __init__(self):
        self.win = tk.Tk()
        self.win.title("Cryptographic Message Syntax Sign Tool")
        self.init_win()
    
    def init_win(self):
        # row 0
        tk.Label(self.win, text = "待签名文件:", anchor='e', width=App.NAME_WIDTH).grid(row=0, column=0,sticky=tk.W)
        self.lb_file = tk.Label(self.win, text = "请选择文件路径", anchor='w', width=App.PATH_WIDTH)
        self.lb_file.grid(row=0, column=1, columnspan=3, sticky=tk.W)
        self.btn_file = tk.Button(self.win, text="选择文件", width=10, command=self.choosefile)
        self.btn_file.grid(row=0, column=4)

        # row 1
        tk.Label(self.win, text = "签名证书:", anchor='e', width=App.NAME_WIDTH).grid(row=1, column=0, sticky=tk.W)
        self.lb_cert = tk.Label(self.win, text = "请选择文件路径", anchor='w', width=App.PATH_WIDTH)
        self.lb_cert.grid(row=1, column=1, columnspan=3, sticky=tk.W)
        self.btn_cert = tk.Button(self.win, text="选择文件", width=10, command=self.choosecert)
        self.btn_cert.grid(row=1, column=4)

        # row 2
        tk.Label(self.win, text = "签名私钥:", anchor='e', width=App.NAME_WIDTH).grid(row=2, column=0, sticky=tk.W)
        self.lb_priv = tk.Label(self.win, text = "请选择文件路径", anchor='w', width=App.PATH_WIDTH)
        self.lb_priv.grid(row=2, column=1, columnspan=3, sticky=tk.W)
        self.btn_priv = tk.Button(self.win, text="选择文件", width=10, command=self.choosepriv)
        self.btn_priv.grid(row=2, column=4)

        # row 3
        tk.Label(self.win, text = "时间戳签名证书:", anchor='e', width=App.NAME_WIDTH).grid(row=3, column=0, sticky=tk.W)
        self.lb_tscert = tk.Label(self.win, text = "请选择文件路径", anchor='w', width=App.PATH_WIDTH)
        self.lb_tscert.grid(row=3, column=1, columnspan=3, sticky=tk.W)
        self.btn_tscert = tk.Button(self.win, text="选择文件", width=10, command=self.choosetscert)
        self.btn_tscert.grid(row=3, column=4)

        # row 4
        tk.Label(self.win, text = "时间戳签名私钥:", anchor='e', width=App.NAME_WIDTH).grid(row=4, column=0, sticky=tk.W)
        self.lb_tspriv = tk.Label(self.win, text = "请选择文件路径", anchor='w', width=App.PATH_WIDTH)
        self.lb_tspriv.grid(row=4, column=1, columnspan=3, sticky=tk.W)
        self.btn_tspriv = tk.Button(self.win, text="选择文件", width=10, command=self.choosetspriv)
        self.btn_tspriv.grid(row=4, column=4)

        # row 5
        tk.Label(self.win, text = "使用自定义时间:", anchor='e', width=App.NAME_WIDTH).grid(row=5, column=0, sticky=tk.W)
        self.ck_btn_state = tk.IntVar()
        self.ck_btn = tk.Checkbutton(self.win, command=self.doCheckBtn, variable=self.ck_btn_state)
        self.ck_btn.grid(row=5, column=1, sticky=tk.W)

        # row 6
        self.timestamp = tk.StringVar()
        tk.Label(self.win, text = "签名时间戳:", anchor='e', width=App.NAME_WIDTH).grid(row=6, column=0, sticky=tk.W)
        self.ts_entry = tk.Entry(self.win, textvariable=self.timestamp)
        self.ts_entry.grid(row=6, column=1, sticky='we')
        self.ts_entry.config(state='disabled')
        print(self.ts_entry)

        # row 7
        self.combine_ts_to_cms = tk.IntVar()
        self.ts_combine_ck = tk.Checkbutton(self.win, variable=self.combine_ts_to_cms)
        self.ts_combine_ck.grid(row=7, column=0, sticky=tk.E)
        tk.Label(self.win, text = "合并时间戳文件到cms文件的未签名属性中", anchor='w', width=20).grid(row=7, column=1, sticky=tk.W)
        # row 8
        self.btn_sign = tk.Button(self.win, text="签名", width=App.PATH_WIDTH, command=self.sign)
        self.btn_sign.grid(row=8, column=1, columnspan=3, sticky=tk.W)

        # end
        tk.Label(self.win, width=0).grid(row=8, column=0)

    def doCheckBtn(self):
        if self.ck_btn_state.get() == 1:
            self.ts_entry.config(state='normal')
        else:
            self.ts_entry.config(state='disabled')

    def choosefile(self):
        tkfile = filedialog.askopenfile(title="选择待签名文件")
        if tkfile:
            self.lb_file.config(text=tkfile.name)

    def choosecert(self):
        tkfile = filedialog.askopenfile(title="选择签名证书")
        if tkfile:
            self.lb_cert.config(text=tkfile.name)

    def choosepriv(self):
        tkfile = filedialog.askopenfile(title="选择签名私钥")
        if tkfile:
            self.lb_priv.config(text=tkfile.name)

    def choosetscert(self):
        tkfile = filedialog.askopenfile(title="选择时间戳签名证书")
        if tkfile:
            self.lb_tscert.config(text=tkfile.name)

    def choosetspriv(self):
        tkfile = filedialog.askopenfile(title="选择时间戳签名私钥")
        if tkfile:
            self.lb_tspriv.config(text=tkfile.name)
    
    def sign(self):
        file_name = self.lb_file.cget('text')
        cert = self.lb_cert.cget('text')
        priv = self.lb_priv.cget('text')
        tscert = self.lb_tscert.cget('text')
        tspriv = self.lb_tspriv.cget('text')

        if not os.path.exists(file_name):
            tk.messagebox.showerror("Error", "Please select file to sign")
            return

        if not os.path.exists(cert) or not os.path.exists(priv):
            tk.messagebox.showerror("Error", "Please set cms certificate and private key")
            return

        print("INFO: Start to sign")
        print(f"INFO: CMS [{file_name}] -> [{file_name}.cms]")
        print(f"INFO: CMS certificate = [{cert}]")
        print(f"INFO: CMS private key = [{priv}]")
        # sign cms
        cms_bytes = sign_cms(cert, priv, file_name)
        with open(f'{file_name}.cms', 'wb+') as f:
            f.write(cms_bytes)

        ts_signed = False
        if os.path.exists(tscert) and os.path.exists(tspriv):
            # sign ts
            print(f"INFO: TSA certificate = [{tscert}]")
            print(f"INFO: TSA private key = [{tspriv}]")
            if self.ck_btn_state.get() == 1:
                # check timestamp format
                try:
                    get_time(self.timestamp.get())
                except ValueError:
                    print(f"ERROR: Invalid timestamp format:[{self.timestamp.get()}]")
                    tk.messagebox.showinfo("Error", f"Invalid timestamp format:[{self.timestamp.get()}]")
                    return

                print(f"INFO: TSA use time = {self.timestamp.get()}")
                tsa_bytes = sign_tsa(cms_bytes, file_name, tscert, tspriv, self.timestamp.get())
            else:
                print("INFO: TSA use system time")
                tsa_bytes = sign_tsa(cms_bytes, file_name, tscert, tspriv, None)
            ts_signed = True
            print(f"INFO: TSA timetramp query = [{file_name}.tsq]")
            print(f"INFO: TSA timetramp reply = [{file_name}.tsr]")
        else:
            print("INFO: no timestamp cert and private key is set, timestamp is not signed")

        # combine
        if ts_signed and self.combine_ts_to_cms.get():
            big_cms = append_tsa_to_cms(cms_bytes, tsa_bytes)
            with open(f'{file_name}.cms', 'wb+') as f:
                f.write(big_cms)
            print("INFO: Add timestamp to cms file success")

        tk.messagebox.showinfo("Success", "Sign Success")

    def run(self):
        self.win.mainloop()


def main():
    a = App()
    a.run()

if __name__ == '__main__':
    main()
