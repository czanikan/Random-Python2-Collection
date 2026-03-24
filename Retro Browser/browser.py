import Tkinter as tk
import urllib2
from HTMLParser import HTMLParser
import tkFont

HOME_PAGE = "home.html"

class RetroHTMLParser(HTMLParser):
     
    def __init__(self, text_widget, link_callback, title_callback):
        HTMLParser.__init__(self)
        self.text = text_widget
        self.link_callback = link_callback
        self.title_callback = title_callback

        self.current_tags = []
        self.current_link = None
        self.link_index = 0

        self.in_title = False
        self.page_title = ""

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.in_title = True

        elif tag == "br":
            self.text.insert("end", "\n")
            
        elif tag == "p":
            self.text.insert("end", "\n\n")

        elif tag in ("h1", "h2", "h3"):
            self.text.insert("end", "\n")
            self.current_tags.append(tag)

        elif tag == "b":
            self.current_tags.append("bold")

        elif tag == "i":
            self.current_tags.append("italic")

        elif tag == "a":
            for attr in attrs:
                if attr[0] == "href":
                    self.current_link = attr[1]

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
            if self.page_title:
                self.title_callback(self.page_title.strip())

        elif tag in ("h1", "h2", "h3"):
            if tag in self.current_tags:
                self.current_tags.remove(tag)
            self.text.insert("end", "\n")

        elif tag == "b":
            if "bold" in self.current_tags:
                self.current_tags.remove(tag)

        elif tag == "i":
            if "italic" in self.current_tags:
                self.current_tags.remove(tag)

        elif tag == "a":
            self.current_link = None

    def handle_data(self, data):
        if self.in_title:
            self.page_title += data
            return
        
        tags = list(self.current_tags)

        if self.current_link:
            tag_name = "link-%d" % self.link_index
            self.text.tag_config(tag_name, foreground="blue", underline=1)
            self.text.tag_bind(tag_name, "<Button-1>", lambda e, url=self.current_link: self.link_callback(url))
            tags.append(tag_name)
            self.link_index += 1

        self.text.insert("end", data, tuple(tags))

class BrowserTab:
    
    def __init__(self, parent):
        self.frame = tk.Frame(parent)

        text_frame = tk.Frame(self.frame)
        text_frame.pack(fill="both", expand=1)

        scrollbar = tk.Scrollbar(text_frame, width=14)
        scrollbar.pack(side="right", fill="y")

        self.text = tk.Text(text_frame, wrap="word", yscrollcommand=scrollbar.set)
        self.text.pack(side="left", fill="both", expand=1)
        self.text.bind("<MouseWheel>", lambda e: self.text.yview_scroll(-1 * (e.delta / 120), "units"))

        scrollbar.config(command=self.text.yview)

        self.history = []
        self.history_index = -1
        self.current_url = None
        self.button = None

