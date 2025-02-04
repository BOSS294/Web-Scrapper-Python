import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from ttkthemes import ThemedTk
import threading
import time
from scraper_functions import scrape_website


class ScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Web Scrapper (V1) ")
        self.root.geometry("1600x1500")  
        self.root.config(bg="#2c2c2c")

        
        self.header_frame = tk.Frame(self.root, bg="#5e2af3", bd=0, padx=20, pady=20)
        self.header_frame.pack(fill=tk.X)
        self.header_label = tk.Label(self.header_frame, text="Web Scrapper (V1) ", font=("Roboto", 28, "bold"), fg="white", bg="#5e2af3")
        self.header_label.pack(side=tk.LEFT, padx=20)

        self.made_by_label = tk.Label(self.header_frame, text="Made By: Mayank Chawdhari", font=("Segoe UI", 14), fg="white", bg="#5e2af3")
        self.made_by_label.pack(side=tk.RIGHT, padx=20)

        
        self.console_frame = tk.Frame(self.root, bg="#333333", bd=3, relief="solid", padx=20, pady=20)
        self.console_frame.pack(fill=tk.BOTH, padx=20, pady=20)

        
        self.console_text = tk.Text(self.console_frame, bg="#222222", fg="lime", font=("Courier New", 14), wrap="word", bd=0, height=28)
        self.console_text.pack(expand=True, fill=tk.BOTH, pady=(10, 20))  

        
        self.url_frame = tk.Frame(self.console_frame, bg="#333333")
        self.url_frame.pack(fill=tk.X, pady=10)

        
        self.url_entry_frame = tk.Frame(self.url_frame, bg="#444444", bd=2, relief="solid", padx=10, pady=10)
        self.url_entry_frame.pack(fill=tk.X, pady=5)

        self.url_entry = tk.Entry(self.url_entry_frame, font=("Courier New", 14), bg="#444444", fg="lime", bd=0, relief="flat", insertbackground="lime", width=50, highlightthickness=0)
        self.url_entry.pack(fill=tk.X)

        
        self.button_frame = tk.Frame(self.url_frame, bg="#333333")
        self.button_frame.pack(fill=tk.X, pady=(20, 0))  

        
        self.start_button = tk.Button(self.button_frame, text="Start Scraping", font=("Roboto", 14), bg="#4CAF50", fg="white", bd=0, relief="flat", command=self.start_scraping)
        self.start_button.pack(side=tk.LEFT, padx=10, fill=tk.X)
        self.start_button.bind("<Enter>", self.on_button_hover)
        self.start_button.bind("<Leave>", self.on_button_leave)
        self.start_button.bind("<Button-1>", self.on_button_click)

        self.stop_button = tk.Button(self.button_frame, text="Stop Scraping", font=("Roboto", 14), bg="#f44336", fg="black", bd=0, relief="flat", command=self.stop_scraping)
        self.stop_button.pack(side=tk.LEFT, padx=10, fill=tk.X)
        self.stop_button.config(state=tk.DISABLED)
        self.stop_button.bind("<Enter>", self.on_button_hover)
        self.stop_button.bind("<Leave>", self.on_button_leave)
        self.stop_button.bind("<Button-1>", self.on_button_click)

        
        self.close_button = tk.Button(self.button_frame, text="Close Program", font=("Roboto", 14), bg="#FF5733", fg="white", bd=0, relief="flat", command=self.close_program)
        self.close_button.pack(side=tk.LEFT, padx=10, fill=tk.X)
        self.close_button.bind("<Enter>", self.on_button_hover)
        self.close_button.bind("<Leave>", self.on_button_leave)
        self.close_button.bind("<Button-1>", self.on_button_click)

        self.counter_label = tk.Label(self.console_frame, text="Time Taken: 0s", font=("Roboto", 14), fg="lime", bg="#333333")
        self.counter_label.pack(pady=10)

        
        self.log_to_console("Welcome to Web Scraper (V1)", color="lime")

    def on_button_hover(self, event):
        event.widget.config(bg="#ff8c00", fg="white")  

    def on_button_leave(self, event):
        if event.widget == self.start_button:
            event.widget.config(bg="#4CAF50", fg="white")
        elif event.widget == self.stop_button:
            event.widget.config(bg="#f44336", fg="black")
        elif event.widget == self.close_button:
            event.widget.config(bg="#FF5733", fg="white")

    def on_button_click(self, event):
        event.widget.config(bg="#3700b3", fg="white")  

    def start_scraping(self):
        url = self.url_entry.get()
        if not url:
            self.log_to_console("No URL added! Please add a URL", color="red")
            return

        self.log_to_console(f"Starting scraping for {url}...", color="lime")

        
        self.start_button.config(state=tk.DISABLED, text="Scraping...")
        self.url_entry.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        self.scraping_thread = threading.Thread(target=self.scrape_website_thread, args=(url,))
        self.scraping_thread.start()

    def stop_scraping(self):
        
        self.log_to_console("Stopping scraping...", color="yellow")
        self.scraping_thread.join()

        
        self.start_button.config(state=tk.NORMAL, text="Start Scraping")
        self.url_entry.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def scrape_website_thread(self, url):
        def log_func(message, color="lime"):
            self.log_to_console(message, color)

        scrape_website(url, log_func)
        self.start_button.config(state=tk.NORMAL, text="Start Scraping")
        self.url_entry.config(state=tk.NORMAL)

    def log_to_console(self, message, color="lime"):
        self.console_text.insert(tk.END, f"{message}\n")
        self.console_text.see(tk.END)

    def close_program(self):
        self.root.quit()



root = ThemedTk(theme="arc")
app = ScraperApp(root)
root.mainloop()
