from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess
import os

class Ide:
   def __init__(self, name):
      self.name = name + ".py"
      self.compiler = Tk()
      self.compiler.title("Bicorne-IDE")
      self.file_path = ''
      self.output = ""
      self.compiler.protocol("WM_DELETE_WINDOW", self.close)

      menu_bar = Menu(self.compiler)

      file_menu = Menu(menu_bar, tearoff=0)
      file_menu.add_command(label="Sauvegarder", command=self.save_as)
      file_menu.add_command(label="Soummette", command=exit)
      menu_bar.add_cascade(label="Fichier", menu=file_menu)

      run_bar = Menu(menu_bar, tearoff=0)
      run_bar.add_command(label="Lancer", command=self.run)
      menu_bar.add_cascade(label="Run", menu=run_bar)

      self.compiler.config(menu=menu_bar)
      self.editor = Text()
      self.editor.pack()
      self.code_output = Text(height=10)
      self.code_output.pack()
      self.compiler.mainloop()

   def set_file_path(self, path):
      self.file_path = self.path

   def save_as(self):
      self.path = os.getcwd() + '\\'+self.name
      with open(self.path, "w") as file:
         code = self.editor.get("1.0", END)
         file.write(code)
         self.set_file_path(self.path)

   def run(self):
      if self.file_path == "":
         save_prompt = Toplevel()
         text = Label(save_prompt, text="Sauvegardez votre code!")
         text.pack()
         return
      command = f"python {self.file_path}"
      process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr = subprocess.PIPE, shell=True)
      self.output, self.error = process.communicate()
      self.code_output.insert("1.0", self.output)
      self.code_output.insert("1.0", self.error)

   def close(self):
      self.save_as()
      self.run()
      if len(self.error) <= 5:
         self.compiler.destroy()
      else:
         self.code_output.insert("1.0", self.error)

   def getoutput(self):
      return self.output