class RetroBrowser:
    
    def __init__(self, root):
        self.root = root
        root.title("Retro Browser")

        top_frame = tk.Frame(root)
        top_frame.pack(fill="x")

        self.back_button = tk.Button(top_frame, text="Back", command=self.go_back)
        self.back_button.pack(side="left")

        self.forward_button = tk.Button(top_frame, text="Forward", command=self.go_forward)
        self.forward_button.pack(side="left")

        self.home_button = tk.Button(top_frame, text="Home", command=self.go_home)
        self.home_button.pack(side="left")

        self.url_entry = tk.Entry(top_frame)
        self.url_entry.pack(side="left", fill="x", expand=1)
        self.url_entry.bind("<Return>", self.load_from_entry)

        self.tab_bar = tk.Frame(root, bg="lightgray")
        self.tab_bar.pack(fill="x")

        self.tab_buttons_frame = tk.Frame(self.tab_bar, bg="lightgray")
        self.tab_buttons_frame.pack(side="left")

        self.new_tab_button = tk.Button(self.tab_buttons_frame, text="+", width=3, command=self.new_tab)
        self.new_tab_button.pack(side="left")

        self.container = tk.Frame(root)
        self.container.pack(fill="both", expand=1)

        self.tabs = []
        self.current_tab = None
        
        self.setup_fonts()

        self.new_tab()
        self.load_local_page(self.current_tab, HOME_PAGE)

    def new_tab(self):
        tab = BrowserTab(self.container)
        self.apply_fonts_to_text(tab.text)

        self.new_tab_button.pack_forget()

        button = tk.Button(self.tab_buttons_frame, text="New Tab", bg="lightgray", command=lambda t=tab: self.show_tab(t))
        button.bind("<Button-3>", lambda e, t=tab: self.close_tab(t))
        button.pack(side="left")

        self.new_tab_button.pack(side="left")

        tab.button = button
        self.tabs.append(tab)

        self.show_tab(tab)

    def close_tab(self, tab):
        if len(self.tabs) <= 1:
            return
        
        tab.frame.destroy()
        tab.button.destroy()

        self.tabs.remove(tab)

        self.show_tab(self.tabs[-1])

    def show_tab(self, tab):
        for t in self.tabs:
            t.frame.pack_forget()
            t.button.config(bg="lightgray")

        tab.frame.pack(fill="both", expand=1)
        tab.button.config(bg="white")

        self.current_tab = tab

        if tab.current_url:
            self.url_entry.delete(0, "end")
            self.url_entry.insert(0, tab.current_url)

    def set_tab_title(self, tab, title):
        if len(title) > 10:
            title = title[:10] + "..."

        tab.button.config(text=title)

    def setup_fonts(self):
        default_font = tkFont.Font(font='TkDefaultFont')

        bold_font = tkFont.Font(self.root, default_font)
        bold_font.configure(weight="bold")

        italic_font = tkFont.Font(self.root, default_font)
        italic_font.configure(slant="italic")

        h1_font = tkFont.Font(self.root, default_font)
        h1_font.configure(size=18, weight="bold")

        h2_font = tkFont.Font(self.root, default_font)
        h2_font.configure(size=16, weight="bold")

        h3_font = tkFont.Font(self.root, default_font)
        h3_font.configure(size=14, weight="bold")

        self.bold_font = bold_font
        self.italic_font = italic_font
        self.h1_font = h1_font
        self.h2_font = h2_font
        self.h3_font = h3_font

    def apply_fonts_to_text(self, text_widget):
        text_widget.tag_config("bold", font=self.bold_font)
        text_widget.tag_config("italic", font=self.italic_font)
        text_widget.tag_config("h1", font=self.h1_font)
        text_widget.tag_config("h2", font=self.h2_font)
        text_widget.tag_config("h3", font=self.h3_font)


    def load_from_entry(self, event=None):
        url = self.url_entry.get()
        if self.current_tab:
            self.load_page(self.current_tab, url)

    def load_page(self, tab, url, add_to_history=True):
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url

        try:
            response = urllib2.urlopen(url)
            html = response.read()

            tab.text.delete(1.0, "end")

            parser = RetroHTMLParser(tab.text, lambda link: self.load_page(tab, link), lambda title: self.set_tab_title(tab, title))
            parser.feed(html)

            if add_to_history:
                tab.history = tab.history[:tab.history_index + 1]

                tab.history.append(url)
                tab.history_index += 1

            tab.current_url = url

            self.url_entry.delete(0, "end")
            self.url_entry.insert(0, url)

        except Exception, e:
            tab.text.delete(1.0, "end")
            tab.text.insert("end", "Error loading page:\n\n" + str(e))

    def load_local_page(self, tab, filepath, add_to_history=True):

        try:
            f = open(filepath, "r")
            html = f.read()
            f.close()

            tab.text.delete(1.0, "end")

            parser = RetroHTMLParser(tab.text, lambda link: self.load_page(tab, link), lambda title: self.set_tab_title(tab, title))

            parser.feed(html)

            if add_to_history:
                tab.history = tab.history[:tab.history_index + 1]
                tab.history.append(filepath)
                tab.history_index += 1

            tab.current_url = filepath

            self.url_entry.delete(0, "end")
            self.url_entry.insert(0, filepath)

        except Exception, e:
            tab.text.delete(1.0, "end")
            tab.text.insert("end", "Error loading home page:\n\n" + str(e))

    def go_back(self):
        tab = self.current_tab

        if not tab:
            return
        
        if tab.history_index <= 0:
            return
        
        tab.history_index -= 1
        url = tab.history[tab.history_index]

        self.load_page(tab, url, add_to_history=False)

    def go_forward(self):
        tab = self.current_tab

        if not tab:
            return
        
        if tab.history_index >= len(tab.history) - 1:
            return
        
        tab.history_index += 1

        url = tab.history[tab.history_index]

        self.load_page(tab, url, add_to_history=False)

    def go_home(self):
        if self.current_tab:
            self.load_local_page(self.current_tab, HOME_PAGE)

if __name__ == "__main__":
    root = tk.Tk()
    browser = RetroBrowser(root)
    root.mainloop()
